import re
import tkinter as tk
from tkinter import ttk

subcategories = [["A: Principles of American Democracy", "B: System of Government", "C: Rights and Responsibilities"],
                 ["A: Colonial Period and Independence", "B: 1800s",
                  "C: Recent American History and Other Important Historical Information"],
                 ["A: Geography", "B: Symbols", "C: Holidays"]]


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                             variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')


class Application(tk.Frame):
    def __init__(self, questions, master=None):
        super().__init__(master)
        self.questions = questions
        self.master = master
        self.categoryText = tk.StringVar()
        self.subcategoryText = tk.StringVar()
        self.promptText = tk.StringVar()
        self.answersText = tk.StringVar()
        self.showAnswerButton = None
        self.informationFrame = None
        self.resultButtonFrame = None
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        questionsFrame = tk.Frame(self.master, bg="gray", width=500)
        questionsFrame.pack(side="left", fill="both")
        questionsFrame.pack_propagate(0)

        cat1 = ToggledFrame(questionsFrame, text='AMERICAN GOVERNMENT', relief="raised", borderwidth=1)
        cat1.pack(fill="x", expand=0, pady=2, padx=2, anchor="n")
        for subcategory in subcategories[0]:
            subcat = ToggledFrame(cat1.sub_frame, text=subcategory, relief="raised", borderwidth=1)
            subcat.pack(fill="x", expand=1, pady=2, padx=2)
            self.createQuestionsListBox(subcat.sub_frame, subcategory)

        cat2 = ToggledFrame(questionsFrame, text='AMERICAN HISTORY', relief="raised", borderwidth=1)
        cat2.pack(fill="x", expand=0, pady=2, padx=2, anchor="n")
        for subcategory in subcategories[1]:
            subcat = ToggledFrame(cat2.sub_frame, text=subcategory, relief="raised", borderwidth=1)
            subcat.pack(fill="x", expand=1, pady=2, padx=2)
            self.createQuestionsListBox(subcat.sub_frame, subcategory)

        cat3 = ToggledFrame(questionsFrame, text='INTEGRATED CIVICS', relief="raised", borderwidth=1)
        cat3.pack(fill="x", expand=0, pady=2, padx=2, anchor="n")
        for subcategory in subcategories[2]:
            subcat = ToggledFrame(cat3.sub_frame, text=subcategory, relief="raised", borderwidth=1)
            subcat.pack(fill="x", expand=1, pady=2, padx=2)
            self.createQuestionsListBox(subcat.sub_frame, subcategory)

        self.informationFrame = tk.Frame(self.master, bg="white", width=600)
        self.informationFrame.pack(side="right", fill="both", expand="1")
        self.informationFrame.pack_propagate(0)

        categoryLabel = tk.Label(self.informationFrame, textvariable=self.categoryText, font=("Arial", 20), bg="white")
        categoryLabel.grid(row=0, column=0, sticky="w", padx=3, pady=3)
        categoryLabel.propagate(0)

        subcategoryLabel = tk.Label(self.informationFrame, textvariable=self.subcategoryText, font=("Arial", 15),
                                    bg="white")
        subcategoryLabel.grid(row=1, column=0, sticky="w", padx=3, pady=3)
        subcategoryLabel.propagate(0)

        prompLabel = tk.Label(self.informationFrame, textvariable=self.promptText, font=("Arial", 10), bg="white")
        prompLabel.grid(row=2, column=0, sticky="w", padx=3, pady=3)
        prompLabel.propagate(0)

        answerLabel = tk.Label(self.informationFrame, textvariable=self.answersText, font=("Arial", 10), bg="white",
                               justify="left")
        answerLabel.grid(row=4, column=0, sticky="w", padx=3, pady=3)
        answerLabel.propagate(0)

        self.resultButtonFrame = tk.Frame(self.informationFrame, bg="white")
        self.resultButtonFrame.grid(row=5, column=0, sticky="w")

    def createQuestionsListBox(self, sub_frame, subcategory):
        questionsListBoxFrame = tk.Frame(sub_frame)
        questionsListBox = tk.Listbox(questionsListBoxFrame, height=10, exportselection=True)
        xScrollbar = tk.Scrollbar(questionsListBoxFrame, orient="horizontal")
        xScrollbar.pack(side="bottom", fill="x")
        yScrollbar = tk.Scrollbar(questionsListBoxFrame)
        yScrollbar.pack(side="right", fill="y")
        questionsListBox.config(xscrollcommand=xScrollbar.set, yscrollcommand=yScrollbar.set)
        for question in self.questions:
            if question.subcategory == subcategory:
                questionsListBox.insert("end", question.prompt)
                questionsListBox.pack(side="top", fill="x", expand=1, pady=2, padx=2)
                questionsListBox.bind('<<ListboxSelect>>', self.getSelection)
        yScrollbar.config(command=questionsListBox.yview)
        xScrollbar.config(command=questionsListBox.xview)
        questionsListBoxFrame.pack(fill="both")

    def getSelection(self, event):
        getNumberRe = re.compile(r"^([0-9]+)\.")
        selection = event.widget.curselection()
        if selection:
            value = event.widget.get(selection[0])
            value = value.strip("\n")
            match = re.search(getNumberRe, value)
            if match:
                questionIndex = int(match[1])
                self.displayQuestion(self.questions[questionIndex])

    def displayQuestion(self, question):
        self.answersText.set("")
        self.categoryText.set(question.category)
        self.subcategoryText.set(question.subcategory)
        self.promptText.set(question.prompt)
        correctButton = tk.Button(self.resultButtonFrame, text="Correct", bg="#94F27F",
                                  command=lambda: self.correct(question))
        incorrectButton = tk.Button(self.resultButtonFrame, text="Incorrect", bg="#F76868",
                                    command=lambda: self.incorrect(question))
        self.showAnswerButton = tk.Button(self.informationFrame, text="Show Answer",
                                          command=lambda: self.showAnswer(question))
        self.showAnswerButton.grid(row=3, column=0, sticky="w", padx=3, pady=3)
        correctButton.grid(row=0, column=0, sticky="w", padx=3, pady=3)
        incorrectButton.grid(row=0, column=1, sticky="w", padx=3, pady=3)

    def showAnswer(self, question):
        answerString = "\n"
        answerString = answerString.join(question.answer)
        self.answersText.set(answerString)

    def correct(self, question):
        question.numCorrect += 1
        print(question.numCorrect)
        print("correct ", question.prompt)

    def incorrect(self, question):
        print("incorrect", question.prompt)
