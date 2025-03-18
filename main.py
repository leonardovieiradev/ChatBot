import tkinter as tk
from tkinter import scrolledtext, PhotoImage, Canvas
from PIL import Image, ImageTk
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

model_name = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def send_message():
    texto_digitado = user_entry.get()
    if texto_digitado.strip() == "":
        return
    chat_history.insert(tk.END, f"Você: {texto_digitado}\n", "user")
    user_entry.delete(0, tk.END)

    input_processado = tokenizer(texto_digitado, return_tensors="pt")
    resposta_ids = model.generate(**input_processado, max_length=50)
    resposta_pronta = tokenizer.decode(resposta_ids[0], skip_special_tokens=True)

    chat_history.insert(tk.END, f"Bot: {resposta_pronta}\n", "bot")
    chat_history.yview(tk.END)


root = tk.Tk()
root.title("Chatbot Python")
root.geometry("600x700")

image = Image.open("background.png").convert("RGBA")
image = image.resize((600, 700), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(image)

canvas = Canvas(root, width=600, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

frame_chat = tk.Frame(root, bg="#1a1a1a", bd=2, relief=tk.FLAT)
frame_chat.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.6)

chat_history = scrolledtext.ScrolledText(frame_chat, wrap=tk.WORD, bg="#1a1a1a", fg="#0ff",
                                         font=("Arial", 12), padx=10, pady=10, borderwidth=0, relief=tk.FLAT,
                                         insertbackground="white")
chat_history.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
chat_history.tag_configure("user", foreground="#ff00ff", font=("Arial", 12, "bold"))
chat_history.tag_configure("bot", foreground="#00ff00", font=("Arial", 12))

frame_entry = tk.Frame(root, bg="#000000")
frame_entry.place(relx=0.05, rely=0.7, relwidth=0.9, relheight=0.1)

user_entry = tk.Entry(frame_entry, font=("Arial", 14), bg="#222", fg="#ffffff",
                      insertbackground="white", relief=tk.FLAT, bd=5)
user_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
user_entry.bind("<Return>", lambda event: send_message())

lista_de_cores = ["#ff0000", "#00ff00", "#0000ff", "#ff00ff", "#00ffff", "#ffff00"]


def animar_botao_rgb():
    cor_atual = lista_de_cores[animar_botao_rgb.index % len(lista_de_cores)]
    botaoRGB.config(bg=cor_atual)
    if animar_botao_rgb.index > 100:
        animar_botao_rgb.index = 0
    else:
        animar_botao_rgb.index += 1
    root.after(300, animar_botao_rgb)


animar_botao_rgb.index = 0

botaoRGB = tk.Button(frame_entry, text="Enviar", font=("Arial", 12, "bold"),
                     bg="#ff0000", fg="black", relief=tk.FLAT, bd=5,
                     activebackground="#5294e2", activeforeground="white", command=send_message)
botaoRGB.pack(side=tk.RIGHT, padx=5, pady=5)

cor_padrao = "#ff0000"
botaoRGB.config(bg=cor_padrao)

for i in range(3):
    cor_teste = lista_de_cores[i % len(lista_de_cores)]

animar_botao_rgb()

root.mainloop()