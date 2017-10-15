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
        # FAQPathFilename is string containing
        # path and filename to text corpus in FAQ format.
        self.FAQPathFilename = FAQPathFilename
        with open(FAQPathFilename,"r", encoding="utf-8") as f: # Example code
            self.FAQasList = f.readlines()                     # Example code
        # TODO: Open FAQ and parse question,answers
        #       into knowledge base.
        self.FAQParsed = parseFAQsIntoInputs(self.FAQPathFilename)

        return

    def UserFeedback(self,yesorno):
        #TODO: user calls this with "yes" or "no" feedback when InputOutput returns TRUE
        return

    def InputOutput(self,msg):
        # msg is text to chatbot: question or "yes" or "no"
        # return expect response from user, agent response
        # return True,  response text as string
        # return False, "I do not know"

        if msg == "Who are you?" or msg == "Who are you":
            return False, "KBAI student, " + self.FAQPathFilename

        # TODO: Insert calls to your chatbot here
        #       Your chatbot should return '' if 
        #       it does not have an answer.
        response = ''
        # for qa in self.FAQasList:           # Example code
        #     question = qa.split('?')[0]     # Example code
        #     answer =qa.split('?')[1]        # Example code
        #     if question == msg:
        #         response = answer
        #         break
        response = basicChatBot(msg, self.FAQasList)
        response = CBRChatBot(msg, self.FAQasList)

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

