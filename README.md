# YouTube Audio Downloader

This project provides a simple web interface built with Streamlit to search for songs on YouTube (or use a direct URL) and download their audio as MP3 files.

## Features

- Search YouTube by song name or keyword.
- Input a direct YouTube video URL.
- Downloads the audio of the first search result or the specified URL.
- Converts the audio to MP3 format.
- Provides a download button for the MP3 file directly in the web interface.

## Project Structure

```
youtube_audio_downloader/
├── app.py             # Main Streamlit application file
├── youtube_utils.py   # Module for YouTube search and download logic
├── requirements.txt   # Python package dependencies
├── downloads/         # Default directory for downloaded MP3 files (created automatically)
└── README.md          # This file
```

## Setup

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   `pip` (Python package installer) installed.
    *   `ffmpeg` installed on your system. `yt-dlp` requires `ffmpeg` for audio conversion.
        - On Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
        - On macOS (using Homebrew): `brew install ffmpeg`
        - On Windows: Download from the official FFmpeg website and add it to your system's PATH.

2.  **Clone or Download:**
    *   Place the project files (`app.py`, `youtube_utils.py`, `requirements.txt`) into a directory on your local machine.

3.  **Create Virtual Environment (Recommended):**
    *   Navigate to the project directory in your terminal.
    *   Create a virtual environment: `python -m venv venv`
    *   Activate the virtual environment:
        *   On macOS/Linux: `source venv/bin/activate`
        *   On Windows: `.\venv\Scripts\activate`

4.  **Install Dependencies:**
    *   With the virtual environment activated, install the required Python packages:
        `pip install -r requirements.txt`

## Running the Application

1.  **Activate Virtual Environment (if not already active):**
    *   Navigate to the project directory.
    *   Activate the virtual environment (see Setup step 3).

2.  **Run Streamlit:**
    *   Execute the following command in your terminal:
        `streamlit run app.py`

3.  **Access the UI:**
    *   Streamlit will typically open the application automatically in your default web browser.
    *   If not, open your browser and go to the local URL provided in the terminal (usually `http://localhost:8501`).

4.  **Use the App:**
    *   Enter a song name or YouTube URL in the input field.
    *   Click the "Download Audio (MP3)" button.
    *   Wait for the download and conversion process to complete.
    *   Once finished, a download button for the MP3 file will appear.

