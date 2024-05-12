<h1>Audio Feature Extraction and Music Recommendation System Report</h1>


---
<h2>Overview</h2>
This repository contain a Python script (extract_mfcc_to_mongodb.py) for extracting Mel-Frequency Cepstral Coefficients (MFCC) features from audio files, associating them with metadata from a tracks dataset, and storing the results in MongoDB. The script leverages libraries like librosa for audio processing and pandas for data manipulation. Additionally, it demonstrates a music recommendation system implemented using Apache Spark's ALS (Alternating Least Squares) algorithm and MongoDB.

<h2>Dependencies</h2>

Ensure you have the following dependencies installed before running the project:

- [Python 3.x](https://www.python.org/downloads/)

- [Librosa](https://librosa.org/doc/main/install.html)

- [Pandas](https://pandas.pydata.org/)

- [PyMongo](https://pypi.org/project/pymongo/)

- [Apache Spark](https://spark.apache.org/downloads.html)

- [MongoDB](https://www.mongodb.com/try/download/community)

- [numpy](https://numpy.org/install/)

- [scikit-learn](https://scikit-learn.org/stable/install.html)

- [matplotlib](https://matplotlib.org/stable/users/installing.html)

Make sure to install these dependencies using pip or follow the respective installation instructions linked above. Additionally, set up MongoDB based on your system requirements and adjust configurations accordingly in your project scripts.


<h2>Methodology</h2>
<h4>1. Audio Feature Extraction and Storage</h4>
<h5>Data Preparation:</h5>

Ensure your audio files (.mp3 format) are structured within a folder named fma_large, and the metadata (tracks.csv) is located in fma_metadata.

<h5>MongoDB Connection:</h5> 
Update the MongoDB connection URI in the script (extract_mfcc_to_mongodb.py) to match your server configuration.

<h5>Feature Extraction:</h5>

Utilizes librosa to compute MFCC features for each audio file.
Matches track IDs extracted from filenames with metadata (track title, genre) from tracks.csv.

<h5>Data Storage:</h5>

Establishes a connection to MongoDB and specifies a database (mfcc_database2) and collection (mfcc_collection2) for storing processed data.
Documents containing track ID, genre, title, and computed MFCC features are stored in MongoDB.
<h4>2. Music Recommendation System</h4>
<h5>Spark Session Creation:</h5>

Sets up a Spark session with MongoDB integration for data loading and saving.

<h5>Data Processing:</h5>

Loads data from MongoDB into a DataFrame.
Utilizes StringIndexer to index track_id and genre_all columns.

<h5>ALS Model Building:</h5>

Splits the data into training and testing sets.
Configures and trains an ALS (Alternating Least Squares) model using implicit feedback (rating column).

<h5>Similarity Calculation:</h5>

Defines a UDF (User Defined Function) to compute cosine similarity between item factors.
Recommends similar songs based on the input song ID using computed item factors.

<h2>Findings</h2>
<h4>1. Audio Feature Extraction and Storage</h4>
<h5>Effectiveness:</h5>

Successfully extracts MFCC features from audio files using librosa.
Matches audio metadata with track IDs and stores enriched data in MongoDB.
<h5>Implementation:</h5>

The script efficiently handles exceptions during audio processing and data lookup to ensure  smooth execution.

<h4>2. Music Recommendation System</h4>

<h5>Effectiveness:</h5>

The ALS-based recommendation model provides a basis for song recommendations using implicit feedback.
Recommendations are based on item factors learned from the dataset.

<h5>Evaluation:</h5>

The system can be evaluated through metrics like precision, recall, and user engagement metrics based on user feedback.

<h2>Results</h2>

[Output Screenshots](https://github.com/AbdurRahmanGrami/bda-project/files/15287229/Outputs.zip)


<h2>Authors</h2>

- Muneeb Ahmad (22i-1889)
- Abdur Rahman Grami (22i-2008)
- Samiullah (22i-1962)

<h2>Conclusion</h2>
This project provides a comprehensive framework for audio feature extraction, metadata association, and music recommendation. The combined usage of librosa, pandas, MongoDB, and Apache Spark's ALS algorithm offers a solid foundation for building and evaluating music recommendation systems. Further enhancements can involve fine-tuning model parameters, incorporating additional features, and integrating user feedback for iterative improvement.
For detailed instructions and code implementation, refer to the provided repository (audio-feature-extraction) and its README.md.
