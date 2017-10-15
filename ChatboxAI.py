
from textblob import TextBlob
# import sys



def basicChatBot(msg, FAQList):
    response = ''
    for qa in FAQList:  # Example code
        question = qa.split('?')[0]  # Example code
        answer = qa.split('?')[1]  # Example code
        if question == msg:
            response = answer
    return response;

def CBRChatBot(msg, FAQList):
    response = ''
    textList = TextBlob(FAQList)




    return response;

def parseFAQsIntoInputs(FAQPathFilename):
    # sys.setdefaultencoding('utf8')
    FAQFile = open(FAQPathFilename,"r", encoding="utf-8")
    FAQtext = FAQFile.read()
    with open(FAQPathFilename, "r", encoding="utf-8") as f:  # Example code
        FAQasList = f.readlines()  # Example code

    textList = TextBlob(FAQtext)
    print(textList)
    i=0
    questionList = []
    for qa in FAQasList:
        question = qa.split('?')[0]
        questionList.append(TextBlob(question))
        i += 1

    for que in questionList:
        print(que)
        print(que.words)
        print(len(que.words))
        print(que.tags)
        extraWords = [word for word, tag in que.tags if tag in ('DT')]
        print(extraWords)
        print([(word, tag) for word, tag in que.tags if tag not in ('DT')])
        newQue = ' '
        sub_stopwords = set(que.words) - set(extraWords)
        print(sub_stopwords)
        for word in sub_stopwords:
            newQue = word + newQue + ' '
        newQue = TextBlob(newQue)
        print(newQue.words)
        print(len(newQue.words))
        print(newQue.tags)

    

    return 1;