from openai import OpenAI
import config
client = OpenAI(api_key=config.API_KEY)
import docx
import tkinter as tk
from tkinter import filedialog



root = tk.Tk()
root.title("Text Translator")
root.configure(bg="white")

file_location = None


def browse_file():
    global file_location
    file_location = filedialog.askopenfilename(initialdir="/",
                                               title="Select file",
                                               filetypes=(("Word files", "*.docx"), ("all files", "*.*")))
    if file_location:
        text_field.delete("1.0", tk.END)
        text_field.insert(tk.END, "File selected. Now choose the target language and click 'Translate'.")


def translate_text():
    global file_location
    if file_location:
        target_language = language_var.get()
        doc = docx.Document(file_location)
        text = ""
        for para in doc.paragraphs:
            text += para.text

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": "You are a professional language translator. "
                        "Below I will ask you to translate text. "
                        "I expect from you to give me the correct translation. "
                        "Can you help me with that?"},
            {"role": "assistant", "content": "Yes, I can help you with that."},
            {"role": "user",
             "content": f"Translate the following text into {target_language}: {text}"}
        ])
        translated_text = response.choices[0].message.content.strip()
        text_field.delete("1.0", tk.END)
        text_field.insert(tk.END, translated_text)


header_font = ("Open Sans", 16, "bold")

header = tk.Label(root, text="Text Translator", bg="white", font=header_font)
header.grid(row=0, column=0, columnspan=2, pady=20)

source_label = tk.Label(root, text="Source File", bg="white", font=("Arial", 12))
source_label.grid(row=1, column=0, padx=20, pady=5)

browse_button = tk.Button(root, text="Browse", bg="#4267B2", fg="black", relief="flat", borderwidth=0,
                          activebackground="#4267B2", activeforeground="white", command=browse_file)
browse_button.config(font=("Arial", 12, "bold"), width=10, height=2)
browse_button.grid(row=2, column=0, padx=20, pady=5)

target_language_label = tk.Label(root, text="Target Language", bg="white", font=("Arial", 12))
target_language_label.grid(row=1, column=1, padx=20, pady=5)

languages = ["Gujarati", "Hindi", "Spanish", "French"]
language_var = tk.StringVar(root)
language_var.set(languages[0])
language_menu = tk.OptionMenu(root, language_var, *languages)
language_menu.config(font=("Arial", 12), width=10)
language_menu.grid(row=2, column=1, padx=20, pady=5)

translate_button = tk.Button(root, text="Translate", bg="#34A853", fg="black", relief="flat", borderwidth=0,
                             activebackground="#34A853", activeforeground="white", command=translate_text)
translate_button.config(font=("Arial", 12, "bold"), width=10, height=2)
translate_button.grid(row=3, column=0, columnspan=2, pady=10)

text_field = tk.Text(root, height=20, width=50, bg="white", fg="black", relief="flat", borderwidth=0, wrap="word")
text_field.grid(row=4, column=0, columnspan=2, padx=20, pady=20)
text_field.grid_rowconfigure(0, weight=1)
text_field.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
