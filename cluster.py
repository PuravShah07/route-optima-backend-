import numpy as np

def batch_clusters(orders, batch_size=4):
    # Orders should be sorted so paid first; each order = dict
    # Returns: List of batches, each batch is a list of orders
    
    clusters = []
    batch = []
    for order in orders:
        batch.append(order)
        if len(batch) == batch_size:
            clusters.append(batch)
            batch = []
    if batch:  # add last, incomplete batch
        clusters.append(batch)
    return clusters


