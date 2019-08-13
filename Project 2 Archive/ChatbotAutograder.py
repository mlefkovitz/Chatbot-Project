"""
Chatbot Autograder.
Please use this file to test your Chatbot class.

Usage: chatbotTester.py -f faq -l <log filename>
"""
import sys, getopt, os
import Chatbot


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
    for qa in scriptFileasList:
        question = qa.split('?')[0]
        answer =qa.split('?')[1]
        # We open and close the file to avoid loosing data if we crash
        if LogFilename:
            logFile = open(LogFilename,"a")

        Type,response = chatbot.InputOutput(question)
        action = "0.0"
        if Type == True:
            if response.split('\n')[0] == answer.split('\n')[0]:
                score += 1.0
                action = "1.0"
                chatbot.UserFeedback("yes")
            else:
                score -= 0.1
                action = "-0.1"
                chatbot.UserFeedback("no")

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
    print("Score:", score)

def main(argv):
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    FAQFilename = ''
    LogFilename = ''
    ScriptFilename = ''
    try:
        opts, args = getopt.getopt(argv,"hs:f:l:",["script=","faq=","log="])
    except getopt.GetoptError:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
            sys.exit()
        elif opt in ("-f", "--faq"):
            FAQFilename = arg
        elif opt in ("-l", "--log"):
            LogFilename = arg
        elif opt in ("-s", "--script"):
            ScriptFilename = arg

    if not FAQFilename:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(2)

    if not ScriptFilename:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(3)

    return ChatbotAutograder(ScriptFilename,FAQFilename,LogFilename)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
