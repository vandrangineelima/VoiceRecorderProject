import tkinter as interface
import sounddevice as sound_util
import numpy as data_handler
import threading as bg_process
import time as clock
import os
from scipy.io.wavfile import write as audio_writer, read as audio_reader

# Shared data and state variables
buffer_audio = None
is_recording_ongoing = False
record_list = []
current_file_index = 1
is_timer_active = False
elapsed_seconds = 0

# Start Recording Function
def initiate_recording():
    global buffer_audio, is_recording_ongoing, is_timer_active, elapsed_seconds

    sample_rate = 44100  # Standard audio sample rate
    max_duration_limit = 300  # Limit to 5 minutes of recording time

    is_recording_ongoing = True
    is_timer_active = True
    elapsed_seconds = 0
    audio_display_list.delete(0, interface.END)
    update_audio_file_list()

    status_text.config(text="Recording... 🎙️")
    start_timer()

    buffer_audio = sound_util.rec(int(max_duration_limit * sample_rate), samplerate=sample_rate, channels=2)
    start_record_button.config(state=interface.DISABLED)
    stop_record_button.config(state=interface.NORMAL)

# Stop Recording Function
def stop_recording():
    global is_recording_ongoing, is_timer_active, current_file_index

    if is_recording_ongoing:
        is_recording_ongoing = False
        is_timer_active = False
        sound_util.stop()

        filename = f"audio_clip_{current_file_index}.wav"
        audio_writer(filename, 44100, buffer_audio[:int(elapsed_seconds * 44100)])

        record_list.append(filename)
        current_file_index += 1

        update_audio_file_list()
        status_text.config(text=f"Recording saved as {filename}")
        start_record_button.config(state=interface.NORMAL)
        stop_record_button.config(state=interface.DISABLED)
        timer_display.config(text="Time Elapsed: 0 sec")

# Timer Logic
def start_timer():
    def update_time_display():
        if is_timer_active:
            global elapsed_seconds
            elapsed_seconds += 1
            timer_display.config(text=f"Time Elapsed: {elapsed_seconds} sec")
            root.after(1000, update_time_display)
    update_time_display()

# Refresh the Audio File List
def update_audio_file_list():
    audio_display_list.delete(0, interface.END)
    for record in record_list:
        audio_display_list.insert(interface.END, record)
    audio_display_list.yview(interface.END)

# Play Audio Function
def play_audio_clip():
    selected_item = audio_display_list.curselection()
    if selected_item:
        filename = audio_display_list.get(selected_item[0])
        if os.path.exists(filename):
            status_text.config(text=f"Playing {filename} ▶️")

            def play_audio_in_background():
                sample_rate, audio_data = audio_reader(filename)
                sound_util.play(audio_data, sample_rate)
                sound_util.wait()
                status_text.config(text="Ready")

            bg_process.Thread(target=play_audio_in_background).start()
        else:
            status_text.config(text="File not found ❌")

# GUI Components
root = interface.Tk()
root.title("Voice Recorder Application 🎙️")
root.geometry("450x550")
root.resizable(False, False)

start_record_button = interface.Button(root, text="Start Recording", command=initiate_recording, bg="green", fg="white", height=2, width=20)
start_record_button.pack(pady=15)

stop_record_button = interface.Button(root, text="Stop Recording", command=stop_recording, bg="red", fg="white", height=2, width=20)
stop_record_button.pack(pady=15)
stop_record_button.config(state=interface.DISABLED)

play_audio_button = interface.Button(root, text="Play Selected Clip", command=play_audio_clip, bg="blue", fg="white", height=2, width=25)
play_audio_button.pack(pady=15)

status_text = interface.Label(root, text="Status: Ready", font=("Arial", 12))
status_text.pack(pady=15)

timer_display = interface.Label(root, text="Time Elapsed: 0 sec", font=("Arial", 12))
timer_display.pack(pady=15)

audio_display_list = interface.Listbox(root, width=45, height=10)
audio_display_list.pack(pady=15)

root.mainloop()