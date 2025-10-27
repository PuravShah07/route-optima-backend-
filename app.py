from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from cluster import batch_clusters
from route_optimizer import optimize_route, route_metrics

app = Flask(__name__)
CORS(app)  # <-- Enables CORS for all routes and origins

# Ensure uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = os.path.join('uploads', file.filename)
    file.save(filename)

    try:
        # Read CSV and filter only pending orders
        df = pd.read_csv(filename)
        df_pending = df[df['OrderStatus'] == 'Pending']
        # Prioritize paid deliveries (IsPaidDelivery==1)
        df_pending_sorted = df_pending.sort_values(by='IsPaidDelivery', ascending=False)
        orders_list = df_pending_sorted.to_dict(orient='records')

        # Cluster pending orders (vehicle batch size = 4)
        clusters = batch_clusters(orders_list, batch_size=4)

        # Optimize routes and calculate metrics
        clusters_data = []
        for batch in clusters:
            optimized = optimize_route(batch)
            metrics = route_metrics(optimized)
            clusters_data.append({
                'route': optimized,
                'metrics': metrics
            })

        return jsonify({
            'message': 'Routes optimized and metrics calculated!',
            'clusters_count': len(clusters_data),
            'clusters': clusters_data
        })
    except Exception as e:
        # Return the exception string for debugging (consider hiding in production)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Listen on all interfaces for frontend backend communication
    app.run(host="0.0.0.0", port=5000, debug=True)
