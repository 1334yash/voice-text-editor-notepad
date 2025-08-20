import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import threading

def new_file():
    text.delete(1.0, tk.END)

def open_file():
    file_path=filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0,tk.END)
            text.insert(tk.END, file.read())
def save_file():
    file_path= filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path,'w') as file:
            file.write(text.get(1.0,tk.END))
            messagebox.showinfo("Info","File saves successfully!")

def cut():
    text.event_generate("<<Cut>>")

def copy():
     text.event_generate("<<Copy>>")
def paste():
     text.event_generate("<<paste>>")

recognizer= sr.Recognizer()
mic=sr.Microphone()
listening= False

def voice_typing():
    global listening
    listening=True
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        text.insert(tk.END,"voice typing started...\n")

    while listening:
        try:
            with mic as source:
                audio= recognizer.listen(source)
                result= recognizer.recognize_google(audio,language='en-IN')
                text.insert(tk.END,result + " ")
                text.see(tk.END)

        except:
            text.insert(tk.END,"[Speech not recognized]")

def start_voice_typing():
    threading.Thread(target=voice_typing).start()

def stop_voice_typing():
    global listening
    listening=False
    text.insert(tk.END,"\nVoice typing stopped./n")

root = tk.Tk()
root.title(" voice Text Editor")
root.geometry("800x600")

text= tk.Text(root,wrap=tk.WORD,font=("Helvetica",12),fg="black")
text.pack(expand=tk.YES, fill=tk.BOTH)


menu= tk.Menu(root)
file_menu= tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)

edit_menu=tk.Menu(menu,tearoff=0)
edit_menu.add_command(label="Cut",command=cut)
edit_menu.add_command(label="Copy",command=copy)
edit_menu.add_command(label="Paste",command=paste)
menu.add_cascade(label="Edit",menu=edit_menu)

voice_menu= tk.Menu(menu,tearoff=0)
voice_menu.add_command(label="Start Voice Typing",command=start_voice_typing)
voice_menu.add_command(label="Stop Voice Typing",command=stop_voice_typing)
menu.add_cascade(label="Voice",menu=voice_menu)


root.config(menu=menu)

root.mainloop()