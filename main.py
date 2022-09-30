from tkinter import *
import random
import pandas
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
timer = None

# Words
def right():
    word_pairs.remove(current_pair)
    new_word()

def new_word():
    global timer
    global current_pair
    window.after_cancel(timer)
    current_pair = random.choice(word_pairs)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(word, text=current_pair["French"])
    timer = window.after(3000, reveal_word)


def reveal_word():
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(word, text=current_pair["English"])


try:
    data_file = pandas.read_csv("data/words_to_learn.csv")
    word_pairs = data_file.to_dict(orient="records")
    current_pair = random.choice(word_pairs)
except FileNotFoundError:
    data_file = pandas.read_csv("data/french_words.csv")
    word_pairs = data_file.to_dict(orient="records")
    current_pair = random.choice(word_pairs)


#UI Layout
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"), fill="black")
word = canvas.create_text(400, 263, text=current_pair["French"], font=("Ariel", 60, "bold"), fill="black")
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
right_button = Button(image=right_image, bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR,
                      highlightthickness=0, command=right)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR,
                      highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)
timer = window.after(3000, reveal_word)

window.mainloop()

data_file = pd.DataFrame.from_dict(word_pairs)
data_file.to_csv("data/words_to_learn.csv", index=False)
