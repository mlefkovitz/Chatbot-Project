
from ChatboxAI import *

def SentenceSimilarityChatBot(msg, answer_list, question_list, wordTupList, uniqueWordSums, threshold_learner, extra_output = False):
    print_to_window = False
    response = ''

    new_msg = TextBlob(msg) #convert the input string to TextBlob
    new_msg = ExtractUnnecessaryWords(new_msg) # remove unnecessary words from the message

    similar_sentences = SimilarQuestions(new_msg, question_list, print_to_window) # identify similarity between input message and each sentence

    if threshold_learner == 'basic':
        score_threshold = .45
    else:
        score_threshold = .5

    if extra_output:
        response, selected_answer_id, selected_answer_score = ReturnBestResponse(answer_list, response, score_threshold,
                                                                                 similar_sentences, print_to_window,
                                                                                 extra_output)  # return best response
        return response, selected_answer_id, selected_answer_score
    else:
        response = ReturnBestResponse(answer_list, response, score_threshold, similar_sentences, print_to_window, extra_output)  # return best response
        return response


def SimilarQuestions(input_msg, question_list, print_to_window):
    # This method identifies the similarity between each question and the input message.
    # Return tuples <QuestionID, SimilarityScore>
    question_similarity_tups = []
    i = 0

    for question in question_list:
        new_question = ExtractUnnecessaryWords(question)
        question_similarity_tuple = (i, sentenceSimilarity(new_question, input_msg, print_to_window))
        question_similarity_tups.append(question_similarity_tuple)
        i = i + 1
        if print_to_window:
            print("questionID and similarityScore: " + str(question_similarity_tuple))

    return question_similarity_tups


def sentenceSimilarity(faq_sentence, input_sentence, print_to_window):
    # This method calculates the similarity between two setences.
    # Calculation found here: http://www.aclweb.org/anthology/S15-2#page=190
    # sts(S1,S2) = (na(S1) + na(S2)) / (n(S1) + n(S2))
    # sts(x, y) = similarity between two input sentences x and y;
    # na(S) = number of aligned content words in sentence S;
    # n(S) = number of content words in sentence S
    # Return similarity score

    number_of_aligned_words1 = numberOfAlignedWordsWithMatchMethod(faq_sentence, input_sentence, print_to_window)

    number_of_aligned_words2 = number_of_aligned_words1
    number_of_content_words1 = len(faq_sentence.words)
    number_of_content_words2 = len(input_sentence.words)
    if print_to_window:
        print("Number of aligned words: " + str(number_of_aligned_words1) + " " + str(number_of_aligned_words2) +
              " content words: " + str(number_of_content_words1) + " " + str(number_of_content_words2))

    sentence_similarity_score = (number_of_aligned_words1 + number_of_aligned_words2)/(number_of_content_words1 + number_of_content_words2)

    return sentence_similarity_score

def numberOfAlignedWordsWithMatchMethod(faq_sentence, input_sentence, print_to_window):
    # This method calculates the number of aligned words between two sentences.
    # Return the number of aligned words between sentence 1 and 2

    aligned_words = 0

    inputMessageWords = createInputWordTuple(input_sentence) # <Word, lowerWord, correctedWord, wordSynset>

    for faqWord in faq_sentence.words:
        word_aligned = False
        match_method = ''
        match_methods = []
        word_identical_match = False
        for input_words in inputMessageWords:
            if word_identical_match == False:
                match, match_method = similarWords(faqWord, input_words, print_to_window)
                if match:
                    word_aligned = True
                    if match_method == 'identical':
                        match_method_score = 1
                    elif match_method == 'corrected':
                        match_method_score = 1
                    elif match_method == 'singularized':
                        match_method_score = 1
                    elif match_method == 'similarity':
                        match_method_score = .4

                    match_methods.append(match_method_score)

                    if match_method == 'identical':
                        word_identical_match
        if word_aligned:
            aligned_words = aligned_words + max(match_methods)
        if print_to_window:
            print("Sentence1 word: " + str(faqWord) + " is aligned? " + str(word_aligned))

    return aligned_words

# def numberOfAlignedWords(faq_sentence, input_sentence, print_to_window):
#     # This method calculates the number of aligned words between two sentences.
#     # Return the number of aligned words between sentence 1 and 2
#
#     aligned_words = 0
#
#     input_message_words = createInputWordTuple(input_sentence) # <Word, lowerWord, correctedWord, wordSynset>
#
#     for faq_word in faq_sentence.words:
#         word_aligned = False
#         for input_words in input_message_words:
#             if word_aligned == False:
#                 match, match_method = similarWords(faq_word, input_words, print_to_window)
#                 if match:
#                     word_aligned = True
#         if word_aligned:
#             aligned_words = aligned_words + 1
#         if print_to_window:
#             print("Sentence1 word: " + str(faq_word) + " is aligned? " + str(word_aligned))
#
#     return aligned_words


