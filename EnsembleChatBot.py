from CBRChatBot import *
from SentenceSimilarityChatBot import *

def EnsembleChatBot(msg, answer_list, question_list, word_tup_list, unique_word_sums, threshold_learner, extra_output = False):

    SSresponse, SSselected_answer_id, SSselected_answer_score = SentenceSimilarityChatBot(msg, answer_list, question_list, word_tup_list, unique_word_sums, threshold_learner, True)
    CBRresponse, CBRselected_answer_id, CBRselected_answer_score = CBRChatBot(msg, answer_list, word_tup_list, unique_word_sums, threshold_learner, True)

    if SSselected_answer_score >= CBRselected_answer_score - 0.2:
        response = SSresponse
        selected_chat_bot = 'SS'
    else:
        response = CBRresponse
        selected_chat_bot = 'CBR'

    if extra_output:
        return response, SSselected_answer_id, SSselected_answer_score, CBRselected_answer_id, CBRselected_answer_score, selected_chat_bot
    else:
        return response