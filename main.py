from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
french_words_dict = {}

try:
    file_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    file_data = pandas.read_csv("./data/french_words.csv")
    french_words_dict = file_data.to_dict(orient="records")
else:
    french_words_dict = file_data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_words_dict)
    canvas1.itemconfig(canvas1_card, image=card_front)
    canvas1.itemconfig(canvas1_title, text='French', fill="black")
    canvas1.itemconfig(canvas1_word, text=f'{current_card["French"]}', fill="black")
    flip_timer = window.after(3000, func=flip_card)


def right_answer():
    global current_card, file_data
    french_words_dict.remove(current_card)
    next_card()
    data = pandas.DataFrame(french_words_dict)
    data.to_csv("./data/words_to_learn.csv", index=False)
    file_data = pandas.read_csv("./data/words_to_learn.csv")


def flip_card():
    canvas1.itemconfig(canvas1_card, image=card_back)
    canvas1.itemconfig(canvas1_title, text='English', fill="white")
    canvas1.itemconfig(canvas1_word, text=f'{current_card["English"]}', fill="white")


window = Tk()
# window.minsize(700, 600)
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# canvas 1
canvas1 = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas1_card = canvas1.create_image(400, 263, image=card_front)
canvas1_title = canvas1.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
canvas1_word = canvas1.create_text(400, 250, text="word", font=("Arial", 45, "bold"))
canvas1.grid(row=0, column=0, columnspan=2)

# canvas 2 - right
right_img = PhotoImage(file="./images/right.png")
right_btn = Button(width=100, height=100, bg=BACKGROUND_COLOR, highlightthickness=0, image=right_img, bd=0,
                   command=right_answer)
right_btn.grid(row=1, column=1, pady=5)

# canvas 3 - wrong
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(width=100, height=100, bg=BACKGROUND_COLOR, highlightthickness=0, image=wrong_img, bd=0,
                   command=next_card)
wrong_btn.grid(row=1, column=0, pady=5)

next_card()

window.mainloop()
