import tkinter as tk
from tkinter.ttk import Progressbar
import customtkinter as ctk
import pygame
from threading import Thread
import json
import sys
import subprocess
import platform
from PIL import Image, ImageTk  # Add this import

# --- Get genre from command line argument or default ---
if len(sys.argv) > 1:
    selected_genre = sys.argv[1]
else:
    selected_genre = "tereo"  # fallback genre

# --- Load music data from JSON ---
def load_music_data():
    with open('data/music_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)['genres']

music_data = load_music_data()
songs = music_data.get(selected_genre, [])
if not songs:
    tk.messagebox.showerror("Error", f"No songs found for genre: {selected_genre}")
    sys.exit()

current_song_index = 0  # Track the current song

# Initialize the window
ctk.set_appearance_mode("dark")
window = ctk.CTk(fg_color="#23272a")  # dark grey background
window.title("Music Page")
window.geometry('540x725')
window.resizable(width=0, height=0)
window.eval('tk::PlaceWindow . center')
pygame.mixer.init()
window.configure(border=10, relief="raised")

# Load images
def get_cover(index):
    try:
        img = Image.open(songs[index]['cover'])
        img = img.resize((486, 378), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        # fallback blank image of the same size
        img = Image.new('RGB', (486, 378), color='grey')
        return ImageTk.PhotoImage(img)

coverphoto = get_cover(current_song_index)
LeftArrow = tk.PhotoImage(file="images/app_images/button_leftarrow.png")
DownArrow = tk.PhotoImage(file="images/app_images/button_downarrow.png")
RightArrow = tk.PhotoImage(file="images/app_images/button_rightarrow.png")

# --- Song and artist labels ---
song_title_var = tk.StringVar()
artist_name_var = tk.StringVar()
def update_labels():
    song = songs[current_song_index]
    song_title_var.set(song.get('title', 'Unknown Title'))
    artist_name_var.set(song.get('artist', {}).get('name', 'Unknown Artist'))

# Functions for Play, Pause, and Song Navigation
def play_song():
    song = songs[current_song_index]
    pygame.mixer.music.load(song['file'])
    pygame.mixer.music.play()
    update_cover()
    update_labels()
    threading_progress_bar()

def pause_song():
    pygame.mixer.music.pause()

def unpause_song():
    pygame.mixer.music.unpause()

def next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    play_song()

def previous_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    play_song()

def threading_progress_bar():
    t1 = Thread(target=update_progress_bar)
    t1.start()

def update_progress_bar():
    song = songs[current_song_index]
    sound = pygame.mixer.Sound(song['file'])
    duration = sound.get_length()
    def update_progress(i):
        if i < int(duration):
            progress_bar.set(i / duration)
            window.after(1000, update_progress, i + 1)
    update_progress(0)

def set_volume(value):
    pygame.mixer.music.set_volume(float(value))

def update_cover():
    # Update the displayed cover image when the song changes
    global coverphoto
    coverphoto = get_cover(current_song_index)
    label1.configure(image=coverphoto)
    label1.image = coverphoto  # Keep a reference to avoid garbage collection

def show_artist_info():
    # Save the current song's artist info to a JSON file and open the artist profile window
    artist = songs[current_song_index].get("artist", {})
    with open("data/current_artist.json", "w", encoding="utf-8") as f:
        json.dump(artist, f)
    # Launch the artist profile page as a new process
    if platform.system() == "Windows":
        subprocess.Popen(["python", "artistprofile.py"])
    else:
        subprocess.Popen(["python3", "artistprofile.py"])

def return_home():
    # Close the music player window and return to the homepage
    window.destroy()
    if sys.platform.startswith("win"):
        subprocess.Popen(["python", "homepage.py"])
    else:
        subprocess.Popen(["python3", "homepage.py"])

# --- UI Layout ---
home_button = tk.Button(
    window, text="Home", command=return_home,
    bg="#23272a", fg="#2ed8b6", font=("Segoe Script", 10, "bold"),
    activebackground="#23272a", activeforeground="#2ed8b6", borderwidth=0
)
home_button.place(x=10, y=10)

label1 = tk.Label(window, image=coverphoto, bg="#23272a")
label1.place(x=115, y=55)

song_title_label = tk.Label(
    window, textvariable=song_title_var,
    font=("Segoe Script", 14, "bold"), bg='#23272a', fg="#2ed8b6"
)
song_title_label.place(x=75, y=350)
artist_name_label = tk.Label(
    window, textvariable=artist_name_var,
    font=("Segoe Script", 12), bg='#23272a', fg="#b0bec5"  # light grey
)
artist_name_label.place(x=75, y=380)
update_labels()

button1 = tk.Button(window, image=LeftArrow, command=previous_song, bg="#23272a", activebackground="#23272a", borderwidth=0)
button1.place(x=70, y=450)
label2 = tk.Label(window, text="Previous Song", foreground="#2ed8b6", bg='#23272a', font=("Segoe Script", 10, "bold"))
label2.place(x=100, y=530)

button2 = tk.Button(window, image=DownArrow, command=show_artist_info, bg="#23272a", activebackground="#23272a", borderwidth=0)
button2.place(x=260, y=450)
label3 = tk.Label(window, text="See More Information", foreground="#b0bec5", bg='#23272a', font=("Segoe Script", 10, "bold"))
label3.place(x=270, y=530)

button3 = tk.Button(window, image=RightArrow, command=next_song, bg="#23272a", activebackground="#23272a", borderwidth=0)
button3.place(x=450, y=450)
label4 = tk.Label(window, text="Next Song", foreground="#2ed8b6", bg='#23272a', font=("Segoe Script", 10, "bold"))
label4.place(x=480, y=530)

play_button = tk.Button(window, text="Play", command=play_song, bg="#23272a", fg="#2ed8b6", font=("Segoe Script", 10, "bold"),
                        activebackground="#23272a", activeforeground="#b0bec5", borderwidth=2, highlightbackground="#2ed8b6")
play_button.place(x=225, y=585)

pause_button = tk.Button(window, text="Pause", command=pause_song, bg="#23272a", fg="#b0bec5", font=("Segoe Script", 10, "bold"),
                         activebackground="#23272a", activeforeground="#2ed8b6", borderwidth=2, highlightbackground="#b0bec5")
pause_button.place(x=325, y=585)

unpause_button = tk.Button(window, text="Unpause", command=unpause_song, bg="#23272a", fg="#2ed8b6", font=("Segoe Script", 10, "bold"),
                           activebackground="#23272a", activeforeground="#b0bec5", borderwidth=2, highlightbackground="#2ed8b6")
unpause_button.place(x=425, y=585)

progress_bar = ctk.CTkProgressBar(window, progress_color="#2ed8b6", width=400, fg_color="#23272a")
progress_bar.place(x=75, y=600)

volume_slider = ctk.CTkSlider(window, from_=0, to=1, command=set_volume, width=300,
                              progress_color="#2ed8b6", button_color="#b0bec5", fg_color="#23272a")
volume_slider.place(x=135, y=650)

# Start with first song loaded and playing when the window opens
play_song()

# Start the Tkinter event loop to keep the window open and responsive
window.mainloop()