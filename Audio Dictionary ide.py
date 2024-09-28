import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from gtts import gTTS
from bs4 import BeautifulSoup
import requests
import json
import itertools

# Initial user data storage
user_data_file = "users.json"


# Function to save user data
def save_user_data(data):
    with open(user_data_file, 'w') as file:
        json.dump(data, file)


# Function to load user data
def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            return json.load(file)
    return {}


# Global variable to store the current logged-in user
current_user = None


# Function to fetch word definitions from the internet
def fetch_definition(word):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{word}"
    response = requests.get(url)
    data = response.json()

    if 'extract' in data:
        definition = data['extract']
        sentences = definition.split('. ')
        if len(sentences) > 1:
            return definition, f'Example sentence: {sentences[0]}.'
        else:
            return definition, "Example sentence not found."
    return "Definition not found online.", ""


# Function to create an audio file for a word, its meaning, and example sentence
def create_audio(word, meaning, example_sentence):
    tts = gTTS(text=f"{word}: {meaning}. {example_sentence}", lang='en')
    filename = f"{word}.mp3"
    tts.save(filename)
    return filename


# Function to play the audio of the word using a system command
def play_audio(filename):
    if os.path.exists(filename):
        # Use system command to play the audio file
        if os.name == 'nt':  # Windows
            subprocess.call(['start', filename], shell=True)
        else:  # MacOS or Linux
            subprocess.call(['open' if os.name == 'darwin' else 'xdg-open', filename])
    else:
        print(f"Audio file '{filename}' not found.")


# Function to process the word: fetch definition, create audio, and play it
def process_word():
    word = entry_word.get().strip()
    if word:
        meaning, example_sentence = fetch_definition(word)
        if meaning != "Definition not found online.":
            filename = create_audio(word, meaning, example_sentence)
            play_audio(filename)
            messagebox.showinfo("Success", f"Audio for the word '{word}' has been played.")
            save_searched_word(word, meaning, example_sentence)
        else:
            messagebox.showerror("Error", f"No definition found for '{word}'.")
    else:
        messagebox.showerror("Error", "Word field is required.")


# Function to save searched words
def save_searched_word(word, meaning, example_sentence):
    user_data = load_user_data()
    if current_user:
        user_list = user_data.get(current_user, {}).get("searched_words", {})
        if not isinstance(user_list, dict):
            user_list = {}  # Reset to an empty dictionary if the data format is corrupted
        user_list[word] = {"meaning": meaning, "example_sentence": example_sentence}
        user_data[current_user]["searched_words"] = user_list
        save_user_data(user_data)


# Function to show searched words
def show_searched_words():
    if current_user:
        user_data = load_user_data()
        searched_words = user_data.get(current_user, {}).get("searched_words", {})
        if not isinstance(searched_words, dict):
            messagebox.showerror("Error", "Saved searched words data is corrupted.")
            return
        words_text = "\n".join([f"{word}: {details['meaning'][:50]}... Example: {details['example_sentence']}"
                                for word, details in searched_words.items() if isinstance(details, dict)])
        messagebox.showinfo("Searched Words", words_text if words_text else "No searched words found.")


# Function to register a new user
def register_user():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if username and password:
        user_data = load_user_data()
        if username in user_data:
            messagebox.showerror("Error", "Username already exists!")
        else:
            user_data[username] = {"password": password, "searched_words": {}}
            save_user_data(user_data)
            messagebox.showinfo("Success", f"User '{username}' registered successfully!")
    else:
        messagebox.showerror("Error", "Both username and password are required.")


# Function to log in a user
def login_user():
    global current_user
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if username and password:
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            current_user = username
            messagebox.showinfo("Success", f"Welcome, {username}!")
            show_main_screen()
            entry_username.config(state='disabled')  # Disable username entry after logging in
            entry_username.delete(0, tk.END)
            entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Both username and password are required.")


# Function to log out a user
def logout_user():
    global current_user
    current_user = None
    entry_username.config(state='normal')  # Enable username entry for next login
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    frame_main.pack_forget()
    frame_login.pack(pady=10, padx=10, fill='x', expand=True)
    lbl_greeting.config(text=f"Welcome, User!")
    animate_greeting_label()


# Function to show the main screen after login
def show_main_screen():
    # Clear the login screen
    frame_login.pack_forget()
    # Show the main application screen
    frame_main.pack(pady=10, padx=10, fill='x', expand=True)
    lbl_greeting.config(text=f"Welcome, {current_user}!")
    animate_greeting_label()


# Function to animate the greeting label
def animate_greeting_label():
    colors = itertools.cycle(['red', 'green', 'blue', 'yellow', 'purple'])

    def change_color():
        lbl_greeting.config(fg=next(colors))
        root.after(500, change_color)

    change_color()


# Initialize the GUI
root = tk.Tk()
root.title("Audio Dictionary")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

# Create login frame
frame_login = tk.Frame(root, bg="#e1e1e1", padx=10, pady=10)
frame_login.pack(pady=10, padx=10, fill='x', expand=True)

lbl_username = tk.Label(frame_login, text="Username:", bg="#e1e1e1", font=("Helvetica", 12))
lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_username = ttk.Entry(frame_login, width=30, font=("Helvetica", 12))
entry_username.grid(row=0, column=1, padx=5, pady=5)

lbl_password = tk.Label(frame_login, text="Password:", bg="#e1e1e1", font=("Helvetica", 12))
lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_password = ttk.Entry(frame_login, width=30, font=("Helvetica", 12), show='*')
entry_password.grid(row=1, column=1, padx=5, pady=5)

btn_register = tk.Button(frame_login, text="Register", command=register_user, bg="#4CAF50", fg="white",
                         font=("Helvetica", 12))
btn_register.grid(row=2, column=0, pady=10, sticky="e")

btn_login = tk.Button(frame_login, text="Login", command=login_user, bg="#4CAF50", fg="white", font=("Helvetica", 12))
btn_login.grid(row=2, column=1, pady=10, sticky="w")

# Create main application frame (initially hidden)
frame_main = tk.Frame(root, bg="#e1e1e1", padx=10, pady=10)
frame_main.pack_forget()

# Add a title label at the top
title_label = tk.Label(root, text="Audio Dictionary", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Personalized greeting below the title label
lbl_greeting = tk.Label(root, text="Welcome, User!", font=("Helvetica", 14), bg="#f0f0f0", fg="#333")
lbl_greeting.pack(pady=5)

# Entry label and textbox for word in the main frame
lbl_word = tk.Label(frame_main, text="Word:", bg="#e1e1e1", font=("Helvetica", 12))
lbl_word.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_word = ttk.Entry(frame_main, width=30, font=("Helvetica", 12))
entry_word.grid(row=0, column=1, padx=5, pady=5)

# Button to process the word
btn_process_word = tk.Button(frame_main, text="Fetch & Play", command=process_word, bg="#4CAF50", fg="white",
                             font=("Helvetica", 12))
btn_process_word.grid(row=1, columnspan=2, pady=10)

# Button to show searched words
btn_show_words = tk.Button(frame_main, text="History", command=show_searched_words, bg="#4CAF50",
                           fg="white", font=("Helvetica", 12))
btn_show_words.grid(row=2, columnspan=2, pady=10)

# Button to log out
btn_logout = tk.Button(frame_main, text="Logout", command=logout_user, bg="#f44336", fg="white", font=("Helvetica", 12))
btn_logout.grid(row=3, columnspan=2, pady=10)

# Instruction label at the bottom of the window
lbl_instruction = tk.Label(root, text="Enter a Word to Fetch its Audio Definition", bg="#f0f0f0",
                           font=("Helvetica", 12))
lbl_instruction.pack(pady=5)

# Style configuration
style = ttk.Style()
style.configure("TLabel", background="#f0f0f0")
style.configure("TButton", padding=5, font=("Helvetica", 12), focuscolor="none")
style.configure("TEntry", padding=5, font=("Helvetica", 12))

# Start the greeting label animation
animate_greeting_label()

# Start the GUI event loop
root.mainloop()
