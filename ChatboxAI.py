
from textblob import TextBlob
from operator import itemgetter

# def basicChatBot(msg, FAQList):
#     response = ''
#     for qa in FAQList:  # Example code
#         question = qa.split('?')[0]  # Example code
#         answer = qa.split('?')[1]  # Example code
#         if question == msg:
#             response = answer
#     return response;

def CBRChatBot(msg, FAQPathFilename):
    printToWindow = False
    response = ''

    answerList, questionList = ReadFAQFile(FAQPathFilename) # read the FAQ
    wordTupList = RelevantWordTuples(questionList, printToWindow) # extract to tuples <word, answerID, score>
    uniqueWordsList = FindUniqueWords(wordTupList, printToWindow) # find unique words
    uniqueWordSums = ScoreUniqueWords(wordTupList, uniqueWordsList, printToWindow) # <word, SUM(score)>

    newMsg = ExtractUnnecessaryWords(TextBlob(msg)) # remove unnecessary words from the message

    answerTups = RelevantAnswerTuples(newMsg, uniqueWordSums, wordTupList, printToWindow) # find all questions with
                            #... words that match a word in the message. Return tuples <AnswerID, score, sum(scores)>
    uniqueAnswerList = ListUniqueAnswers(answerTups, printToWindow) # List unique answers relevant to the message
    uniqueAnswerScores = ScoreEachAnswer(answerTups, uniqueAnswerList, printToWindow) # Find the score for each answer

    scoreThreshold = .5
    response = ReturnBestResponse(answerList, response, scoreThreshold, uniqueAnswerScores, printToWindow) #return best response

    return response;


def ReturnBestResponse(answerList, response, scoreThreshold, uniqueAnswerScores, printToWindow):
    # This method identifies the highest scoring response and returns it
    # Return the best scoring response
    bestAnswerID, bestAnswerScore = max(uniqueAnswerScores, key=itemgetter(1))
    if printToWindow:
        print("bestAnswerScore = " + str(bestAnswerScore))

    # Sort the responses and select the ones with the highest two scores
    topUniqueAnswerSums = tuple(sorted(uniqueAnswerScores, key=itemgetter(1), reverse=True)[:2])
    if printToWindow:
        print("topUniqueAnswerSums = " + str(topUniqueAnswerSums))

    topTwoScoreThreshold = -1
    topTwoScoreDifference = 0
    # Calculate the difference between the 1st and 2nd highest scores
    if len(topUniqueAnswerSums) > 1:
        if printToWindow:
            print("bestAnswerScore - topUniqueAnswerSums[1][1] = " + bestAnswerScore - topUniqueAnswerSums[1][1])
        topTwoScoreDifference = bestAnswerScore - topUniqueAnswerSums[1][1]
        topTwoScoreThreshold = 0

    # To be returned, a response must exceed the "scoreThreshold" and must differ from the 2nd highest scoring response
    if bestAnswerScore >= scoreThreshold and topTwoScoreDifference > topTwoScoreThreshold:
        response = answerList[bestAnswerID]
    return response


def ScoreEachAnswer(answerTups, uniqueAnswerList, printToWindow):
    # This method finds the normalized score associated with each answer
    uniqueAnswerSums = []
    for answers in uniqueAnswerList:
        answerSum = 0
        for tuples in answerTups:
            if tuples[0] == answers:
                currentAnswerSum = float(tuples[1]) / float(tuples[2])
                if printToWindow:
                    print(
                        str(answers) + " => " + str(tuples[1]) + " / " + str(tuples[2]) + " = " + str(currentAnswerSum))
                answerSum += currentAnswerSum
        uniqueAnswerSums.append((answers, answerSum))
    if printToWindow:
        print("uniqueAnswerSums = " + str(uniqueAnswerSums))
    return uniqueAnswerSums


def ListUniqueAnswers(answerTups, printToWindow):
    # This method lists all unique answers relevant to the input message
    uniqueAnswerList = []
    for tuples in answerTups:
        answer = tuples[0]
        if answer not in uniqueAnswerList:
            uniqueAnswerList.append(answer)
    if printToWindow:
        print("Unique Answers: " + str(uniqueAnswerList))
    return uniqueAnswerList


def RelevantAnswerTuples(newMsg, uniqueWordSums, wordTupList, printToWindow):
    # This method finds all questions with words that match a word in the message.
    # Return tuples <AnswerID, score, sum(scores)>
    answerTups = []
    for words in newMsg.words:
        if printToWindow:
            print("Input word: " + words)
        for tuples in wordTupList:
            if tuples[0].lower() == words.lower():
                for uniqueWordTuples in uniqueWordSums:
                    if uniqueWordTuples[0].lower() == words.lower():
                        wordLikelihood = uniqueWordTuples[1]
                if printToWindow:
                    print("word, answer, and scores: " + str(tuples))
                answerTups.append((tuples[1], str(tuples[2]), wordLikelihood))
    if printToWindow:
        print("Answers, scores, and likelihood modifiers, for all words: " + str(answerTups))
    return answerTups


def ExtractUnnecessaryWords(setOfWords):
    # This method extracts unnecessary words from an input set and returns the remaining words as a TextBlob object
    extraWords = [word for word, tag in setOfWords.tags if tag in ('DT')]
    newSetOfWords = ' '
    sub_stopwords = set(setOfWords.words) - set(extraWords)
    for word in sub_stopwords:
        newSetOfWords = word + ' ' + newSetOfWords
    newSetOfWords = TextBlob(newSetOfWords)
    return newSetOfWords


def ScoreUniqueWords(wordTupList, uniqueWordsList, printToWindow):
    # This method returns a tuple containing:
    #   <the word>,
    #   <the sum of the word's relative importance across all questions> (this value will be used to normalize words)
    # A low total score means that the word appears very infrequently. A high total score means that the word is common

    uniqueWordSums = []
    for words in uniqueWordsList:
        wordSum = 0
        for tuples in wordTupList:
            if tuples[0].lower() == words:
                wordSum += tuples[2]
        uniqueWordSums.append((words, wordSum))
    if printToWindow:
        print(uniqueWordSums)
    return uniqueWordSums


def RelevantWordTuples(questionList, printToWindow):
    # This method creates a tuple for each relevant word in each question
    # The tuples take the form: (
    #   <relevant word>,
    #   <question/answer number>, (so the answer can be found in the AnswerList)
    #   <relative word importance in the question> (1/the number of relevant words in the question)
    i = 0
    wordTupList = []
    for que in questionList:
        newQue = ExtractUnnecessaryWords(que)

        if printToWindow:
            print(que)
            print(len(que.words))
            print(newQue.words)
            print(len(newQue.words))

        for words in newQue.words:
            # wordTup = (words, answerList[i], 1/len(newQue.words)) # answers are hardcoded
            wordTup = (words, i, 1 / len(newQue.words))  # answer keys are hardcoded
            wordTupList.append(wordTup)
            if printToWindow:
                print(wordTup)
        i += 1
    return wordTupList


def FindUniqueWords(wordTupList, printToWindow):
    # This method identifies the unique words in the list of question
    uniqueWordsList = []
    for tuples in wordTupList:
        words = tuples[0].lower()
        if words not in uniqueWordsList:
            uniqueWordsList.append(words)
    if printToWindow:
        print("Unique Words: " + uniqueWordsList)
    return uniqueWordsList


def ReadFAQFile(FAQPathFilename):
    # This method reads the FAQ file into a list of questions (textblob) and answers (strings)
    with open(FAQPathFilename, "r", encoding="utf-8") as f:  # Example code
        FAQasList = f.readlines()  # Example code
    questionList = []
    answerList = []
    for qa in FAQasList:
        question = qa.split('?')[0]
        answer = qa.split('?')[1]
        questionList.append(TextBlob(question))
        answerList.append(answer)
    return answerList, questionList