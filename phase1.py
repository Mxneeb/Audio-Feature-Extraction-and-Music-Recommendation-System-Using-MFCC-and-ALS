
from pymongo import MongoClient
import pandas as pd
import librosa
import os
import numpy as np 


pathToDataset = 'fma_large'
# making df of tracks and skipping first 2 redundant rows
pathToFeatureSet = pd.read_csv('tracks.csv', skiprows=2, header=0) # here header is defined so that it understands that it has to take the 0th row as the column names row

FilteredFeatures = pathToFeatureSet[['title', 'track_id', 'genres_all']]

# mongoDB details
client = MongoClient('mongodb://localhost:27017/')
db = client['MuneebTest']
collection = db['SpotifyBDATest']



# checking columms if they're correct
# print (FilteredFeatures.head()) 


def mfccCalculatorFunction(audio_path):
    audioData, samplingRate = librosa.load(audio_path, sr=20000)
    mfccCalculated = librosa.feature.mfcc(y=audioData, sr=samplingRate, n_mfcc=13)
    mfccMeans = np.mean(mfccCalculated, axis=1)
    mfccMeansList = mfccMeans.tolist()
    return mfccMeansList


# going over all the folders and files using os.walk to iterate over all the files in the dataset
for root, dirs, mp3Files in os.walk(pathToDataset):
    for file in mp3Files:
        if file.endswith('.mp3'):
            try:
                # Extract track ID from the filename
                trackID = str(file.split('.')[0].lstrip('0'))

                # Filter tracks DataFrame to find matching track ID
                tracksInformation = FilteredFeatures[FilteredFeatures['track_id'] == trackID]
                
                print (tracksInformation.head()) 
                
                if not tracksInformation.empty:
                    songTitle = tracksInformation['title'].iloc[0]
                    genre = tracksInformation['genres_all'].iloc[0]

                    audio_path = os.path.join(root, file)
                    MFCCFeatureSet = mfccCalculatorFunction(audio_path)

                    audioDataToSendToMongoDB = {
                        'track_id': file ,
                        'genre_all': genre,
                        'title': songTitle,
                        'mfcc_features': MFCCFeatureSet
                    }
                    
                    # Sending data to mongoDB
                    collection.insert_one(audioDataToSendToMongoDB)
                    print(f" MFCC features for {audio_path} sent to MongoDB.")
                else:
                    print(f" {track_id} Does not Exist, moving onto the next track")
            except Exception as e:
                print(f"{file} might be currupted: {e}")
