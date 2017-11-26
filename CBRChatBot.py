
from ChatboxAI import *

def CBRChatBot(msg, answer_list, word_tup_list, unique_word_sums, threshold_learner, extra_output = False):
    print_to_window = False
    response = ''

    if(print_to_window):
        print(msg)

    new_msg = TextBlob(msg) #convert the input string to TextBlob
    if (print_to_window):
        print(new_msg)

    new_msg = ExtractUnnecessaryWords(new_msg) # remove unnecessary words from the message
    if (print_to_window):
        print(new_msg)

    answer_tups = RelevantAnswerTuples(new_msg, unique_word_sums, word_tup_list, print_to_window) # find all questions with
                            #... words that match a word in the message. Return tuples <AnswerID, weight, sum(weights)>

    unique_answer_list = ListUniqueAnswers(answer_tups, print_to_window) # List unique answers relevant to the message
    unique_answer_scores = ScoreEachAnswer(answer_tups, unique_answer_list, print_to_window) # Find the score for each answer

    if threshold_learner == 'basic':
        score_threshold = .5
    else:
        score_threshold = .6

    if extra_output:
        response, selected_answer_id, selected_answer_score = ReturnBestResponse(answer_list, response, score_threshold,
                                                                                 unique_answer_scores, print_to_window,
                                                                                 extra_output)  # return best response
        selected_answer_confidence = selected_answer_score/(1 + selected_answer_score)
        return response, selected_answer_id, selected_answer_confidence
    else:
        response = ReturnBestResponse(answer_list, response, score_threshold, unique_answer_scores, print_to_window, extra_output)  # return best response
        return response

def ScoreEachAnswer(answer_tups, unique_answer_list, print_to_window):
    # This method finds the normalized score associated with each answer
    unique_answer_sums = []
    for answers in unique_answer_list:
        answer_sum = 0
        for tuples in answer_tups:
            if tuples[0] == answers:
                current_answer_sum = float(tuples[1]) / float(tuples[2])
                if print_to_window:
                    print(
                        str(answers) + " => " + str(tuples[1]) + " / " + str(tuples[2]) + " = " + str(current_answer_sum))
                answer_sum += current_answer_sum
        unique_answer_sums.append((answers, answer_sum))
    if print_to_window:
        print("unique_answer_sums = " + str(unique_answer_sums))
    return unique_answer_sums


def ListUniqueAnswers(answer_tups, print_to_window):
    # This method lists all unique answers relevant to the input message
    unique_answer_list = []
    for tuples in answer_tups:
        answer = tuples[0]
        if answer not in unique_answer_list:
            unique_answer_list.append(answer)
    if print_to_window:
        print("Unique Answers: " + str(unique_answer_list))
    return unique_answer_list

def RelevantAnswerTuples(new_msg, unique_word_sums, word_tup_list, print_to_window):
    # This method finds all questions with words that match a word in the message.
    # Return tuples <AnswerID, score, sum(scores)>
    answer_tups = []

    input_message_words = createInputWordTuple(new_msg)  # <Word, lowerWord, correctedWord, wordSynset>

    for words in input_message_words:
        if print_to_window:
            print("Input word: " + str(words))
        for tuples in word_tup_list: #<word, answerID, probability>
            # if tuples[0].lower() == words.lower():
            if similarWords(tuples[0], words, print_to_window, False)[0]:
                for unique_word_tuples in unique_word_sums: # <word, SUM(score)>
                    if unique_word_tuples[0].lower() == tuples[0].lower():
                        word_likelihood = unique_word_tuples[1]
                        answer_tups.append((tuples[1], str(tuples[2]), word_likelihood))
                if print_to_window:
                    print("word, answerID, and probability: " + str(tuples))
    if print_to_window:
        print("Answers, scores, and likelihood modifiers, for all words: " + str(answer_tups))
    return answer_tups
