'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import json
import requests
import os
import analysis_network_centrality
import analysis_similar_actors_genre

# Ingest and save the IMDb movies dataset
def download_dataset(url, save_path):
    """
    Downloads the dataset from the specified URL and saves it to the given path.
    """
    response = requests.get(url)
    if response.status_code == 200:
        # Save the raw text response
        with open(save_path, 'w') as file:
            file.write(response.text)
        print(f"Dataset downloaded and saved to {save_path}")
    else:
        print("Failed to download dataset")

def load_dataset(file_path):
    """
    Loads the dataset from the specified file path, reading line by line to handle multiple JSON objects.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                movie = json.loads(line)
                data.append(movie)
            except json.JSONDecodeError as e:
                print(f"JSON decoding failed: {e}")
    return data

# Call functions / instantiate objects from the two analysis .py files
def main():
    # Define the URL and the save path for the dataset
    url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
    save_path = os.path.join('data', 'imdb_movies_2000to2022.prolific.json')
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Download the dataset
    download_dataset(url, save_path)
    
    # Load the dataset
    data = load_dataset(save_path)
    
    # Call analysis functions
    analysis_network_centrality.run_analysis(data)
    analysis_similar_actors_genre.run_analysis(data)

if __name__ == "__main__":
    main()
