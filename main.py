import tkinter
import customtkinter
from pytube import YouTube

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
link = customtkinter.CTkEntry(app, width=350, height=40)

#run app
app.mainloop()