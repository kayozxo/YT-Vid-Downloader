import streamlit as st
from pytube import YouTube
from tkinter import filedialog
import os

def get_info(url):
    yt = YouTube(url)
    details= {}
    details["image"] = yt.thumbnail_url
    details["title"] = yt.title
    details["length"] = yt.length
    return details

st.set_page_config(page_title="YouTube Downloader", page_icon=":zap:")
st.title(":zap: YouTube Downloader")
url = st.text_input("**Enter URL**")

def download_video():
  try:
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, file_extension="mp4")
    highest_res_stream = streams.get_highest_resolution()
    DS = highest_res_stream
    save_path = filedialog.askdirectory()
    if save_path:
      DS.download(output_path=save_path)
      st.success("Video is successfully downloaded!")

  except Exception:
    st.warning("Invalid URL!")

def download_audio():
  try:
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    save_path = filedialog.askdirectory()
    if save_path:
      out_file = audio.download(output_path=save_path)
      base, ext = os.path.splitext(out_file)
      new_file = base + '.mp3'
      os.rename(out_file, new_file)
      st.success("Audio is successfully downloaded!")

  except Exception:
    st.warning("Invalid URL!")


col1, col2 = st.columns(2)
col1.button("Download Video :film_frames:", on_click=download_video, use_container_width=True)
col2.button("Download Audio :musical_note:", on_click=download_audio, use_container_width=True)

if url:
    v_info = get_info(url)
    st.image(v_info["image"], use_column_width=True, caption=f"{v_info['title']} - {v_info['length']} seconds")