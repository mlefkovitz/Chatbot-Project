"""
Chatbot Autograder2.
Please use this file to test your Chatbot class.

MODIFIED BY BPOTOCKI3 TO INCLUDE ADDITIONAL STATS

Usage: chatbotAutograder2.py -s script -f faq -l <log filename>
"""
import sys, getopt, os
import Chatbot
import pprint


def ChatbotAutograder(ScriptFilename,FAQFilename,LogFilename):
    print(__doc__.split('.')[0])

    try:
        with open(ScriptFilename,"r", encoding="utf-8") as f:
            scriptFileasList = f.readlines()
    except FileNotFoundError:
        print("Could not find script.")
        return 1

    try:
        chatbot = Chatbot.Chatbot(FAQFilename)
    except FileNotFoundError:
        print("Could not find FAQ.")
        return 1

    if LogFilename:
        print("Loggin to file: "+LogFilename)
        logFile = open(LogFilename,"a")

    score = 0.0
    total_questions = 0
    total_correct = 0
    total_skipped = 0
    total_wrong = 0
    wrong_answers = []
    for qa in scriptFileasList:
        question = qa.split('?')[0]
        answer =qa.split('?')[1].strip()
        # We open and close the file to avoid loosing data if we crash
        if LogFilename:
            logFile = open(LogFilename,"a")

        Type,response = chatbot.InputOutput(question)
        action = "0.0"
        total_questions += 1
        if Type == True:
            if response.split('\n')[0] == answer.split('\n')[0]:
                score += 1.0
                action = "1.0"
                total_correct += 1
                chatbot.UserFeedback("yes")
            else:
                score -= 0.1
                action = "-0.1"
                total_wrong += 1
                wrong_answers.append({'1_question':question, '2_expected_answer':answer.split('\n')[0], '3_actual_answer':response.split('\n')[0]})
                chatbot.UserFeedback("no")
        else:
            if not question.startswith("Who are you"):
                total_skipped += 1

        if LogFilename:
            logFile.write("\nInput: "+question)
            logFile.write("\nResponse: "+response)
            logFile.write("\nCorrect: "+answer)
            logFile.write("\nType: "+str(Type))
            logFile.write("\nAction: "+action)
            logFile.write("\n")
            logFile.close()

        print()
        print("Response: "+response)
        if not Type: print()
        print()
    if LogFilename:
        logFile = open(LogFilename,"a")
        logFile.write("\nScore: " + str(score))
        logFile.write("\nTotal Questions: " + str(total_questions))
        logFile.write("\nTotal Correct: " + str(total_correct))
        logFile.write("\nTotal Skipped: " + str(total_skipped))
        logFile.write("\nTotal Wrong: " + str(total_wrong))
        if total_wrong > 0:
            logFile.write("\nWrong Answer Breakdown:\n")
            pprint.pprint(wrong_answers, logFile)
        logFile.write("\n")
        logFile.close()
    print("Score:", str(score))
    print("Total Questions: " + str(total_questions))
    print("Total Correct: " + str(total_correct))
    print("Total Skipped: " + str(total_skipped))
    print("Total Wrong: " + str(total_wrong))
    if total_wrong > 0:
        print("(Wrong Answer Breakdown in logfile)")
    print("\n")

def main(argv):
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    FAQFilename = ''
    LogFilename = ''
    ScriptFilename = ''
    try:
        opts, args = getopt.getopt(argv,"hs:f:l:",["script=","faq=","log="])
    except getopt.GetoptError:
        print("Usage: chatbotAutograder2.py -s script -f faq -l <log filename>")
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: chatbotAutograder2.py -s script -f faq -l <log filename>")
            sys.exit()
        elif opt in ("-f", "--faq"):
            FAQFilename = arg
        elif opt in ("-l", "--log"):
            LogFilename = arg
        elif opt in ("-s", "--script"):
            ScriptFilename = arg

    if not FAQFilename:
        print("Usage: chatbotAutograder2.py -s script -f faq -l <log filename>")
        sys.exit(2)

    if not ScriptFilename:
        print("Usage: chatbotAutograder2.py -s script -f faq -l <log filename>")
        sys.exit(3)

    return ChatbotAutograder(ScriptFilename,FAQFilename,LogFilename)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
