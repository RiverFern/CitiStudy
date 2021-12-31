from tkinter import PhotoImage

import fileParser
import userInterface
import loadData


def main():
    with open("questions.txt", encoding="utf-8") as rawQuestions:
        rawQuestionsList = rawQuestions.readlines()

    rawQuestions.close()

    questions = fileParser.parseFile(rawQuestionsList)

    try:
        data = loadData.readData()
        loadData.loadData(questions, data)
    except IOError as e:
        print("File does not exist ({})".format(e))

    root = userInterface.tk.Tk()
    root.geometry("1400x600")
    root.title("CitiStudy")
    app = userInterface.Application(questions, master=root)
    app.mainloop()


def on_delete():
    print("delete")


if __name__ == "__main__":
    main()
