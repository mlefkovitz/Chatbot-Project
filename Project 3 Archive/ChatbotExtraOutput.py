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

from ChatbotCorpus import *
from EnsembleChatBot import *


class Chatbot:

    def __init__(self, faq_path_filename):
        print_to_window = False

        answer_list, question_list = ReadFAQFile(faq_path_filename)  # read the FAQ
        word_tup_list, unique_words_list, unique_word_sums = InitializeWordLists(question_list, print_to_window)

        self.answer_list = answer_list
        self.question_list = question_list
        self.word_tup_list = word_tup_list
        self.unique_words_list = unique_words_list
        self.unique_word_sums = unique_word_sums

        self.count = 0
        self.yes = 0
        self.learning_score_threshold = 'basic'

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

        self.count = self.count + 1
        if yesorno == "yes":
            self.yes = self.yes + 1

        if updated_response:
            print("Question: " + self.current_question)  # Example code
            print("Updating FAQ: " + updated_response)  # Example code
            answer_list, question_list = AddToCorpus(self.current_question, updated_response, self.answer_list, self.question_list)
            word_tup_list, unique_words_list, unique_word_sums = InitializeWordLists(question_list, False)
            self.answer_list = answer_list
            self.question_list = question_list
            self.word_tup_list = word_tup_list
            self.unique_words_list = unique_words_list
            self.unique_word_sums = unique_word_sums
        return

    # input_output(msg : string) :        response : string
    #      msg          =  string from user (will not have ? at end)(no case guarantee)
    #      response = Text response from FAQ
    def input_output(self, msg):
        self.current_question = msg

        # Learning portion of the agent
        if self.count >= 10:
            proportion_correct = self.yes / self.count
            if proportion_correct >= 0.50:
                self.learning_score_threshold = 'basic'
            else:
                self.learning_score_threshold = 'increased'

        extra_output = True
        if extra_output:
            response, SSselected_answer_id, SSselected_answer_score, CBRselected_answer_id,  CBRselected_answer_score, selected_chat_bot = \
                EnsembleChatBot(msg, self.answer_list, self.question_list, self.word_tup_list, self.unique_word_sums,
                                self.learning_score_threshold, extra_output)

            if not response:
                return "I do not know.", SSselected_answer_id, SSselected_answer_score, CBRselected_answer_id,  CBRselected_answer_score, selected_chat_bot
            return response, SSselected_answer_id, SSselected_answer_score, CBRselected_answer_id,  CBRselected_answer_score,selected_chat_bot
        else:
            response = EnsembleChatBot(msg, self.answer_list, self.question_list, self.word_tup_list, self.unique_word_sums,
                                self.learning_score_threshold, extra_output)
            # You should not need to change any of the code below
            # this line.

            # If your agent does not know the answer
            if not response:
                return "I do not know."

            # If your agent knows the answer
            return response
