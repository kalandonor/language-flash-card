from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_TEXT_FONT = ("Arial", 40, "italic")  # 400, 150
WORD_TEXT_FONT = ("Arial", 60, "bold")  # 400, 263


class FlashCardUi(Tk):
    def __init__(self):
        super().__init__()
        try:
            database = pandas.read_csv("data/dutch_words.csv")
        except FileNotFoundError:
            database = pandas.read_csv("data/dutch_words_to_learn.csv")
        self.words = database.to_dict(orient="records")
        self.title = "Language learner"
        self.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
        self.foreground = PhotoImage(file="images/card_front.png")
        self.background = PhotoImage(file="images/card_back.png")
        self.flash_card = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.image_id = self.flash_card.create_image(400, 263, image=self.foreground)
        self.flash_card.grid(column=0, row=0, columnspan=2)
        self.language = self.flash_card.create_text(400, 150, font=LANGUAGE_TEXT_FONT, text="Language")
        self.word = self.flash_card.create_text(400, 263, font=WORD_TEXT_FONT, text="Word")
        self.check_image = PhotoImage(file="images/right.png")
        self.cross_image = PhotoImage(file="images/wrong.png")
        self.known_button = Button(image=self.check_image, highlightthickness=0, command=self.click_check)
        self.known_button.grid(column=1, row=1)
        self.unknown_button = Button(image=self.cross_image, highlightthickness=0, command=self.click_cross)
        self.unknown_button.grid(column=0, row=1)
        self.current_word = {}
        self.flip_timer = ""
        self.next_card()
        self.mainloop()

    def click_check(self):
        self.words.remove(self.current_word)
        data = pandas.DataFrame(data=self.words)
        data.to_csv("data/dutch_words_to_learn.csv", index=False)
        self.next_card()

    def click_cross(self):
        self.next_card()

    def next_card(self):
        if self.flip_timer:
            self.after_cancel(self.flip_timer)
        self.flash_card.itemconfig(self.image_id, image=self.foreground)
        self.current_word = random.choice(self.words)
        self.flash_card.itemconfig(self.language, text="Dutch", fill="Black")
        self.flash_card.itemconfig(self.word, text=f"{self.current_word.get('Dutch')}", fill="Black")
        self.flip_timer = self.after(3000, func=self.flip_card)

    def flip_card(self):
        self.flash_card.itemconfig(self.image_id, image=self.background)
        self.flash_card.itemconfig(self.language, text="English", fill="White")
        self.flash_card.itemconfig(self.word, text=self.current_word.get("English"), fill="White")


def main():
    fl_card = FlashCardUi()


if __name__ == "__main__":
    main()
