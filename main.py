import tkinter
import customtkinter
from yt_dlp import YoutubeDL


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
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            
        with YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([ytLink])
        print("Download Complete")
    except Exception as e:
        print(f"Error: {e}")
        
    

#sys settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Tube DL")

# UI
title = customtkinter.CTkLabel(app, text="insert a youtube link")
title.pack(padx=10,pady=10)

# link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()


# Format selection
format_var = customtkinter.StringVar(value="MP3")
format_options = customtkinter.CTkOptionMenu(
    app,
    values=["MP3", "MP4"],
    variable=format_var
)
format_options.pack(padx=10, pady=10)

# Quality selection
quality_var = customtkinter.StringVar(value="192")  # default for MP3
quality_options = customtkinter.CTkOptionMenu(
    app,
    values=["128", "192", "256", "320"] if format_var.get() == "MP3" else ["480p", "720p", "Highest"],
    variable=quality_var
)
quality_options.pack(padx=10, pady=10)

# Function to update quality options based on format selection
def update_quality_options(*args):
    if format_var.get() == "MP3":
        quality_options.configure(values=["128", "192", "256", "320"])
        quality_var.set("192")
    else:
        quality_options.configure(values=["480p", "720p", "Highest"])
        quality_var.set("720p")

# Bind the format selection to update quality options
format_var.trace('w', update_quality_options)

#DL button
download = customtkinter.CTkButton(app, text="Download", command=start_download)
download.pack(padx=10,pady=10)

# Status label
status_label = customtkinter.CTkLabel(app, text="")
status_label.pack(padx=10, pady=10)

#run app
app.mainloop()