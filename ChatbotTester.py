"""
Simple console chatbot tester.
Please use this file to test your Chatbot class.

Usage: chatbotTester.py -f faq -l <log filename>
"""
import sys, getopt, os
import Chatbot


def ChatbotTester(FAQFilename,LogFilename):
    print(__doc__.split('.')[0])
    try:
        chatbot = Chatbot.Chatbot(FAQFilename)
    except FileNotFoundError:
        print("Could not find FAQ.")
        return 1

    if LogFilename:
        print("Loggin to file: "+LogFilename)
        logFile = open(LogFilename,"a")

    # loop
    while(1):
        try:
            userInput = input('Input: ')
        except KeyboardInterrupt:
            # User hit ctrl-c
            if LogFilename:
                logFile.close()
            return 1

        # We open and close the file to avoid loosing data if we crash
        if LogFilename:
            logFile = open(LogFilename,"a")

        response = chatbot.input_output(userInput)
        if LogFilename:
            logFile.write("\nInput: "+userInput)
            logFile.write("\nResponse: "+response)
            logFile.write("\n")
            logFile.close()

        print()
        print("Response: "+response)
        # if Type == True:
        #     try:
        #         chatbot.UserFeedback(input())
        #     except KeyboardInterrupt:
        #         # User hit ctrl-c
        #         if LogFilename:
        #             logFile.close()
        #         return 1
        # else:
        #     print()
        print()


def main(argv):
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    FAQFilename = ''
    LogFilename = ''
    try:
        opts, args = getopt.getopt(argv,"hf:l:",["faq=","log="])
    except getopt.GetoptError:
        print("Usage: chatbotTester.py -f faq -l <log filename>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: chatbotTester.py -f faq -l <log filename>")
            sys.exit()
        elif opt in ("-f", "--faq"):
            FAQFilename = arg
        elif opt in ("-l", "--log"):
            LogFilename = arg

    if not FAQFilename:
        print("Usage: chatbotTester.py -f faq -l <log filename>")
        sys.exit(1)

    return ChatbotTester(FAQFilename,LogFilename)

if __name__ == '__main__':
    print(sys.executable)
    sys.exit(main(sys.argv[1:]))
