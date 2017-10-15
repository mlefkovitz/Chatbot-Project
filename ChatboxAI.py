
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
    response = ''

    with open(FAQPathFilename, "r", encoding="utf-8") as f:  # Example code
        FAQasList = f.readlines()  # Example code

    questionList = []
    answerList = []
    for qa in FAQasList:
        question = qa.split('?')[0]
        answer = qa.split('?')[1]
        questionList.append(TextBlob(question))
        answerList.append(answer)

    i=0
    wordTupList = []
    for que in questionList:
        # print(que)
        # print(answerList[j])
        # print(len(que.words))
        extraWords = [word for word, tag in que.tags if tag in ('DT')]
        newQue = ' '
        sub_stopwords = set(que.words) - set(extraWords)
        for word in sub_stopwords:
            newQue = word + ' ' + newQue
        newQue = TextBlob(newQue)

        # print(newQue.words)
        # print(len(newQue.words))


        for words in newQue.words:
            # wordTup = (words, answerList[i], 1/len(newQue.words)) # answers are hardcoded
            wordTup = (words, i, 1/len(newQue.words)) # answer keys are hardcoded
            wordTupList.append(wordTup)
            # print(wordTup)

        i += 1

    uniqueWordsList = []
    for tuples in wordTupList:
        words = tuples[0].lower()
        if words not in uniqueWordsList:
            uniqueWordsList.append(words)

    # print(uniqueWordsList)

    uniqueWordSums = []
    for words in uniqueWordsList:
        wordSum = 0
        for tuples in wordTupList:
            if tuples[0].lower() == words:
                   wordSum += tuples[2]
        uniqueWordSums.append((words, wordSum))

    print(uniqueWordSums)

    # LogFilename = 'storequestionsparsed.txt'
    # if LogFilename:
    #     logFile = open(LogFilename, "a")
    #     logFile.write(str(wordTupList))
    #     logFile.close()

    message = TextBlob(msg)
    # print(message)
    extraWords = [word for word, tag in message.tags if tag in ('DT')]
    newMsg = ' '
    sub_stopwords = set(message.words) - set(extraWords)
    for word in sub_stopwords:
        newMsg = word + ' ' + newMsg
    newMsg = TextBlob(newMsg)
    # print(newMsg)

    answerTups = []
    for words in newMsg.words:
        print(words)
        for tuples in wordTupList:
            if tuples[0].lower() == words.lower():
                for uniqueWordTuples in uniqueWordSums:
                    if uniqueWordTuples[0].lower() == words.lower():
                        wordLikelihood = uniqueWordTuples[1]
                print(str(tuples))
                answerTups.append((tuples[1], str(tuples[2]), wordLikelihood))

    print(str(answerTups))

    uniqueAnswerList = []
    for tuples in answerTups:
        answer = tuples[0]
        if answer not in uniqueAnswerList:
            uniqueAnswerList.append(answer)

    print(uniqueAnswerList)

    uniqueAnswerSums = []
    for answers in uniqueAnswerList:
        answerSum = 0
        for tuples in answerTups:
            if tuples[0] == answers:
                currentAnswerSum = float(tuples[1]) / float(tuples[2])
                print(str(answers) + " => " + str(tuples[1]) + " / " + str(tuples[2]) + " = " + str(currentAnswerSum))
                answerSum += currentAnswerSum
        uniqueAnswerSums.append((answers, answerSum))

    print(uniqueAnswerSums)

    bestAnswer, bestAnswerScore = max(uniqueAnswerSums,key=itemgetter(1))
    print(bestAnswerScore)

    topUniqueAnswerSums = tuple(sorted(uniqueAnswerSums, key=itemgetter(1), reverse=True)[:2])
    print(topUniqueAnswerSums)

    topTwoScoreDifference = 0
    topTwoScoreThreshold = -1
    if len(topUniqueAnswerSums) > 1:
        print(bestAnswerScore - topUniqueAnswerSums[1][1])
        topTwoScoreDifference = bestAnswerScore - topUniqueAnswerSums[1][1]
        topTwoScoreThreshold = 0

    scoreThreshold = .5
    if bestAnswerScore >= scoreThreshold and topTwoScoreDifference > topTwoScoreThreshold:
        response = answerList[bestAnswer]

    return response;