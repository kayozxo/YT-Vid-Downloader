from pytube import YouTube
import tkinter as tk
import customtkinter
from tkinter import filedialog
import os
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
title.pack(padx=10, pady=30, anchor=tk.CENTER)

uv = customtkinter.CTkLabel(app, text="Enter URL", font=("Montserrat", 12, "bold"))
uv.pack(padx=10, pady=0, anchor=tk.CENTER)

# link input
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var, font=("Montserrat", 13), corner_radius=5)
link.pack(padx=1, pady=10, anchor=tk.CENTER)

# finish label
finishLabel = customtkinter.CTkLabel(app, text="", font=("Montserrat Medium", 12))
finishLabel.pack(padx=1, pady=10, anchor=tk.CENTER)

# prog bar
progNum = customtkinter.CTkLabel(app, text="0%", font=("Montserrat Medium", 15))
progNum.pack(padx=1, pady=0, anchor=tk.CENTER)

progBar = customtkinter.CTkProgressBar(app, width=400, height=2)
progBar.set(0)
progBar.pack(padx=10, pady=15, anchor=tk.CENTER)

#audio download
ad = customtkinter.CTkButton(app, text="Download Audio", font=("Montserrat Medium", 12), command = download_audio, corner_radius=5, width=160, height=34)
ad.pack(padx=1, pady=15, anchor=tk.CENTER)

# res selection / download
rs = customtkinter.CTkLabel(app, text="Download Video", font=("Montserrat", 12, "bold"))
rs.pack(padx=1, pady=10, anchor=tk.CENTER)

options = ["Download 360p", "Download 720p", "Download 1080p"]
res_selection = customtkinter.CTkComboBox(master=app, values=options, width=160, height=34, font=("Montserrat Medium", 12), dropdown_font=("Montserrat Medium", 12), corner_radius=5, state="readonly", command = download_video, justify="center")
res_selection.pack(padx=10, pady=0, anchor=tk.CENTER)

# run app
app.mainloop() 