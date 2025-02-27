# Install dependencies:
# pip install yt_dlp tkinter customtkinter openai-whisper googletrans==4.0.0-rc1 edge-tts moviepy pydub  libretranslate

import os
import asyncio
import whisper
from googletrans import Translator
# from translate import Translator
from yt_dlp import YoutubeDL
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import tkinter
import customtkinter


# Function to download YouTube video
def start_download():
    try:
        ytLink = link.get()
        format_choice = format_var.get()
        quality_choice = quality_var.get()

        if format_choice == "MP3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality_choice,
                }],
            }
        elif format_choice == "MP4":
            if quality_choice == "Highest":
                format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif quality_choice == "720p":
                format_str = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best'
            elif quality_choice == "480p":
                format_str = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best'

            ydl_opts = {
                'format': format_str,
                'outtmpl': './downloads/downloadedYTvideo.mp4',
                'overwrites': True, 
                'restrictfilenames': True,
            }

        with YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([ytLink])
        status_label.configure(text="Download Complete!", text_color="green")
    except Exception as e:
        print(f"Error: {e}")
        status_label.configure(text=f"Error: {e}", text_color="red")


# TTS generation function
async def generate_tts(text, output_audio_file, voice):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_audio_file)


# Transcription function
def transcribe_video(video_file):
    print("Transcribing video...")
    model = whisper.load_model("base")
    result = model.transcribe(video_file)
    return result['segments']


# Translation function
def translate_segments(segments, dest_language):
    print(f"Translating text to {dest_language}...")
    translator = Translator()
    for segment in segments:
        translation = translator.translate(
            segment['text'],
            src='en',
            dest=dest_language
        )
        segment['translated_text'] = translation.text
    return segments


# Generate audio for translated text with timing alignment !!
async def generate_translated_audio(segments, voice):
    print("Generating audio with timestamp alignment...")
    audio_files = []
    for i, segment in enumerate(segments):
        # Generate TTS for the translated text
        output_audio_file = f"translated_audio_{i}.mp3"
        await generate_tts(segment['translated_text'], output_audio_file, voice)

        # Load the generated audio
        audio_segment = AudioSegment.from_file(output_audio_file)

        # Calculate duration of the original segment
        original_duration = (segment['end'] - segment['start']) * 1000  # Convert to milliseconds

        # Adjust the audio duration to match the original timing
        if len(audio_segment) < original_duration:
            # Add silence to extend the duration
            silence = AudioSegment.silent(duration=(original_duration - len(audio_segment)))
            audio_segment += silence
        elif len(audio_segment) > original_duration:
            # Trim the audio to match the duration
            audio_segment = audio_segment[:original_duration]

        # Export the adjusted audio
        adjusted_audio_file = f"adjusted_translated_audio_{i}.mp3"
        audio_segment.export(adjusted_audio_file, format="mp3")
        audio_files.append(adjusted_audio_file)

        # Clean up the intermediate TTS audio file
        os.remove(output_audio_file)

    return audio_files


# Merge audio with video using timestamps
def merge_audio_with_video(video_file, audio_files, segments, output_file):
    print("Merging audio with video...")
    combined_audio = AudioSegment.silent(duration=0)

    for i, (segment, audio_file) in enumerate(zip(segments, audio_files)):
        # Add silence before the segment starts
        if i == 0 and segment['start'] > 0:
            combined_audio += AudioSegment.silent(duration=segment['start'] * 1000)
        elif i > 0:
            gap = segment['start'] - segments[i - 1]['end']
            if gap > 0:
                combined_audio += AudioSegment.silent(duration=gap * 1000)

        # Add the translated audio segment
        audio_segment = AudioSegment.from_file(audio_file)
        combined_audio += audio_segment

    # Export the combined audio
    combined_audio_file = "combined_translated_audio.mp3"
    combined_audio.export(combined_audio_file, format="mp3")

    # Replace the original audio in the video with the combined translated audio
    video = VideoFileClip(video_file)
    translated_audio = AudioFileClip(combined_audio_file)
    final_video = video.set_audio(translated_audio)
    final_video.write_videofile(
        output_file,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    # Cleanup
    video.close()
    translated_audio.close()
    os.remove(combined_audio_file)
    for audio_file in audio_files:
        os.remove(audio_file)
        

# Main processing pipeline (TTS and translation)
async def process_video():
    try:
        # input_video = "./downloads/test_video.mp4"
        input_video = "./downloads/downloadedYTvideo.mp4"
        output_video = "./downloads/output_video.mp4"

        # Select language and voice
        language_choice = language_var.get()
        if language_choice == "French":
            dest_language = 'fr'
            voice = 'fr-FR-DeniseNeural'
        elif language_choice == "Russian":
            dest_language = 'ru'
            voice = 'ru-RU-SvetlanaNeural'
        else:
            status_label.configure(text="Invalid language selection!", text_color="red")
            return

        status_label.configure(text="Processing video...", text_color="blue")
        segments = transcribe_video(input_video)
        segments = translate_segments(segments, dest_language)
        audio_files = await generate_translated_audio(segments, voice)
        merge_audio_with_video(input_video, audio_files, segments, output_video)

        status_label.configure(text=f"Processing complete! Output saved to {output_video}", text_color="green")
    except Exception as e:
        print(f"Error: {e}")
        status_label.configure(text=f"Error: {e}", text_color="red")


# GUI setup
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x600")
app.title("YouTube Downloader & Translator")

# YouTube Downloader UI
title = customtkinter.CTkLabel(app, text="Insert a YouTube link")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Format selection
format_var = customtkinter.StringVar(value="MP4")
format_options = customtkinter.CTkOptionMenu(
    app,
    values=["MP3", "MP4"],
    variable=format_var
)
format_options.pack(padx=10, pady=10)

# Quality selection
quality_var = customtkinter.StringVar(value="Highest")  # default for MP4
quality_options = customtkinter.CTkOptionMenu(
    app,
    values=["128", "192", "256", "320"] if format_var.get() == "MP3" else ["480p", "720p", "Highest"],
    variable=quality_var
)
quality_options.pack(padx=10, pady=10)

# Update quality options
def update_quality_options(*args):
    if format_var.get() == "MP3":
        quality_options.configure(values=["128", "192", "256", "320"])
        quality_var.set("192")
    else:
        quality_options.configure(values=["480p", "720p", "Highest"])
        quality_var.set("Highest")

format_var.trace('w', update_quality_options)

download_button = customtkinter.CTkButton(app, text="Download", command=start_download)
download_button.pack(padx=10, pady=10)

# Language selection
language_var = customtkinter.StringVar(value="French")
language_label = customtkinter.CTkLabel(app, text="Select a language for translation:")
language_label.pack(padx=10, pady=10)
language_options = customtkinter.CTkOptionMenu(
    app,
    values=["French", "Russian"],
    variable=language_var
)
language_options.pack(padx=10, pady=10)

# Process button
process_button = customtkinter.CTkButton(app, text="Process Video", command=lambda: asyncio.run(process_video()))
process_button.pack(padx=10, pady=20)

# Status label
status_label = customtkinter.CTkLabel(app, text="")
status_label.pack(padx=10, pady=10)

# Run app
app.mainloop()