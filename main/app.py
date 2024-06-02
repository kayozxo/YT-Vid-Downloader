import streamlit as st
from pytube import YouTube
import os

directory= 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

def get_info(url):
    yt = YouTube(url)
    details= {}
    details["image"] = yt.thumbnail_url
    details["title"] = yt.title
    details["length"] = yt.length
    return details

st.set_page_config(page_title="YouTube Downloader", page_icon=":zap:")
st.title(":zap: YouTube Downloader")
url = st.text_input("**Paste URL here 👇**", placeholder="https://www.youtube.com/")

code = """
<a href="https://www.buymeacoffee.com/kayozxo" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=kayozxo&button_colour=40DCA5&font_colour=ffffff&font_family=Lato&outline_colour=000000&coffee_colour=FFDD00" /></a>

"""


def download_video():
  with st.spinner("Downloading..."):
    try:
      yt = YouTube(url)
      streams = yt.streams.filter(progressive=True, file_extension="mp4")
      highest_res_stream = streams.get_highest_resolution()
      DS = highest_res_stream
      save_path = directory
      if save_path:
        DS.download(output_path=save_path)
        st.success("Video is successfully downloaded!")
    except Exception:
      st.warning("Invalid URL!")

def download_audio():
  with st.spinner("Downloading..."):
    try:
      yt = YouTube(url)
      audio = yt.streams.filter(only_audio=True).first()
      save_path = directory
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

with st.sidebar:
  st.html(code)