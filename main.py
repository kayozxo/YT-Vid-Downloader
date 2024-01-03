from pytube import YouTube
import tkinter as tk
import customtkinter
from tkinter import filedialog
import os
from sys import platform
import subprocess

def download_video(choice):
  try:
    ytlink = link.get()
    ytobject = YouTube(ytlink, on_progress_callback=on_prog)
    streams = ytobject.streams.filter(progressive=True, file_extension="mp4")

    if choice == options[0]:
      r360 = streams.filter(res="360p").first()
      DS = r360
    elif choice == options[1]:
      r720 = streams.filter(res="720p").first()
      DS = r720
    else:
      highest_res_stream = streams.get_highest_resolution()
      DS = highest_res_stream

    title.configure(text=ytobject.title, text_color="white")

    save_path = filedialog.askdirectory()
    if save_path:
      finishLabel.configure(text="")
      finishLabel.configure(text=f"Selected Folder: {save_path}", text_color="white")
      DS.download(output_path=save_path)
      finishLabel.configure(text="Video Downloaded Successfully!", text_color="white", font=("Montserrat Medium", 12)) 

      if platform == 'darwin':
        subprocess.Popen(["open", save_path])
      elif platform == 'win32':
        os.startfile(save_path)
      else:
        os.system('xdg-open "%s"' % save_path)
        
  except Exception:
    title.configure(text="YT-VIDEO DOWNLOADER")
    finishLabel.configure(text="INVALID URL", text_color="red", font=("Montserrat Medium", 12))

def download_audio():
  try:
    ytlink = link.get()
    ytobject = YouTube(ytlink, on_progress_callback=on_prog)
    audio = ytobject.streams.filter(only_audio=True).first()
    title.configure(text=ytobject.title, text_color="white")

    save_path = filedialog.askdirectory()
    if save_path:
      finishLabel.configure(text="")
      finishLabel.configure(text=f"Selected Folder: {save_path}", text_color="white")
      out_file = audio.download(output_path=save_path)
      base, ext = os.path.splitext(out_file) 
      new_file = base + '.mp3'
      os.rename(out_file, new_file) 
      finishLabel.configure(text="Audio Downloaded Successfully!", text_color="white", font=("Montserrat Medium", 12)) 

      if platform == 'darwin':
        subprocess.Popen(["open", save_path])
      elif platform == 'win32':
        os.startfile(save_path)
      else:
        os.system('xdg-open "%s"' % save_path)
      
  except Exception:
    title.configure(text="YT-VIDEO DOWNLOADER")
    finishLabel.configure(text="INVALID URL", text_color="red", font=("Montserrat Medium", 12))

def on_prog(stream, chunk, bytes_rem):
  total_size = stream.filesize
  bytes_downloaded = total_size-bytes_rem
  percentage_of_completion = bytes_downloaded / total_size * 100
  per = str(int(percentage_of_completion))
  progNum.configure(text=per + "%")
  progNum.update()
  progBar.set(float(percentage_of_completion / 100))
  
# system settings
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("theme.json")

# app frame
app = customtkinter.CTk()
app.geometry("800x500")
app.title("YT Downloader")

# adding ui elements
title = customtkinter.CTkLabel(app, text="YT-VIDEO DOWNLOADER", font=("Montserrat Black", 20))
title.place(x=400, y=50, anchor="center")

uv = customtkinter.CTkLabel(app, text="Enter URL", font=("Montserrat", 12, "bold"))
uv.place(x=220, y=95)

# link input
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var, font=("Montserrat", 13), corner_radius=5)
link.place(x=220, y=120)

# finish label
finishLabel = customtkinter.CTkLabel(app, text="", font=("Montserrat Medium", 12))
finishLabel.place(x=400, y=240, anchor="center")

# prog bar
progNum = customtkinter.CTkLabel(app, text="0%", font=("Montserrat", 12, "bold"))
progNum.place(x=555, y=107, anchor="center")

progBar = customtkinter.CTkProgressBar(app, width=800, height=5)
progBar.set(0)
progBar.place(x=0, y=0)

#audio download
ad = customtkinter.CTkButton(app, text="Download Audio", font=("Montserrat Medium", 12), command = download_audio, corner_radius=5, width=160, height=34)
ad.place(x=220, y=170)

# res selection / download

options = ["Download 360p", "Download 720p", "Download 1080p"]
res_selection = customtkinter.CTkComboBox(master=app, values=options, width=160, height=34, font=("Montserrat Medium", 12), dropdown_font=("Montserrat Medium", 12), corner_radius=5, state="readonly", command = download_video, justify="center")
res_selection.place(x=410, y=170)

# run app
app.mainloop() 