import tkinter as tk
from tkinter import Text
from PIL import Image, ImageTk
import json
import os
import subprocess
import sys

# Load artist info from temp file
artist_file = "data/current_artist.json"
if not os.path.exists(artist_file):
    raise FileNotFoundError("No artist info found. Please open from the music player.")

with open(artist_file, "r", encoding="utf-8") as f:
    artist = json.load(f)

window = tk.Tk()
window.title("Artist Profile")
window.geometry('565x600')
window.resizable(width=0, height=0)
window.eval('tk::PlaceWindow . center')
window.configure(border=10, relief="raised", bg="#23272a")  # dark grey

# Home button function
def return_home():
    window.destroy()
    if sys.platform.startswith("win"):
        subprocess.Popen(["python", "homepage.py"])
    else:
        subprocess.Popen(["python3", "homepage.py"])

# Home Button (top left)
home_button = tk.Button(window, text="Home", command=return_home, bg="#23272a", fg="#2ed8b6", font=("Segoe Script", 10, "bold"),
                        activebackground="#23272a", activeforeground="#2ed8b6", borderwidth=0)
home_button.place(x=10, y=10)

# Load images (fallback to default if not found)
def safe_photo(path, fallback="images/profilepicture.png"):
    try:
        img = Image.open(path)
    except Exception:
        img = Image.open(fallback)
    img = img.resize((200, 150), Image.LANCZOS)  # Force size to 200x150
    return ImageTk.PhotoImage(img)

Avatar = safe_photo(artist.get("image", "images/profilepicture.png"))
Spotify = ImageTk.PhotoImage(Image.open("images/app_images/spotifylogo.png"))
Youtube = ImageTk.PhotoImage(Image.open("images/app_images/youtubelogo.png"))
Instagram = ImageTk.PhotoImage(Image.open("images/app_images/instagramlogo.png"))

# Avatar Image
label1 = tk.Label(window, image=Avatar, bg="#23272a")
label1.place(x=150, y=0)
label1.image = Avatar  # keep reference


# Label of text box to display information about Artist
label4 = tk.Label(window, text="About The Artist", foreground="#2ed8b6", bg='#23272a', font=("Segoe Script", 10, "bold"))
label4.place(x=200, y=155)
# Text of Information
text1 = Text(window, width=40, height=10, bg="#23272a", fg="#b0bec5", insertbackground="#2ed8b6")
text1.place(x=100, y=175)
text1.insert("1.0", artist.get("bio", "No information available."))
text1.config(state="disabled")

# Social Media Handles
# Spotify
label6 = tk.Label(window, image=Spotify, bg="#23272a")
label6.place(x=130, y=400)
label6.image = Spotify
text2 = Text(window, width=25, height=1, bg="#23272a", fg="#2ed8b6", insertbackground="#2ed8b6")
text2.place(x=170, y=400)
text2.insert("1.0", artist.get("spotify", ""))
text2.config(state="disabled")
# Youtube
label7 = tk.Label(window, image=Youtube, bg="#23272a")
label7.place(x=130, y=440)
label7.image = Youtube
text3 = Text(window, width=25, height=1, bg="#23272a", fg="#2ed8b6", insertbackground="#2ed8b6")
text3.place(x=170, y=440)
text3.insert("1.0", artist.get("youtube", ""))
text3.config(state="disabled")
# Instagram
label8 = tk.Label(window, image=Instagram, bg="#23272a")
label8.place(x=130, y=480)
label8.image = Instagram
text4 = Text(window, width=25, height=1, bg="#23272a", fg="#2ed8b6", insertbackground="#2ed8b6")
text4.place(x=170, y=480)
text4.insert("1.0", artist.get("instagram", ""))
text4.config(state="disabled")

window.mainloop()