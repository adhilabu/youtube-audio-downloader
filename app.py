import streamlit as st
import os
from youtube_utils import download_audio

st.title("YouTube Audio Downloader")

# Create a directory for downloads if it doesn't exist
download_dir = "C:/Users/user0/Downloads/telegram/youtube_audio_downloader/downloads"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

search_query = st.text_input("Enter song name or YouTube URL:")

if st.button("Download Audio (MP3)"):
    if search_query:
        st.info(f"Searching and downloading audio for: {search_query}")
        with st.spinner("Downloading..."):
            try:
                # Ensure the download path is absolute for clarity
                absolute_download_dir = os.path.abspath(download_dir)
                file_path = download_audio(search_query, download_path=absolute_download_dir)

                if file_path and os.path.exists(file_path):
                    st.success("Download complete!")
                    file_name = os.path.basename(file_path)
                    # Read the file content for the download button
                    with open(file_path, "rb") as fp:
                        btn = st.download_button(
                            label=f"Download {file_name}",
                            data=fp,
                            file_name=file_name,
                            mime="audio/mpeg"
                        )
                else:
                    st.error("Download failed. Could not find the downloaded file or an error occurred during download. Please check the logs or try a different query.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a search query or URL.")

# Optional: Add some instructions or information
st.markdown("--- ")
st.markdown("**How to use:** Enter the name of a song or a direct YouTube video URL in the box above and click the button. The audio will be downloaded as an MP3 file.")

