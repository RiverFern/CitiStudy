import re


def readData():
    numCorrectRe = re.compile(r"@(-?[0-9]+)")
    questionRe = re.compile(r"^([0-9]+)")

    with open("CitiStudyProgress.txt", "r", encoding="utf-8") as rawProgress:
        progress = rawProgress.readlines()


    rawProgress.close()

    data = []

    for line in progress:
        index = re.match(questionRe, line)
        numCorrect = re.search(numCorrectRe, line)
        questionData = (int(index[1]), int(numCorrect[1]))
        data.append(questionData)

    return data


def loadData(questions, data):
    for questionData in data:
        questions[questionData[0]].numCorrect = questionData[1]
