
from textblob import TextBlob
from operator import itemgetter


def InitializeWordLists(question_list, print_to_window):
    word_tup_list = RelevantWordTuples(question_list, print_to_window)  # extract to tuples <word, answerID, weight>
    unique_words_list = FindUniqueWords(word_tup_list, print_to_window)  # find unique words
    unique_word_sums = ScoreUniqueWords(word_tup_list, unique_words_list, print_to_window)  # <word, SUM(weight)>

    return word_tup_list, unique_words_list, unique_word_sums


def RelevantWordTuples(question_list, print_to_window):
    # This method creates a tuple for each relevant word in each question
    # The tuples take the form: (
    #   <relevant word>,
    #   <question/answer number>, (so the answer can be found in the AnswerList)
    #   <relative word importance in the question> (1/the number of relevant words in the question)
    i = 0
    word_tup_list = []
    for que in question_list:
        new_que = ExtractUnnecessaryWords(que, print_to_window)

        if print_to_window:
            print("Original question: " + str(que))
            print("Number of words in original question: " + str(len(que.words)))
            print("Remaining words after removal of unnecessary words: " + str(new_que.words))
            print("Number of words remaining: " + str(len(new_que.words)))

        for words in new_que.words:
            # word_tup = (words, answerList[i], 1/len(new_que.words)) # answers are hardcoded
            word_tup = (words, i, 1 / len(new_que.words))  # answer keys are hardcoded
            word_tup_list.append(word_tup)
            if print_to_window:
                print("word, questionID, fraction of question: " +  str(word_tup))
        i += 1
    return word_tup_list


def FindUniqueWords(word_tup_list, print_to_window):
    # This method identifies the unique words in the list of question
    unique_words_list = []
    for tuples in word_tup_list:
        words = tuples[0].lower()
        if words not in unique_words_list:
            unique_words_list.append(words)
    if print_to_window:
        print("Unique Words: " + str(unique_words_list))
    return unique_words_list


def ScoreUniqueWords(word_tup_list, unique_words_list, print_to_window):
    # This method returns a tuple containing:
    #   <the word>,
    #   <the sum of the word's relative importance across all questions> (this value will be used to normalize words)
    # A low total score means that the word appears very infrequently. A high total score means that the word is common

    unique_word_sums = []
    for words in unique_words_list:
        word_sum = 0
        for tuples in word_tup_list:
            if tuples[0].lower() == words:
                word_sum += tuples[2]
        unique_word_sums.append((words, word_sum))
    if print_to_window:
        print(unique_word_sums)
    return unique_word_sums


def createInputWordTuple(input_sentence, use_synsets = True):
    #This method creates a tuple for each word in the inputSentence
    corrected_input_word_synsets = ''

    input_message_words = []  # input Words
    # <Word, lowerWord, correctedWord, wordSynset>
    for input_word in input_sentence.words:
        tb_input_word = TextBlob(input_word)
        lower_input_word = tb_input_word.lower()
        corrected_input_word = lower_input_word.correct()
        if use_synsets:
            corrected_input_word_synsets = corrected_input_word.words[0].synsets
        input_message_words.append((input_word, lower_input_word, corrected_input_word, corrected_input_word_synsets))

    return input_message_words


def ReturnBestResponse(answer_list, response, score_threshold, unique_answer_scores, print_to_window, extra_output = False):
    # This method identifies the highest scoring response and returns it
    # Return the best scoring response
    if len(unique_answer_scores) == 0:
        return response

    best_answer_id, best_answer_score = max(unique_answer_scores, key=itemgetter(1))
    if print_to_window:
        print("best_answer_score = " + str(best_answer_score))

    # Sort the responses and select the ones with the highest two scores
    top_unique_answer_sums = tuple(sorted(unique_answer_scores, key=itemgetter(1), reverse=True)[:2])
    if print_to_window:
        print("top_unique_answer_sums = " + str(top_unique_answer_sums))

    top_two_score_threshold = -1
    top_two_score_difference = 0
    # Calculate the difference between the 1st and 2nd highest scores
    if len(top_unique_answer_sums) > 1:
        if print_to_window:
            print("best_answer_score - top_unique_answer_sums[1][1] = " + str(best_answer_score - top_unique_answer_sums[1][1]))
        top_two_score_difference = best_answer_score - top_unique_answer_sums[1][1]
        top_two_score_threshold = 0

    # To be returned, a response must exceed the "scoreThreshold" and must differ from the 2nd highest scoring response
    if best_answer_score >= score_threshold and top_two_score_difference > top_two_score_threshold:
        response = answer_list[best_answer_id]

    if extra_output:
        return response, best_answer_id, best_answer_score
    else:
        return response


def ExtractUnnecessaryWords(set_of_words, print_to_window = False):
    # This method extracts unnecessary words from an input set and returns the remaining words as a TextBlob object
    if print_to_window:
        print("Parts of speach for each word: " + str(set_of_words.tags))

    extra_words = [word for word, tag in set_of_words.tags if tag in ('DT', 'POS')]
    new_set_of_words = ' '
    sub_stopwords = set(set_of_words.words) - set(extra_words)
    for word in sub_stopwords:
        new_set_of_words = word + ' ' + new_set_of_words
    new_set_of_words = TextBlob(new_set_of_words)
    return new_set_of_words



def similarWords(faq_word, input_words, print_to_window, use_synsets = True):
    # This method identifies whether two words are similar
    # Return True or False

    similar_path = False
    match_method = ''
    tb_faq_word = TextBlob(faq_word)
    lower_faq_word = tb_faq_word.lower()
    lower_input_word = input_words[1]
    corrected_input_word = input_words[2]
    if use_synsets:
        faq_word_synset = lower_faq_word.words[0].synsets

    # print("Words and Synset Lengths: " + str(lower_faq_word) + "(" + str(len(lower_faq_word.words[0].synsets)) + ") & " + str(
    #     lower_input_word) + "(" + str(len(lower_input_word.words[0].synsets)) + ") ")

    words_are_similar = False
    if lower_faq_word == lower_input_word:
        words_are_similar = True
        match_method = 'identical'
    elif lower_faq_word == corrected_input_word:
        words_are_similar = True
        match_method = 'corrected'
    elif lower_faq_word.words.singularize() == corrected_input_word.words.singularize():
        words_are_similar = True
        match_method = 'singularized'
    elif use_synsets:
        if len(faq_word_synset) > 0:
            #correct_input_word_synsets = corrected_input_word.words[0].synsets
            correct_input_word_synsets = input_words[3]
            if len(correct_input_word_synsets) > 0:
                corrected_word_similarity = faq_word_synset[0].wup_similarity(correct_input_word_synsets[0])
                if corrected_word_similarity is not None:
                    if corrected_word_similarity >= 0.65:
                        words_are_similar = True
                        similar_path = True
                        match_method = 'similarity'

    # printToWindow = True
    if print_to_window & words_are_similar:
        print("Words: " + str(lower_faq_word) + " & " + str(lower_input_word) + " (" + str(match_method) + ")")
        if similar_path:
           print("Synset path similarity: " + str(corrected_word_similarity))

    return words_are_similar, match_method



