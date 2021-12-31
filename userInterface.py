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
        self.focusListBoxList = []
        self.correctListBoxList = []
        self.questions = questions
        self.master = master
        self.categoryText = tk.StringVar()
        self.subcategoryText = tk.StringVar()
        self.promptText = tk.StringVar()
        self.answersText = tk.StringVar()
        self.focusListBoxText = tk.StringVar()
        self.correctListBoxText = tk.StringVar()
        self.informationFrame = None
        self.resultButtonFrame = None
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.categoryText.set("CitiStudy 2021")

        # Set up Initial Frame for Questions (Left side)
        questionsFrame = tk.Frame(self.master, bg="gray", width=500)
        questionsFrame.pack(side="left", fill="both")
        questionsFrame.pack_propagate(0)

        # Set up the three Toggled frames for each major category
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

        # Set up focus Frame (Right Side)
        focusFrame = tk.Frame(self.master, bg="grey", width=250)
        focusFrame.pack(side="right", fill="both", expand="0")
        focusFrame.pack_propagate(0)

        # Create focusListBox
        focusListBoxFrame = tk.Frame(focusFrame)

        focusListBoxLabel = tk.Label(focusListBoxFrame, textvariable=self.focusListBoxText)
        focusListBoxLabel.pack(side="top", fill="x", expand=1, pady=2, padx=2, anchor="n")

        self.focusListBox = tk.Listbox(focusListBoxFrame, height=10, exportselection=True)
        xScrollbar = tk.Scrollbar(focusListBoxFrame, orient="horizontal")
        xScrollbar.pack(side="bottom", fill="x")
        yScrollbar = tk.Scrollbar(focusListBoxFrame)
        yScrollbar.pack(side="right", fill="y")
        self.focusListBox.config(xscrollcommand=xScrollbar.set, yscrollcommand=yScrollbar.set)
        yScrollbar.config(command=self.focusListBox.yview)
        xScrollbar.config(command=self.focusListBox.xview)
        self.focusListBox.bind('<<ListboxSelect>>', self.getSelection)
        self.focusListBox.pack(side="bottom", fill="x", expand=1, pady=2, padx=2, anchor="n")
        focusListBoxFrame.pack(fill="both")

        # Populate List Box from load data
        for question in self.questions:
            if question.numCorrect < 0:
                self.focusListBox.insert("end", question.prompt)
                self.focusListBoxList.append(question)

        self.focusListBoxText.set("Questions to Study: {}/100".format(len(self.focusListBoxList)))

        # Create correctListBox
        correctListBoxFrame = tk.Frame(focusFrame)

        correctListBoxLabel = tk.Label(correctListBoxFrame, textvariable=self.correctListBoxText)
        correctListBoxLabel.pack(side="top", fill="x", expand=1, pady=2, padx=2, anchor="n")

        self.correctListBox = tk.Listbox(correctListBoxFrame, height=10, exportselection=True)
        xScrollbar = tk.Scrollbar(correctListBoxFrame, orient="horizontal")
        xScrollbar.pack(side="bottom", fill="x")
        yScrollbar = tk.Scrollbar(correctListBoxFrame)
        yScrollbar.pack(side="right", fill="y")
        self.correctListBox.config(xscrollcommand=xScrollbar.set, yscrollcommand=yScrollbar.set)
        yScrollbar.config(command=self.correctListBox.yview)
        xScrollbar.config(command=self.focusListBox.xview)
        self.correctListBox.bind('<<ListboxSelect>>', self.getSelection)
        self.correctListBox.pack(side="bottom", fill="x", expand=1, pady=2, padx=2, anchor="n")
        correctListBoxFrame.pack(fill="both")

        loadButton = tk.Button(focusFrame, text="Load Progress", bg="#94F27F",
                               command=lambda: self.loadProgress())
        loadButton.pack(side="bottom", fill="x", expand=1, pady=2, padx=2, anchor="n")

        saveButton = tk.Button(focusFrame, text="Save Progress", bg="#94F27F",
                               command=lambda: self.saveProgress())
        saveButton.pack(side="bottom", fill="x", expand=0, pady=2, padx=2, anchor="n")

        # Populate correctListBox from load data
        for question in self.questions:
            if question.numCorrect > 0:
                self.correctListBox.insert("end", question.prompt)
                self.correctListBoxList.append(question)

        self.correctListBoxText.set("Questions to Study: {}/100".format(len(self.correctListBoxList)))

        # Set up Information Frame (Middle)
        self.informationFrame = tk.Frame(self.master, bg="white")
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

    def createQuestionsListBox(self, subFrame, subCategory):
        questionsListBoxFrame = tk.Frame(subFrame)
        questionsListBox = tk.Listbox(questionsListBoxFrame, height=10, exportselection=True)
        xScrollbar = tk.Scrollbar(questionsListBoxFrame, orient="horizontal")
        xScrollbar.pack(side="bottom", fill="x")
        yScrollbar = tk.Scrollbar(questionsListBoxFrame)
        yScrollbar.pack(side="right", fill="y")
        questionsListBox.config(xscrollcommand=xScrollbar.set, yscrollcommand=yScrollbar.set)
        for question in self.questions:
            if question.subcategory == subCategory:
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
        showAnswerButton = tk.Button(self.informationFrame, text="Show Answer",
                                     command=lambda: self.showAnswer(question))
        showAnswerButton.grid(row=3, column=0, sticky="w", padx=3, pady=3)
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

        if question.numCorrect > 0 and question.prompt in self.focusListBox.get(0, "end"):
            self.focusListBox.delete(self.focusListBox.get(0, "end").index(question.prompt))
            self.focusListBoxList.remove(question)

        self.focusListBoxText.set("Questions to Study: {}/100".format(len(self.focusListBoxList)))

        if question.numCorrect > 0 and question.prompt not in self.correctListBox.get(0, "end"):
            self.correctListBox.insert("end", question.prompt)
            self.correctListBoxList.append(question)

        self.correctListBoxText.set("Confident Questions: {}/100".format(len(self.correctListBoxList)))

    def incorrect(self, question):
        question.numCorrect -= 1
        print(question.numCorrect)
        print("incorrect", question.prompt)

        if question.numCorrect < 0 and question.prompt not in self.focusListBox.get(0, "end"):
            self.focusListBox.insert("end", question.prompt)
            self.focusListBoxList.append(question)

        self.focusListBoxText.set("Questions to Study: {}/100".format(len(self.focusListBoxList)))

        if question.numCorrect < 0 and question.prompt in self.correctListBox.get(0, "end"):
            self.correctListBox.delete(self.correctListBox.get(0, "end").index(question.prompt))
            self.correctListBoxList.remove(question)

        self.correctListBoxText.set("Confident Questions: {}/100".format(len(self.correctListBoxList)))

    def saveProgress(self):
        print("Save Progress")

        with open("CitiStudyProgress.txt", 'w+', encoding="utf-8") as progress:
            for question in self.focusListBoxList:
                data = "{} @{} \n".format(question.prompt, question.numCorrect)
                progress.write(data)
            for question in self.correctListBoxList:
                data = "{} @{} \n".format(question.prompt, question.numCorrect)
                progress.write(data)

        progress.close()

    def loadProgress(self):
        print("Load Progress")
