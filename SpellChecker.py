############################
# Group A Skill 
# OOP: Classes
############################

class SpellCheck:

    ############################
    # Group B Skill
    # Reads words from words.txt file then puts them into a set (faster lookup time than list)
    # Words.txt contains a list of 58,112 valid english words
    ############################
    def __init__(self):
        with open("words.txt", "r") as f:
            words = f.read()
        self.wordset = {word.lower() for word in words.splitlines()}

    # Determines whether the passed in word is in the list of words
    def check_word(self,word):
        return word in self.wordset