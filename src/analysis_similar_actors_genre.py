'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

import pandas as pd
from sklearn.metrics import DistanceMetric
import os
from datetime import datetime

# Write your code below
def run_analysis(data):
    """
    Analyzes actors' genre appearances and finds the most similar actors based on genre.
    """
    # Create a DataFrame for actors and their genre appearances
    genre_list = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
    actor_genres = {}

    for movie in data:
        genres = movie['genre']
        actors = movie['actors']
        for actor_id, actor_name in actors:
            if actor_id not in actor_genres:
                actor_genres[actor_id] = {genre: 0 for genre in genre_list}
                actor_genres[actor_id]['name'] = actor_name
            for genre in genres:
                if genre in actor_genres[actor_id]:
                    actor_genres[actor_id][genre] += 1

    df = pd.DataFrame.from_dict(actor_genres, orient='index')
    
    # Select Chris Hemsworth as the query actor
    query_actor_id = 'nm1165110'
    query_actor = df.loc[query_actor_id, genre_list].values.reshape(1, -1)
    
    # Calculate Euclidean distances
    distance_metric = DistanceMetric.get_metric('euclidean')
    distances = distance_metric.pairwise(df[genre_list].values, query_actor).flatten()
    
    df['distance'] = distances
    top_10_similar = df.sort_values(by='distance').head(11).drop(query_actor_id)
    
    # Save the results to a CSV file
    output_path = os.path.join('output', f'similar_actors_genre_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    top_10_similar[['name', 'distance']].to_csv(output_path, index_label='actor_id')
    print(f"Similar actors analysis complete. Results saved to '{output_path}'")
    
    # Describe how the list changes with Euclidean distance
    print("Top 10 most similar actors to Chris Hemsworth based on genre appearances (using Euclidean distance):")
    print(top_10_similar[['name', 'distance']])

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)
