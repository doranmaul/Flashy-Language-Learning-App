from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
WIDTH = 800
HEIGHT = 526

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

#------------- Read data & create data frame/dictionary -------------#

try:
    read_csv = pandas.read_csv(filepath_or_buffer="../flash-card-project-start/data/words_to_learn.csv")
    lang_to_data_frame = pandas.DataFrame(read_csv)
    lang_dict = lang_to_data_frame.to_dict(orient="records")
    df_list = [list(row) for row in lang_to_data_frame.values]

except FileNotFoundError:
    read_csv = pandas.read_csv(filepath_or_buffer="../flash-card-project-start/data/french_words.csv")
    lang_to_data_frame = pandas.DataFrame(read_csv)
    lang_dict = lang_to_data_frame.to_dict(orient="records")
    df_list = [list(row) for row in lang_to_data_frame.values]

#------------- Flash card functionality -------------#

word = random.choice(lang_dict)
new_word = word["French"]
english_word = word["English"]


def random_word(button_pressed):
    global word
    global new_word
    global english_word
    word = random.choice(lang_dict)
    if button_pressed == "check":
        known_words(new_word, english_word)
    new_word = word["French"]
    canvas.itemconfig(canvas_image, image=front_card)
    canvas.delete("language")
    canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"), tags="language")
    canvas.delete("current_word")
    canvas.create_text(400, 263, text=new_word, font=("Ariel", 60, "bold"), tags="current_word")
    english_word = word["English"]
    window.after(ms=3000, func=flip_card)
    return word, new_word

# Right button


right_image = PhotoImage(file="../flash-card-project-start/images/right.png")
right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=lambda: random_word("check"))
right_button.grid(column=1, row=1)

# Wrong button

wrong_image = PhotoImage(file="../flash-card-project-start/images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=lambda: random_word("x"))
wrong_button.grid(column=0, row=1)


canvas = Canvas(width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="../flash-card-project-start/images/card_front.png")
canvas_image = canvas.create_image(WIDTH/2, HEIGHT/2, image=front_card, anchor="center")  # Easiest way to center image on canvas, w&h
canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"), tags="language")
canvas.create_text(400, 263, text=new_word, font=("Ariel", 60, "bold"), tags="current_word")
canvas.grid(column=0, row=0, columnspan=2)

back_card = PhotoImage(file="../flash-card-project-start/images/card_back.png")


def flip_card():
    global word, english_word
    #Change image, etc
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.delete("language")
    canvas.create_text(400, 150, text="English", font=("Ariel", 40, "italic"), tags="language", fill="white")
    canvas.delete("current_word")
    canvas.create_text(400, 263, text=english_word, font=("Ariel", 60, "bold"), tags="current_word", fill="white")
    return word, english_word


# ------------- Remove known words functionality -------------#

def known_words(french_word_known, english_word_known):
    new_list = [french_word_known, english_word_known]
    df_list.remove(new_list)
    new_data_frame = pandas.DataFrame(df_list)
    new_data_frame.to_csv("../flash-card-project-start/data/words_to_learn.csv", index=False, header=["French", "English"])

#Starts program with timer below


window.after(ms=3000, func=flip_card)

window.mainloop()
