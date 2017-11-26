from textblob import TextBlob

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

def AddToCorpus(new_question, new_answer, answer_list, question_list):
    new_question = new_question.replace("?","")
    question_list.append(TextBlob(new_question))
    answer_list.append(new_answer)
    return answer_list, question_list