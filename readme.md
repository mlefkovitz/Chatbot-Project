## KBAI Chatbot Project

Myles Lefkovitz - gth836x

![Live Chatbot](Chatbot%20Live%20Recording.gif)

### About

A chatbot that returns answers to natural language questions about one of my courses (CS7637 Knowledge Based Artificial Intelligence), helping to replace some of the duties of a teaching assistant. Questions can be typed in a live environment (with responses returned on the screen) or entered via a script and logged via file. The chatbot must be provided with a corpus of knowledge (the FAQ list for the class) and returns answers via that list.

The chatbot uses an ensemble method for natural language processing combining a case based reasoning algorithm and a sentence similarity algorithm. The case based reasoning algorithm identifies the question in the corpus that has the most unique matching words with the input question. The sentence similarity method algorithm identifies the question in the corpus that has the largest proportional match to the input question.

The chatbot is built in Python and implements the TextBlob library for word parsing along with a few other features.

The ensemble method is relatively simple, but very high performing garnering one of the highest scores in the class. The full write-up is available on github (https://github.com/mlefkovitz/Chatbot-Project/blob/master/Chatbot%20Reflection.pdf).

### Run instructions

To run the chatbot from a script, run ChatbotAutograder.py
- use the following command: py chatbotAutograder.py -s TestScript.json -f Fall2017syllabusFAQ.txt -l autograderlogfile.txt
- This command outputs to "autograderlogfile.txt"
- The script (JSON) and FAQ (text) files can be subbed for any other files

To run the chatbot in the command prompt, run ChatbotTester.py
- use the following command: py chatbotTester.py -f Fall2017syllabusFAQ.txt -l testerlogfile.txt
- This command outputs to "testerlogfile.txt"
- The FAQ file can be subbed for any other file
