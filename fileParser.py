import re


class Question:
    def __init__(self, prompt, category, subcategory):
        self.numCorrect = 0
        self.prompt = prompt
        self.category = category
        self.subcategory = subcategory


categoryRe = re.compile(r"^([A-Z]{3}[A-Z]+\s[A-Z]+)")
subcategoryRe = re.compile(r"^([A-Z]:)")
questionRe = re.compile(r"^([0-9]+\.)")
answerRe = re.compile(r"[^\s]")

questions = []

bonusQuestion = Question("0. Who is the coolest person ever?", "INTEGRATED CIVICS", "Holidays")
bonusQuestion.answer = "Fernando : )"
questions.append(bonusQuestion)


def parseFile(rawQuestionsList):
    for line in rawQuestionsList:
        categoryMatch = re.match(categoryRe, line)
        subcategoryMatch = re.match(subcategoryRe, line)
        questionMatch = re.match(questionRe, line)
        answerMatch = re.match(answerRe, line)
        if categoryMatch:
            category = categoryMatch[1]
        elif subcategoryMatch:
            subcategory = subcategoryMatch.string
            subcategory = subcategory.strip("\n")
        elif questionMatch:
            answers = []
            question = questionMatch.string
            question = question.strip('\n')
            questions.append(Question(question, category, subcategory))
        elif answerMatch:
            answer = answerMatch.string
            answer = answer.strip("\n")
            answers.append(answer)
            questions[len(questions) - 1].answer = answers

    return questions
