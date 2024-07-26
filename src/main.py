'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import json
import requests
import os
import analysis_network_centrality
import analysis_similar_actors_genre

# Ingest and save the imbd_movies dataset
def download_dataset(url, save_path):

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'w') as file:
            json.dump(response.json(), file)
        print(f"Dataset downloaded and saved to {save_path}")
    else:
        print("Failed to download dataset")


# Call functions / instanciate objects from the two analysis .py files
def main():
   # Define the URL and the save path for the dataset
    url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
    save_path = os.path.join('data', 'imdb_movies_2000to2022.prolific.json')
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Download the dataset
    download_dataset(url, save_path)
    
    # Load the dataset
    with open(save_path, 'r') as file:
        data = json.load(file)
    
    # Call analysis functions
    analysis_network_centrality.run_analysis(data)
    analysis_similar_actors_genre.run_analysis(data)


if __name__ == "__main__":
    main()
