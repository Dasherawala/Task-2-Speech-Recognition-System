import tkinter as tk
from tkinter import filedialog, messagebox, font
import speech_recognition as sr
from pydub import AudioSegment
import os

# Transcribe selected audio file
def transcribe_audio():
    recognizer = sr.Recognizer()
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.wav *.flac *.mp3")]
    )

    if not file_path:
        messagebox.showinfo("Cancelled", "No file selected.")
        return

    try:
        status_label.config(text="🔄 Processing...", fg="orange")

        # Convert mp3 to wav if necessary
        if file_path.lower().endswith(".mp3"):
            audio_mp3 = AudioSegment.from_mp3(file_path)
            temp_wav_path = "temp_audio.wav"
            audio_mp3.export(temp_wav_path, format="wav")
            file_path_to_use = temp_wav_path
        else:
            file_path_to_use = file_path

        with sr.AudioFile(file_path_to_use) as source:
            audio = recognizer.record(source)

        result = recognizer.recognize_google(audio)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result)
        status_label.config(text="✅ Transcription Complete", fg="lightgreen")

        # Clean up temporary file if created
        if file_path.lower().endswith(".mp3") and os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

    except sr.UnknownValueError:
        status_label.config(text="❌ Could not understand audio.", fg="red")
    except sr.RequestError as e:
        status_label.config(text=f"🚨 API Error: {e}", fg="red")
    except Exception as ex:
        status_label.config(text=f"⚠️ Error: {ex}", fg="red")

# Clear transcribed text
def clear_text():
    text_output.delete(1.0, tk.END)
    status_label.config(text="🧹 Text cleared", fg="lightblue")

# GUI setup
root = tk.Tk()
root.title("🎧 Speech Recognition System")
root.geometry("700x580")
root.configure(bg="#2e2e2e")  # dark gray background

# Fonts
bold_font = font.Font(weight="bold", size=10)
title_font = font.Font(size=16, weight="bold")

# Title
title_label = tk.Label(root, text="Import Audio Clip to Transcribe",
                       font=title_font, bg="#1f1f1f", fg="white", pady=10)
title_label.pack(pady=(20, 10), fill=tk.X)

# Import button
import_button = tk.Button(root, text="🎙️ Import Audio", command=transcribe_audio,
                          width=25, height=2, font=bold_font,
                          bg="#444", fg="white", activebackground="#555", relief="flat")
import_button.pack(pady=10)

# Output label
output_label = tk.Label(root, text="📝 Transcribed Text", font=("Poppins", 11, "bold"),
                        bg="#2e2e2e", fg="white")
output_label.pack(pady=(25, 5))

# Text box for transcription
text_output = tk.Text(root, height=12, width=70, font=bold_font,
                      bg="#1e1e1e", fg="white", insertbackground="white", bd=0)
text_output.pack(pady=5)

# Clear button
clear_button = tk.Button(root, text="🗑️ Clear Text", command=clear_text,
                         width=20, height=1, font=bold_font,
                         bg="#444", fg="white", activebackground="#555", relief="flat")
clear_button.pack(pady=(10, 20))

# Status label
status_label = tk.Label(root, text="", font=("Poppins", 10, "italic"),
                        fg="lightgreen", bg="#2e2e2e")
status_label.pack(pady=5)

root.mainloop()
