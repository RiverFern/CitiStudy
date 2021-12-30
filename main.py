from tkinter import PhotoImage

import fileParser
import userInterface


def main():
    with open("questions.txt", encoding="utf-8") as rawQuestions:
        rawQuestionsList = rawQuestions.readlines()
    questions = fileParser.parseFile(rawQuestionsList)

    root = userInterface.tk.Tk()
    root.geometry("1400x600")
    root.title("CitiStudy")
    app = userInterface.Application(questions, master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
