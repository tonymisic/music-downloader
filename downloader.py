# imports
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import os, urllib.request,subprocess, sys, tkinter.filedialog as fd, moviepy.editor as mp, time, glob, re
from tkinter import messagebox, Button, Entry, Label, Frame, Canvas, Listbox
from pytube import YouTube
from bs4 import BeautifulSoup
from threading import Thread

# global variables
directory = os.getcwd()
current_search = []
result_cap = 5
# main loop and settings
root = tk.Tk()
root.geometry("600x300")
root.title('MP3 Downloader')
# UI Components
searchbar = Entry(root, width="70", borderwidth=5, relief=tk.SUNKEN)
searchbar.grid(row=0, column=0, sticky=tk.W)
search_results = Listbox(root, width="70")
search_results.grid(row=1, column=0, sticky=tk.W, padx=(5,5))
label_currentDir = Label(root, text=directory)
label_currentDir.grid(row=5, column=0, columnspan=2, sticky=tk.W)
label_notification = Label(root, text="Welcome!")
label_notification.grid(row=1, column=1, sticky=tk.W)
label_current_results = Label(root, text="No Searches yet")
# functions
def set_folder():
    tempdir = fd.askdirectory(parent=root, title='Please select a directory')
    label_currentDir['text'] = tempdir
    directory = tempdir
    while tempdir == "":
        tempdir = fd.askdirectory(parent=root, title='Please select a directory')
        label_currentDir['text'] = tempdir
        directory = tempdir
def download():
    URL = ""
    try:
        URL = current_search[search_results.curselection()[0]]
        title = re.sub('\'','', search_results.get(search_results.curselection()[0]))
        label_notification['text'] = "Downloading..."
        YouTube(URL).streams.first().download(label_currentDir['text'])
        label_notification['text'] = "Converting to mp3..."
        clip = mp.VideoFileClip(label_currentDir['text'] + "/" + title + ".mp4")
        clip.audio.write_audiofile(label_currentDir['text'] + "/" + title + ".mp3")
        label_notification['text'] = "Done"
        if clip.audio and clip.audio.reader:
            clip.reader.close()
            clip.audio.reader.close_proc()
        os.remove(label_currentDir['text'] + "/" + title + ".mp4")
    except Exception as err:
        label_notification['text'] = "No URL found!"
        print(err)  
def find_video(term):
    if term != "":
        try:
            label_notification['text'] = "Searching..."
            label_current_results['text'] = ""
            current_search.clear()
            search_results.delete(0,tk.END)
            top_link = ""
            query = urllib.parse.quote(term)
            url = "https://www.youtube.com/results?search_query=" + query
            soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
            counter = 0
            for video in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                if counter >= result_cap:
                    break
                counter += 1
                URL = 'https://www.youtube.com' + video['href']
                current_search.append(URL)
                search_results.insert(tk.END, YouTube(URL).title)
            label_notification['text'] = "Results Found!"
        except:
            label_notification['text'] = "Error, try again."
    else:
        label_notification['text'] = "No term inputted."
# buttons
Button(root, text='Search', command=lambda : Thread(target = find_video, args = (searchbar.get(), )).start()).grid(row=0, column=1, sticky=tk.W)
Button(root, text='Download', command=lambda : Thread(target = download).start()).grid(row=3, column=0, sticky=tk.W, padx=(5,0), pady=(5,0))
Button(root, text='Set Folder', command=lambda : Thread(target = set_folder()).start()).grid(row=4, column=0, sticky=tk.W, padx=(5,0), pady=(5,0))
# Begin Executing
root.mainloop()


