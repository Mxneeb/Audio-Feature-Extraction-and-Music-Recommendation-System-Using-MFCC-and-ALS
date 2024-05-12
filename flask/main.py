from flask import Flask, render_template

app = Flask(__name__)

# Sample song data
songs = [
    {"title": "Song 1", "artist": "Artist 1", "file": "song1.mp3"},
    {"title": "Song 2", "artist": "Artist 2", "file": "song2.mp3"},
    {"title": "Song 3", "artist": "Artist 3", "file": "song3.mp3"},
    {"title": "Song 4", "artist": "Artist 4", "file": "song4.mp3"},
    {"title": "Song 5", "artist": "Artist 5", "file": "song5.mp3"},
    {"title": "Song 6", "artist": "Artist 6", "file": "song6.mp3"},
    {"title": "Song 7", "artist": "Artist 7", "file": "song7.mp3"},
    {"title": "Song 8", "artist": "Artist 8", "file": "song8.mp3"},
    {"title": "Song 9", "artist": "Artist 9", "file": "song9.mp3"},
    {"title": "Song 10", "artist": "Artist 10", "file": "song10.mp3"}
    # Add more songs as needed
]
 
 

@app.route('/')
def main():
    return render_template('index.html', songs=songs)

if __name__ == '__main__':
    app.run(debug=True)
 