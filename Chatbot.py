"""
Chatbot class - Updated 11/05/2017
This is the entry point and exit point for your chatbot.
Do not change this API. If it it changes your chatbot will
not be compatible with the autograder.

https://www.python.org/dev/peps/pep-0008/
function_names and variable:
lowercase with words separated by underscores as necessary to improve readability.
Class names should normally use the CapWords convention (yea!).
"Private" viariables start with _
Spaces are the preferred indentation method.
80 characters per line - Is this the 1980's?
I have not used a line printer since college

I highly recommend just calling your code from this file
(put your chatbot code in another file) in case we need to
change this file during the project.
"""


class Chatbot:

    def __init__(self, faq_path_filename):
        # faq_path_filename is string containing
        # path and filename to text corpus in FAQ format.
        # Note: You MUST use encoding="utf-8" to properly decode the FAQ
        self.faq_path_filename = faq_path_filename
        with open(faq_path_filename, "r", encoding="utf-8") as f:  # Example code
            self.faq_as_list = f.readlines()                       # Example code
        # TODO: Open FAQ using encoding="utf-8" and parse question,answers
        #       into knowledge base.
        return

    # user_feedback(yesorno : boolean, correct_response : string):
    #      yesorno = True - Your previous response was correct
    #                False - Your previous response was incorrect
    #     updated_response = Response to ADD to FAQ
    def user_feedback(self, yesorno, updated_response):
        # TODO:
        # if yesorno == True, you answered the prvious question correctly
        # if yesorno == False, you answered the previous question incorrectly
        # if updated_response != "", you need to update the previous response in the FAQ
        # You WILL get feedback after EVERY question
        if updated_response:
            print("Updating FAQ: "+updated_response)  # Example code
        return

    # input_output(msg : string) :        response : string
    #      msg          =  string from user (will not have ? at end)(no case guarantee)
    #      response = Text response from FAQ
    def input_output(self, msg):
        # TODO: Insert calls to your chatbot here
        #       Your chatbot should return '' if
        #       it does not have an answer.
        response = ''
        for qa in self.faq_as_list:              # Example code
            if len(qa.split('?')) < 2: continue  # Example code
            question = qa.split('?')[0]          # Example code
            answer = qa.split('?')[1]            # Example code
            if question == msg:                  # Example code
                response = answer                # Example code
                break                            # Example code

        # You should not need to change any of the code below
        # this line.

        # If your agent does not know the answer
        if not response:
            return "I do not know."

        # If your agent knows the answer
        return response
