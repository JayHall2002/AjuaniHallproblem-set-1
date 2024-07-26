'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import os
from datetime import datetime

# Build the graph
g = nx.Graph()

# Function to run analysis
def run_analysis(data):
    """
    Builds a graph from the IMDb movies dataset and performs network centrality analysis.
    """
    # Add nodes and edges to the graph
    for movie in data:
        actors = movie['actors']
        
        # Create a node for every actor
        for actor_id, actor_name in actors:
            g.add_node(actor_id, name=actor_name)
        
        # Iterate through the list of actors, generating all pairs
        for i in range(len(actors)):
            for j in range(i + 1, len(actors)):
                left_actor_id, left_actor_name = actors[i]
                right_actor_id, right_actor_name = actors[j]
                
                # Get the current weight, if it exists
                if g.has_edge(left_actor_id, right_actor_id):
                    g[left_actor_id][right_actor_id]['weight'] += 1
                else:
                    # Add an edge for these actors
                    g.add_edge(left_actor_id, right_actor_id, weight=1)

    # Print the info below
    print("Nodes:", len(g.nodes))

    # Print the 10 most central nodes
    centrality = nx.degree_centrality(g)
    sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    for actor_id, cent in sorted_centrality:
        print(f"Actor ID: {actor_id}, Centrality: {cent}")

    # Create a DataFrame to save the results
    edge_data = [
        (g.nodes[left]['name'], '<->', g.nodes[right]['name'], g[left][right]['weight'])
        for left, right in g.edges
    ]
    df = pd.DataFrame(edge_data, columns=['left_actor_name', '<->', 'right_actor_name', 'weight'])

    # Save the DataFrame to a CSV file
    output_path = os.path.join('output', f'network_centrality_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    df.to_csv(output_path, index=False)
    print(f"Network centrality analysis complete. Results saved to '{output_path}'")
