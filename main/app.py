import streamlit as st
from pytube import YouTube
import os
import streamlit_shadcn_ui as ui
from googleapiclient.discovery import build
from pytube import extract

directory= 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

st.set_page_config(page_title="YouTube Downloader", page_icon=":zap:")

st.title(":zap: YouTube Downloader")
st.markdown("Paste URL here")
url = ui.input(placeholder="https://www.youtube.com/", key="url", type="text")

code = """
<a href="https://www.buymeacoffee.com/kayozxo" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=kayozxo&button_colour=40DCA5&font_colour=ffffff&font_family=Lato&outline_colour=000000&coffee_colour=FFDD00" /></a>

"""
def get_info(url):
    yt = YouTube(url)

    video_id = extract.video_id(url)

    youtube = build('youtube', 'v3', developerKey='AIzaSyC54QjnV9FiDRyvwu2_JLoJgnmWq4VoLdo')

    video_request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    video_response = video_request.execute()

    print(video_response)

    details = {
        "image": yt.thumbnail_url,
        "title": yt.title,
        "length": yt.length,
        "likes": 'N/A',  # default value
        "views": 'N/A'   # default value
    }

    if 'items' in video_response and len(video_response['items']) > 0:
        video_details = video_response['items'][0]['statistics']
        details["likes"] = video_details.get('likeCount', 'N/A')
        details["views"] = video_details.get('viewCount', 'N/A')

    return details

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
with col1:
  vid_btn = ui.button("Download Video", variant="secondary", key="vid_btn", class_name="w-full")

with col2:
  aud_btn = ui.button("Download Audio", variant="secondary", key="aud_btn", class_name="w-full")

if vid_btn:
  download_video()

if aud_btn:
  download_audio()

if url:
    v_info = get_info(url)
    st.image(v_info["image"], use_column_width=True, caption=f"{v_info['title']}")
    cols = st.columns(3)
    with cols[0]:
      ui.metric_card(title="Total Views", content=f"{v_info['views']}")
    with cols[1]:
      ui.metric_card(title="Total Likes", content=f"{v_info['likes']}")
    with cols[2]:
      ui.metric_card(title="Video Length", content=f"{v_info['length']} sec")

with st.sidebar:
  st.html(code)