from flask import Flask
import streamlit as st
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

# Function to download audio from YouTube video
def download_audio(yt):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    stream = yt.streams.filter(only_audio=True).first()
    stream.download('downloads', filename='audio.mp4')

    mp4_file = 'downloads/audio.mp4'
    mp3_file = 'downloads/audio.mp3'

    if os.path.exists(mp4_file):
        audio = AudioFileClip(mp4_file)
        audio.write_audiofile(mp3_file)
        audio.close()
        os.remove(mp4_file)
        return mp3_file
    else:
        return None

# Function to download video from YouTube
def download_video(yt, quality):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    if quality == "Highest":
        stream = yt.streams.get_highest_resolution()
    elif quality == "Lowest":
        stream = yt.streams.get_lowest_resolution()
    else:
        # If quality is specified as a string (e.g., "720p"), try to find a matching stream
        stream = yt.streams.filter(res=quality).first()
    
    if stream:
        stream.download('downloads')
        return 'downloads/' + yt.title + '.mp4'
    else:
        return None

# Main function to define the Streamlit app
def main():
    # Title and background styling
    st.markdown(
        """
        <style>
        .title {
            font-size: 36px;
            color: #f0f0f0;
            text-align: center;
            padding-bottom: 20px;
        }
        .down {
            font-weight: bold;
        }
        .tuber {
            color: red;
        }
        .container {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f0f0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Title
    st.markdown("<h1 class='title'><span class='down'>Down</span><span class='tuber'>Tuber</span></h1>", unsafe_allow_html=True)

    # Text input for YouTube video link
    video_link = st.text_input("Enter the YouTube video link:", "")

    # Quality options
    quality_options = ["Highest", "Lowest", "1080p", "720p", "480p", "360p"]
    quality = st.selectbox("Select video quality:", options=quality_options)

    # Center-align buttons
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    # Button for downloading audio
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Download Audio", key="download_audio"):
        if video_link:
            try:
                yt = YouTube(video_link)
                audio_path = download_audio(yt)
                if audio_path:
                    st.success("Audio download completed!")
                    st.audio(audio_path, format='audio/mp3')
                else:
                    st.error("Error: Unable to download audio.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a YouTube video link.")


    # Button for downloading video
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Download Video", key="download_video"):
        if video_link:
            try:
                yt = YouTube(video_link)
                video_path = download_video(yt, quality)
                if video_path:
                    st.success("Video download completed!")
                    st.video(video_path)
                else:
                    st.error("Error: Unable to download video.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a YouTube video link.")

    # Close the div for center-alignment
    st.markdown("</div>", unsafe_allow_html=True)

# Create a Flask app
app = Flask(__name__)

# Define a route for your Streamlit app
@app.route('/')
def streamlit_app():
    # Call your Streamlit app's main function
    main()
    return ''

# Run the Flask app
if __name__ == '__main__':
    app.run()
