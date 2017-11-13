
from textblob import TextBlob
from operator import itemgetter

def CBRChatBot(msg, answer_list, word_tup_list, unique_word_sums, threshold_learner):
    print_to_window = False
    response = ''

    new_msg = TextBlob(msg) #convert the input string to TextBlob
    new_msg = ExtractUnnecessaryWords(new_msg) # remove unnecessary words from the message

    answer_tups = RelevantAnswerTuples(new_msg, unique_word_sums, word_tup_list, print_to_window) # find all questions with
                            #... words that match a word in the message. Return tuples <AnswerID, weight, sum(weights)>

    unique_answer_list = ListUniqueAnswers(answer_tups, print_to_window) # List unique answers relevant to the message
    unique_answer_scores = ScoreEachAnswer(answer_tups, unique_answer_list, print_to_window) # Find the score for each answer

    if threshold_learner == 'basic':
        score_threshold = .5
    else:
        score_threshold = .6

    response = ReturnBestResponse(answer_list, response, score_threshold, unique_answer_scores, print_to_window) #return best response

    return response;


def SentenceSimilarityChatBot(msg, answer_list, question_list, wordTupList, uniqueWordSums, threshold_learner):
    print_to_window = True
    response = ''

    new_msg = TextBlob(msg) #convert the input string to TextBlob
    new_msg = ExtractUnnecessaryWords(new_msg) # remove unnecessary words from the message

    similar_sentences = SimilarQuestions(new_msg, question_list, print_to_window) # identify similarity between input message and each sentence

    if threshold_learner == 'basic':
        score_threshold = .45
    else:
        score_threshold = .5

    response = ReturnBestResponse(answer_list, response, score_threshold, similar_sentences, print_to_window) #return best response

    return response;


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


def numberOfAlignedWords(faq_sentence, input_sentence, print_to_window):
    # This method calculates the number of aligned words between two sentences.
    # Return the number of aligned words between sentence 1 and 2

    aligned_words = 0

    input_message_words = createInputWordTuple(input_sentence) # <Word, lowerWord, correctedWord, wordSynset>

    for faq_word in faq_sentence.words:
        word_aligned = False
        for input_words in input_message_words:
            if word_aligned == False:
                match, match_method = similarWords(faq_word, input_words, print_to_window)
                if match:
                    word_aligned = True
        if word_aligned:
            aligned_words = aligned_words + 1
        if print_to_window:
            print("Sentence1 word: " + str(faq_word) + " is aligned? " + str(word_aligned))

    return aligned_words

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


def similarWords(faq_word, input_words, print_to_window, use_synsets = True):
    # This method identifies whether two words are similar
    # Return True or False

    similar_path = False
    match_method = ''
    tb_faq_word = TextBlob(faq_word)
    lower_faq_word = tb_faq_word.lower()
    lower_input_worrd = input_words[1]
    corrected_input_word = input_words[2]
    if use_synsets:
        faq_word_synset = lower_faq_word.words[0].synsets

    # print("Words and Synset Lengths: " + str(lower_faq_word) + "(" + str(len(lower_faq_word.words[0].synsets)) + ") & " + str(
    #     lower_input_worrd) + "(" + str(len(lower_input_worrd.words[0].synsets)) + ") ")

    words_are_similar = False
    if lower_faq_word == lower_input_worrd:
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
        print("Words: " + str(lower_faq_word) + " & " + str(lower_input_worrd) + " (" + str(match_method) + ")")
        if similar_path:
           print("Synset path similarity: " + str(corrected_word_similarity))

    return words_are_similar, match_method


def ReturnBestResponse(answer_list, response, score_threshold, unique_answer_scores, print_to_window):
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
            if similarWords(tuples[0], words, print_to_window, False):
                for unique_word_tuples in unique_word_sums: # <word, SUM(score)>
                    if unique_word_tuples[0].lower() == tuples[0].lower():
                        word_likelihood = unique_word_tuples[1]
                        answer_tups.append((tuples[1], str(tuples[2]), word_likelihood))
                if print_to_window:
                    print("word, answerID, and probability: " + str(tuples))
    if print_to_window:
        print("Answers, scores, and likelihood modifiers, for all words: " + str(answer_tups))
    return answer_tups


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


def ReadFAQFile(faq_path_filename):
    # This method reads the FAQ file into a list of questions (textblob) and answers (strings)
    with open(faq_path_filename, "r", encoding="utf-8") as f:  # Example code
        faq_as_list = f.readlines()  # Example code
    question_list = []
    answer_list = []
    for qa in faq_as_list:
        question = qa.split('?')[0]
        answer = qa.split('?')[1]
        question_list.append(TextBlob(question))
        answer_list.append(answer)
    return answer_list, question_list