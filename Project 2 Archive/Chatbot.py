"""
Chatbot class
This is the entry point and exit point for your chatbot. 
Do not change this API. If it it changes your chatbot will
not be compatible with the autograder.

I highly recommend just calling your code from this file 
(put your chatbot code in another file) in case we need to
change this file during the project.
"""
from ChatboxAI import *

class Chatbot:

    def __init__(self,FAQPathFilename):
        printToWindow = False

        answerList, questionList = ReadFAQFile(FAQPathFilename)  # read the FAQ
        wordTupList = RelevantWordTuples(questionList, printToWindow)  # extract to tuples <word, answerID, weight>
        uniqueWordsList = FindUniqueWords(wordTupList, printToWindow)  # find unique words
        uniqueWordSums = ScoreUniqueWords(wordTupList, uniqueWordsList, printToWindow)  # <word, SUM(weight)>

        self.answerList = answerList
        self.questionList = questionList
        self.wordTupList = wordTupList
        self.uniqueWordsList = uniqueWordsList
        self.uniqueWordSums = uniqueWordSums

        self.count = 0
        self.yes = 0
        self.learningScoreThreshold = 'basic'
        return

    def UserFeedback(self,yesorno):
        self.count = self.count + 1
        if yesorno == "yes":
            self.yes = self.yes + 1
        return

    def InputOutput(self,msg):
        # msg is text to chatbot: question or "yes" or "no"
        # return expect response from user, agent response
        # return True,  response text as string
        # return False, "I do not know"

        if msg == "Who are you?" or msg == "Who are you":
            return False, "Myles Lefkovitz, gth836x, 901929700, " + self.FAQPathFilename

        # Learning portion of the agent
        if self.count >= 10:
            proportionCorrect = self.yes / self.count
            if proportionCorrect >= 0.50:
                self.learningScoreThreshold = 'basic'
            else:
                self.learningScoreThreshold = 'increased'

        # response = CBRChatBot(msg, self.answerList, self.wordTupList, self.uniqueWordSums, self.learningScoreThreshold)
        response = SentenceSimilarityChatBot(msg, self.answerList, self.questionList, self.wordTupList, self.uniqueWordSums, self.learningScoreThreshold)

        # You should not need to change any of the code below
        # this line.

        # If your agent does not know the answer
        if not response:
            return False,"I do not know."

        # If your agent knows the answer
        # True indicates your agent is expecting a "yes" or "no" from the user
        # in the next call to Chatbot()
        # Do not change this return statement
        return True, response + "\nIs the response correct (yes/no)?"

