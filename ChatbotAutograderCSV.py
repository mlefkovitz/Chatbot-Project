"""
Chatbot Autograder - Updated 11/05/2017
Please use this file to test your Chatbot class.

https://www.python.org/dev/peps/pep-0008/
function_names and variable:
lowercase with words separated by underscores as necessary to improve readability.
Class names should normally use the CapWords convention (yea!).
"Private" viariables start with _
Spaces are the preferred indentation method.
80 characters per line - Is this the 1980's?
I have not used a line printer since college

Usage: chatbotTester.py -f faq -l <log filename>
"""


import sys, getopt, json
import Chatbot
import pprint

def ChatbotAutograder(script_filename, faq_filename, log_filename):
    print(__doc__.split('.')[0])

    try:
        with open(script_filename, encoding='utf-8') as json_data:
            autograder_test_script_as_list_of_dicts = json.load(json_data)
    except:
            print("Failure opening AutograderScript json file")
            return 1

    try:
        chatbot = Chatbot.Chatbot(faq_filename)
    except FileNotFoundError:
        print("Could not find FAQ.")
        return 1

    if log_filename:
        print("Logging to file: "+log_filename)
        log_file = open(log_filename, "w")
        log_file.write("\"#" + "\",")
        log_file.write("\"Test Question" + "\",")
        log_file.write("\"Agent Response" + "\",")
        log_file.write("\"Test Answer" + "\",")
        log_file.write("\"Test Replace" + "\",")
        log_file.write("\"Action" + "\",")
        log_file.write("\n")

    score = 0.0
    total_questions = 0
    total_correct = 0
    total_wrong = 0
    wrong_answers = []
    for qa_dict in autograder_test_script_as_list_of_dicts:
        response = chatbot.input_output(qa_dict["questions"][0]).split('\n')[0]
        total_questions += 1
        if "replace" in qa_dict:
            replace = qa_dict["replace"]
        else:
            replace = ""
        if response == qa_dict["response"]:
            score += 1.0
            action = "1.0"
            total_correct += 1
            chatbot.user_feedback(True, replace)
        else:
            score -= 0.5
            action = "-0.5"
            total_wrong += 1
            chatbot.user_feedback(False, replace)
            wrong_answers.append({'1_question': qa_dict["questions"][0], '2_expected_answer': qa_dict["response"],
                                  '3_actual_answer': response.split('\n')[0]})

        if log_filename:
            log_file.write("\"" + str(total_questions) + "\",")
            log_file.write("\"" + qa_dict["questions"][0] + "\",")
            log_file.write("\"" + response + "\",")
            log_file.write("\"" + qa_dict["response"] + "\",")
            log_file.write("\"" + replace + "\",")
            log_file.write("\"" + action + "\",")
            log_file.write("\n")

    if log_filename:
        log_file.write("\"Totals\",")
        log_file.write("\"" + "Total Questions: " + str(total_questions) + "\",")
        log_file.write("\"" + "Total Wrong: " + str(total_wrong) + "\",")
        log_file.write("\"" + "Total Correct: " + str(total_correct) + "\",")
        log_file.write("\"" + "\",")
        log_file.write("\"" + "Score: " + str(score) + "\",")
        log_file.write("\n")
        log_file.close()
    print("Score:", str(score))
    print("Total Questions: " + str(total_questions))
    print("Total Correct: " + str(total_correct))
    print("Total Wrong: " + str(total_wrong))

def main(argv):
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    faq_filename = ''
    log_filename = ''
    script_filename = ''
    try:
        opts, args = getopt.getopt(argv, "hs:f:l:", ["script=", "faq=", "log="])
    except getopt.GetoptError:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
            sys.exit()
        elif opt in ("-f", "--faq"):
            faq_filename = arg
        elif opt in ("-l", "--log"):
            log_filename = arg
        elif opt in ("-s", "--script"):
            script_filename = arg

    if not faq_filename:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(2)

    if not script_filename:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(3)

    return ChatbotAutograder(script_filename, faq_filename, log_filename)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
