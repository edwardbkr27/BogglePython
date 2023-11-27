from PyDictionary.core import PyDictionary
import random
import time
import threading
from SpellChecker import SpellCheck
import math
import sqlite3
import bcrypt
from Server import Host
from Client import Client

############################
# Group A Skill
# OOP: Classes
############################

class Database:

    # Establishes connection to database and only creates tables if they do not already exist
    connect = sqlite3.connect('gamedata.db', check_same_thread=False)
    c = connect.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS accounts (id integer primary key, username text, password text, correctcolour text, incorrectcolour text)""")

    c.execute("""CREATE TABLE IF NOT EXISTS games (id integer primary key, userid integer, gamemode text, difficulty text, gamelength integer, score integer, wordsfound integer, date text)""")

    connect.commit()

########################
##### ACCOUNTS/SQL #####
########################

    ############################
    # Group A Skill 
    # Hashing
    # Hashes password before inserting it into the database
    ############################
    # Excellent Coding Style Demonstrated throughout database class through:
    # Subroutines with appropriate interfaces
    # Loosely Coupled Modules
    # Cohesive Modules
    # Good Exception Handling
    # Modules with common purpose grouped
    # Defensive Programming
    ############################
    def _doRegister(self, username, password, correctcolour, incorrectcolour):
        password = password.encode('utf-8')
        passhash = bcrypt.hashpw(password, bcrypt.gensalt())
        Database.c.execute("SELECT username FROM accounts WHERE username=?", (username,))
        data = Database.c.fetchall()
        if username not in str(data):
            try:
                Database.c.execute("""INSERT INTO accounts (username, password, correctcolour, incorrectcolour)
                    VALUES (?,?,?,?)""", (username, passhash, correctcolour, incorrectcolour))
            except sqlite3.InterfaceError:
                Database.c.execute("""INSERT INTO accounts (username, password, correctcolour, incorrectcolour)
                    VALUES (?,?,?,?)""", (username, passhash, correctcolour, incorrectcolour))
            Database.connect.commit()
        return [username, password, correctcolour, incorrectcolour]

    # Fetches password from games table by username
    # Determines if the account exists
    # Dehashes password if something is found under the username
    # If correct credentials, returns data under that account
    def _doLogin(self, username, password):
        Database.c.execute("SELECT password FROM accounts WHERE username=?", (username,))
        if password != "":
            try:
                passhash = Database.c.fetchone()[0]
                if passhash != "[]":
                    if bcrypt.checkpw(password, passhash):
                        Database.c.execute("SELECT * FROM accounts WHERE username=?", (username,))
                        items = str(Database.c.fetchall())
                        if items == "[]":
                            return None
                        else:
                            Database.c.execute("SELECT correctcolour FROM accounts WHERE username=?", (username,))
                            correctcolour = Database.c.fetchone()[0]
                            Database.c.execute("SELECT incorrectcolour FROM accounts WHERE username=?", (username,))
                            incorrectcolour = Database.c.fetchone()[0]
                            Database.c.execute("SELECT id FROM accounts WHERE username=?", (username,))
                            id = Database.c.fetchone()[0] 
                            return [username, password, id, correctcolour, incorrectcolour]
                    else:
                        return None
                else:
                    return None
            except TypeError:
                return None
    
    # Checks if a username is already taken
    def _checkIfUsernameTaken(self, username):
        Database.c.execute("SELECT username FROM accounts WHERE username=?", (username,))
        data = Database.c.fetchall()
        if username in str(data):
            return True
        else:
            return False

    # Inserts data about a game into the games table
    def _addGameEntry(self, id, gamemode, difficulty, duration, score, wordsfound, datenow):
        Database.c.execute("""INSERT INTO games (userid, gamemode, difficulty, gamelength, score, wordsfound, date)
        VALUES (?,?,?,?,?,?,?)""", (id, gamemode, difficulty, duration, score, wordsfound, datenow))
        Database.connect.commit()

    # Updates colour settings using account id
    def _updateSettings(self, correctcolour, incorrectcolour, id):
        Database.c.execute("UPDATE accounts set correctcolour = ? WHERE id = ?", (correctcolour, id))
        Database.c.execute("UPDATE accounts set incorrectcolour = ? WHERE id = ?", (incorrectcolour,id))
        Database.connect.commit()

    # Selects data from games table from all accounts on gamemode and difficulty
    def _getLeaderboardData(self, gamemode, difficulty):
        data = []
        Database.c.execute("SELECT userid, id, gamelength, score, wordsfound, date FROM games WHERE gamemode=? AND difficulty=? ORDER BY score DESC", (gamemode, difficulty))
        data = Database.c.fetchall()
        return data
    
    def _getUsernameFromID(self, id):
        Database.c.execute("SELECT username FROM accounts WHERE id=?", (id,))
        username = Database.c.fetchone()[0]
        return username

    def _getIDFromUsername(self, username):
        Database.c.execute("SELECT id FROM accounts WHERE username=?", (username,))
        id = Database.c.fetchone()[0]
        return id

    def _getLatestGameID(self):
        Database.c.execute("SELECT id FROM games ORDER BY id DESC")
        id = Database.c.fetchone()[0]
        return id

    ############################
    # Group A Skill 
    # Cross Table Parameterised SQL
    ############################
    # Fetches previously played games from the games table where the userid in the games table matches the id of the username in the accounts table.
    def _getPreviouslyPlayedGames(self, username, gamemode):
        Database.c.execute("SELECT accounts.id, games.id, games.difficulty, games.gamelength, games.score, games.wordsfound, games.date FROM games INNER JOIN accounts on accounts.id = games.userid WHERE accounts.username = ? and games.gamemode = ?", (username,gamemode))
        data = Database.c.fetchall()
        return data

    # Closes connection to database
    def _closeConnection(self):
        Database.c.close()

############################
# Group A Skill
# OOP: Classes
############################

class Game:
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # Dictionary mapping word length to score multiplier
    WORDLENGTHMULTIPLIER = {1:1, 2:1, 3:2, 4:3, 5:4, 6:6, 7:7, 8:9, 9:10, 10:10, 11:10, 12:10, 13:10, 14:10, 15:10, 16:10, 17:10, 18:10, 19:10, 20:10}
    # Dictionary mapping a score to each letter based on how commonly the letter occurs in english words
    LETTERSCORE = {'A':1, 'B':2, 'C':1, 'D':2, 'E':1, 'F':3, 'G':2, 'H':2, 'I':1, 'J':3, 'K':3, 'L':1, 'M':2, 'N':1, 'O':1, 'P':2, 'Q':3, 'R':1, 'S':1, 'T':1, 'U':1, 'V':3, 'W':3, 'X':3, 'Y':3, 'Z':3}
    LETTERCHALLENGELETTERS = ['A', 'C', 'E', 'I', 'L', 'N', 'O', 'R', 'S', 'T', 'U']
    __VOWELS = ['A', 'E', 'I', 'O', 'U']
    __EMPTY = ' '

    def __init__(self):
        # Initial attributes
        self.wordstack = []
        self.usedlocations = []
        self.words = []
        self._validwords = []
        self._temp_surr_rows = []
        self._temp_surr_cols = []
        self._wordstackcache = []
        self._wordscache = []
        self.__surrrows = []
        self.__surrcols = []

        self.timeup = False
        self.pause = False
        self.word = None
        self.client = None
        self.server = None
        self._gui = False
        self._clientwait = False
        self._multiplayersetup = False
        self._onlinestart = False
        self._startedflag = False
        self.__stoptimer = False
        self.__quit = False
        self.__continueselection = False
        self.__multiplayer = False

        self.time = 60
        self._totalscore = 0
        self._BoardSize = 7
        self._MinLength  = 3

        self._dictionary = SpellCheck()

############################
##### GAME SETUP ###########
############################

    # Representation of board for terminal game
    def __repr__(self):
        grid = "  " + " ".join(str(x+1) for x in range(self._BoardSize))
        for r in range(0, self._BoardSize):
            grid += f"\n{r+1} " + "┇".join(self._Board[r])
            if r != self._BoardSize - 1:
                dashes = "┅" * (2 * self._BoardSize - 1)
                grid += f"\n  {dashes}"
        return grid

    # Uses threading to run in the background, started after initial game settings are entered
    # As this runs in the background, the time module performs a sleep for one second, decreasing a counter every time
    def __calculateTimeLeft(self):
        self.time_left = self.time
        while self.time_left > 1:
            if self.pause == False:
                self.time_left -= 1
                if self.__quit != True:
                    time.sleep(1)
            if self.__stoptimer == True:
                self.time_left = 1
                break
        self.__continueselection = True
        self.timeup = True
        if not self._gui:
            print("Game Over")
        self._endGame()

    ############################
    # Group B Skill 
    # Multi-Dimensional Arrays
    # Randomly generates letters in the board with a minimum of 4 vowels
    ############################
    def _createBoard(self):
        self._Board = [[self.__EMPTY for _ in range(self._BoardSize)] for _ in range(self._BoardSize)]
        # Always a minimum of 4 vowels
        for x in range(3):
            self._Board[random.randint(0, self._BoardSize-1)][random.randint(0, self._BoardSize-1)] = self.__VOWELS[random.randint(0,4)]
        for _ in range(self._BoardSize):
            for x in range(self._BoardSize):
                if self._Board[_][x] not in self.__VOWELS:
                    if len(self.LETTERS) != 26:
                        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                            if letter not in self.LETTERS:
                                self.LETTERS.append(letter)
                                self.LETTERS.sort()
                    self._Board[_][x] = self.LETTERS[random.randint(0,25)]
        if self.__multiplayer == False:
            self.timelimit = self.time
            self.__getValidWords()

    def at(self,row,col):
        row -= 1
        col -= 1
        return self._Board[row][col]

    ############################
    # Group A Skills
    # Lists
    # List Operations
    ############################
    def _getGameSettings(self):
        letters = []
        for row in range(self._BoardSize):
            for col in range(self._BoardSize):
                letters.append(self._Board[row][col])
        gamedata = (self._BoardSize, self._MinLength, self.time, letters)
        gamedata = str(gamedata)
        return gamedata

############################
##### PLAYING THE GAME #####
############################

    ############################
    # Group A Skill
    # Stacks
    # Runs until continueselection is false, used for terminal game
    # Prompts user for row and column inputs, then validates the selection within the rules of the game 
    # User can enter S or Q to submit the word or quit the game
    # Makes use of stack, adding selected letters to the stack to construct the word to be submitted
    ############################
    # Excellent Coding Style Demonstrated through:
    # Good Exception Handling
    # Defensive Programming
    ############################
    def __select(self):
        wordstack = []
        usedlocations = []
        temp = True
        while self.__continueselection == False:
            while True:
                if self.time_left == 0:
                    row=1
                    break
                try:
                    row = input("Enter row | S for submit word | Q for quit: ")
                    if row not in "SsQq": 
                        row = int(row)
                        if row < 1 or row > self._BoardSize:
                            raise ValueError
                except ValueError:
                    if self.time_left != 0:
                        print("Invalid Input! Please try again!")
                    continue
                break
            if row != "S" and row != "Q":
                if self.__continueselection == False:
                    col = ""
                    time.sleep(0.0001)
                    while True:
                        if self.time_left == 0:
                            col=1
                            break
                        try:
                            col = input("Enter column: ")
                            col = int(col)
                            if col < 1 or col > self._BoardSize:
                                raise ValueError
                        except ValueError:
                            if self.time_left != 0:
                                print("Invalid Input! Please try again!")
                            continue
                        break
                    if self.__continueselection == False:
                        self.letter = self._Board[row-1][col-1]
                        if len(wordstack) > 0:
                            temp = True
                        if len(wordstack) == 0:
                            rowcurr = row-1
                            colcurr = col-1
                            currpos = (rowcurr, colcurr)
                            usedlocations.append(currpos)
                            wordstack.append(self.letter)
                            print("Selected letter: " + str(self.letter))
                        if temp == True:
                            if (row-1) == rowcurr or (row-1)-1 == rowcurr or (row) == rowcurr:
                                if col-1 == colcurr or (col-1)-1 == colcurr or (col) == colcurr:
                                    if (row-1,col-1) not in usedlocations:
                                        rowcurr = row-1
                                        colcurr = col-1
                                        currpos = (rowcurr,colcurr)
                                        wordstack.append(self.letter)
                                        usedlocations.append(currpos)
                                        print("Selected letter: " + str(self.letter))
                                    else:
                                        if len(usedlocations) != 1:
                                            print("You have already used this letter!")
                                else:
                                    print("The letter needs to be next touching the previous letter picked!")
                            else:
                                    print("The letter needs to be next touching the previous letter picked!")
            else:
                if row == "S":
                    if len(wordstack) >= self._MinLength: 
                        self.word = ''.join([str(i) for i in wordstack])
                        self.word = str(self.word)
                        print("Submitting word: " + self.word)
                        return self.word
                    else:
                        print("Word is too short!")
                        self.word = None
                        wordstack.clear()
                if row == "Q":
                        self.time = 0
                        self.time_left = 0
                        self.__quit = True
                        self.word = None
                        break
                break

    # Asks for the game settings, performing data type and range check
    # Calls the select routine, which updates the self.word attribute with the selected word for this routine to check in the dictionary
    # When a correct word is found, using the PyDictionary module the definition is printed
    def __play(self):
        if self.__multiplayer == False:
            while True:
                try:
                    self._BoardSize = input("How big do you want the board to be? (5-10): ")
                    self._MinLength = input("What do you want the minimum word length to be?:  ")
                    self.time = input("How long should the time limit be?: ")
                    self._BoardSize = int(self._BoardSize)
                    self._MinLength = int(self._MinLength)
                    self.time = int(self.time)
                    if not ((self._BoardSize >= 5 and self._BoardSize <= 10) and (self._MinLength >= 0 and self._MinLength <= 10) and (self.time > 0)):
                        raise ValueError
                except ValueError:
                    print('''
                    
ERROR: One or more of the following not met:
-> Board Size needs to be between 5 and 10 inclusive
-> Minimum Length needs to be between 0 and 10 inclusive
-> Time Limit needs to be greater than 0
                    
                    ''')
                    continue
                break
            self._createBoard()
        self.words = []
        start = input("Please enter 'start' to begin playing!: ").lower()
        if start == "start":
            print(self)
            timer_thread = threading.Thread(target = self.__calculateTimeLeft)
            timer_thread.start()
            while self.time_left-1 > 0:
                self.__select()
                if self.word:
                    if self._dictionary.check_word(self.word.lower()):
                        print("Correct word!")
                        self.words.append(self.word)
                        self._getDefinition(PyDictionary.meaning(self.word.lower(),disable_errors=True))
                    else:
                        print("Invalid word!")
        else:
            while start != "start":
                start = input("Invalid input! Please enter 'start' to begin playing!: ").lower()
            print(self)
            timer_thread = threading.Thread(target = self.__calculateTimeLeft)
            timer_thread.start()
            while self.time_left-1 > 0:
                self.__select()
                if self.word:
                    if self._dictionary.check_word(self.word.lower()):
                        print("Correct word!")
                        self.words.append(self.word)
                        self._getDefinition(PyDictionary.meaning(self.word.lower(),disable_errors=True))
                    else:
                        print("Invalid word!")

    #########################################
    # Excellent Coding Style Demonstrated through:
    # Subroutine with appropriate interface
    # Loosely Coupled Module
    #########################################
    def _getDefinition(self, msg):
        count = 0
        msg = str(msg)
        newmsg = ""
        if msg == "None" or None:
            newmsg = "No definition available for this word!"
        else:
            for letter in msg:
                if letter not in "'{][}#;',/.!":
                    newmsg += letter
                if letter == ",":
                    break
        for letter in newmsg:
            if letter in "()":
                count += 1
        if count == 1:
            newmsg += ")"
        if not self._gui:
            print("\n" + newmsg + "\n")
            print(self)
        else:
            return newmsg

    # Starts the timer thread which decrements a counter by one every second using time module
    def _doStart(self):
        timer_thread = threading.Thread(target = self.__calculateTimeLeft)
        timer_thread.start()
        self._startedflag = True

    # Performs a similar algorithm to the other select routine but for the GUI game
    def _doLetterClick(self,row,col):
        self.usedletter = False
        self.nottouching = False
        temp = False
        if self.__continueselection == False:
                        self.letter = self._Board[int(row)-1][col-1]
                        if len(self.wordstack) > 0:
                            temp = True
                        if len(self.wordstack) == 0:
                            self.__selectedrow = int(row)-1
                            self.__selectedcol = col-1
                            self.currpos = (self.__selectedrow, self.__selectedcol)
                            self.usedlocations.append(self.currpos)
                            self.wordstack.append(self.letter)
                        if temp == True:
                            if (int(row)-1) == self.__selectedrow or (int(row)-1)-1 == self.__selectedrow or (int(row)-1)+1 == self.__selectedrow:
                                if col-1 == self.__selectedcol or (col-1)-1 == self.__selectedcol or (col-1)+1 == self.__selectedcol:
                                    if ((int(row)-1),col-1) not in self.usedlocations:
                                        self.__selectedrow = int(row)-1
                                        self.__selectedcol = col-1
                                        self.currpos = (self.__selectedrow,self.__selectedcol)
                                        self.wordstack.append(self.letter)
                                        self.usedlocations.append(self.currpos)
                                    else:
                                        if len(self.usedlocations) != 1:
                                            self.usedletter = True
                                else:
                                    self.nottouching = True
                            else:
                                    self.nottouching = True

    # Checks the word currently stored in the self.word attribute in the dictionary
    def _doSubmit(self):
        self.tooshort = False
        self.correct = False
        if len(self.wordstack) >= self._MinLength: 
            self.word = ''.join([str(i) for i in self.wordstack])
            self.word = str(self.word)
            self.currword = str(self.word)
            self.usedlocations = []
            self.wordstack = []
            if self.word not in self.words:
                if self._dictionary.check_word(self.word.lower()):
                    self.correct = True
                    self.words.append(self.word)
                    try:
                        self.meaning = PyDictionary.meaning(self.word.lower(),disable_errors=True)
                    except:
                        self.meaning = "None"
                    self.word = ""
                else:
                    self.word = ""
            else:
                self.word = ""        
        else:
            self.word = None
            self.wordstack.clear()
            self.usedlocations.clear()
            self.tooshort = True

#########################
##### CLIENT/SERVER #####
#########################

    ############################
    # Group A Skill 
    # Dynamic Generation of Objects
    # Asks the user if they want to play an online game
    # User has choice to join or host the game, if host then an instance of host is created and a thread running the server opens in the background
    # If the user wants to join a game, it creates an instance of the client and calls a routine to setup the game, receiving data from the host
    ############################
    def _checkMultiplayer(self):
        doNetwork = input("Do you want to play online against another client? (Y or N): ")
        if doNetwork == "Y":
            self.__multiplayer = True
            doHost = input("Do you want to host a game or join a game? (H or J): ")
            if doHost == "H":
                self._multiplayersetup = True
                self.__setup()
                if self._getGameSettings():
                    self.server = Host()
                    thread = threading.Thread(target=self.server.startServer)
                    thread.start()
                    print("Waiting for second user to connect!")
                    while self.server.getMsg("User 2 has connected") == False:
                        pass
                    self.server.broadcastMessage(self._getGameSettings())
                    self.__play()
            else:
                self.client = Client()
                self.client.send("User 2 has connected")
                self._setupClientGame(self.client.mostRecentMsg)
                self.__play()
        else:
            self.__setup()

    # Ends threads in host class
    def _endServer(self):
        if self.server:
            self.server.endConnection = True
            if self._onlinestart == False:
                self._onlinestart = True

    # Runs in the background when started forcing the host to wait for the client to connect
    def _checkForClientThread(self):
        while self.server.getMsg("User 2 has connected") == False and self.server.endConnection == False:
            pass
        if not self.server.endConnection:
            self._createMultiplayerGame()

    # Begins threads after online game has been set up
    def _createServer(self):
        self.__multiplayer = True
        self.server = Host()
        thread = threading.Thread(target=self.server.startServer)
        thread.start()
        self._createBoard()
        thread2 = threading.Thread(target=self._checkForClientThread)
        thread2.start()        

    # If server, broadcasts the game data for the client to receive
    # If client, receives the game data and creates a game using the settings
    def _createMultiplayerGame(self):
        if self.server != None:
            self.server.broadcastMessage(self._getGameSettings())
            self._onlinestart = True
            self.timelimit = self.time
        elif self.client != None:
            self._setupClientGame(self.client.mostRecentMsg)
            self._onlinestart = True
            self.timelimit = self.time

    # Host waits for message from client saying the user has connected before allowing the game to start
    def _joinServer(self):
        self.client = Client()
        self.client.send("User 2 has connected")
        time.sleep(0.1)
        self._createMultiplayerGame()

    # Host creates the game, client plays on the settings the host chooses
    def __setup(self):
        if self.__multiplayer == False:
            self.__play()
        else:
            if self._multiplayersetup == True:
                while True:
                    try:
                        self._BoardSize = input("How big do you want the board to be? (5-9): ")
                        self._MinLength = input("What do you want the minimum word length to be?:  ")
                        self._BoardSize = int(self._BoardSize)
                        self._MinLength = int(self._MinLength)
                        if not ((self._BoardSize >= 5 and self._BoardSize <= 10) and (self._MinLength >= 0 and self._MinLength <= 9)):
                            raise ValueError
                    except ValueError:
                        print('''
                        
    ERROR: One or more of the following not met:
    -> Board Size needs to be between 5 and 9 inclusive
    -> Minimum Length needs to be between 0 and 10 inclusive
                        
                        ''')
                        continue
                    break
            self.time = 60
            self._createBoard()
            self._multiplayersetup = False

    # Creates a list of the settings to be sent to the client to then create the client game with the same board and settings
    def _setupClientGame(self, gamedata):
        gamedatalist = []
        for item in gamedata:
            if item not in "/,.[]]()'" and item != " ":
                gamedatalist.append(item)
        self._BoardSize = int(gamedatalist[0])
        self._MinLength = int(gamedatalist[1])
        self.time = (gamedatalist[2] + gamedatalist[3])
        self.time = int(self.time)
        for x in range(4):
            gamedatalist.pop(0)
        self._Board = [[self.__EMPTY for _ in range(self._BoardSize)] for _ in range(self._BoardSize)]
        for row in range(self._BoardSize):
            for col in range(self._BoardSize):
                self._Board[row][col] = gamedatalist[0]
                gamedatalist.pop(0)

##############################
##### FINISHING THE GAME #####
##############################

    # When either client or server finishes the game, the total score they achieved is sent to the other player
    def _doFinish(self):          
        self.time_left = 1
        self.time = 1
        self.__quit = True
        self._startedflag = False
        self._getFinalScore(0,0)
        if self.server or self.client:
            if self.server != None:
                self.server.broadcastMessage(str(self._totalscore))
            if self.client != None:
                self.client.send(str(self._totalscore))
            if self.server != None:
                while self.server.msg == "User 2 has connected":
                    time.sleep(0.5)
            if self.client != None:
                while self.client.mostRecentMsg == None:
                    time.sleep(0.5)
            if self.server != None:
                otherscore = self.server.msg
                return otherscore
            if self.client != None:
                otherscore = self.client.mostRecentMsg
                return otherscore

    # Depending on if the game is terminal or GUI, a winner is determined between both players (if online) and the game ends
    # If the game is not online, the total score is calculated the user has to option to see other words they could have found
    def _endGame(self):
            if self.__multiplayer == False or self._gui == True:
                self._getFinalScore(0,0)
                if not self._gui:
                    print("Total score was: " + str(self._totalscore))
                    if not self.__quit:
                        print("Press Enter to continue.")
                self.time_left = 0
                self.__continueselection = True
                self.__quit = True
                self.word = None
                if self._gui == False:
                    getwords = input(("Do you want to see other possible words? (Y or N): ")).lower()
                    if getwords == "y":
                        stringofwords = ""
                        for word in self._validwords:
                            if self._validwords.index(word) != len(self._validwords)-1:
                                stringofwords += word[0].upper() + word[1:] + ", "
                            else:
                                stringofwords += word[0].upper() + word[1:] + "."
                        print(stringofwords)
                    else:
                        pass
            else:
                self._getFinalScore(0,0)
                self.__continueselection = True
                self.__quit = True
                self.word = None
                print(f"Your total score was: {self._totalscore}")
                if self.server or self.client:
                    print("Waiting for other player to finish...")
                if self.server != None:
                    self.server.broadcastMessage(str(self._totalscore))
                if self.client != None:
                    self.client.send(str(self._totalscore))
                if self.server != None:
                    while self.server.msg == "User 2 has connected" or self.server.msg == '':
                        pass
                    print(f"The other player obtained a score of {self.server.msg}")
                    if int(self.server.msg) > self._totalscore:
                        print("You lost!")
                    elif int(self.server.msg) < self._totalscore:
                        print("You won!")
                    else:
                        print("You both got the same score!")
                    self.server.doExit()
                    self.server.endConnection = True
                if self.client != None:
                    print(f"The other player obtained a score of {self.client.mostRecentMsg}")
                    if int(self.client.mostRecentMsg) > self._totalscore:
                        print("You lost!")
                    elif int(self.client.mostRecentMsg) < self._totalscore:
                        print("You won!")
                    else:
                        print("You both got the same score!")
                    self.client.endConnection = True
                print("Press Enter to close.")

    ############################
    # Group A Skill 
    # Recursive Algorithm to establish score
    # Makes use of dictionaries to retrieve the score associated to a letter and the score associated to the length of a word
    # Continues until the base case is met, where n (representing index in list of words) is equal to the length of the words list
    ############################
    # Excellent Coding Style Demonstrated through:
    # Subroutine with appropriate interface
    ############################
    def _getFinalScore(self, score, n):
        wordscore = 0
        if n < len(self.words):
            for letter in self.words[n]:
                wordscore += self.LETTERSCORE[letter.upper()]
            wordscore *= self.WORDLENGTHMULTIPLIER[len(self.words[0])]
            score += wordscore
            n += 1
            self._getFinalScore(score, n)
        else:
            self._totalscore = score
        return self._totalscore

    ############################
    # Group A Skill
    # Complex user defined algorithm which in addition to the algorithm below to check surrounding letters, finds other words that the user could have found
    # Iterates through all the letters in every word in the dictionary
    # Initially checks whether the first letter of the current word is in the grid
    # Checks whether the second letter of the word is in the grid
    # Checks whether the second letter of the word is in a position adjacent to the first letter
    # If true, the second letter becomes the first letter and the second letter becomes the next letter in the word
    # A counter increases every time 
    # A combination is accepted and a word is deemed valid if this counter is equal to the length of the word
    # A combination is rejected if the next letter does not surround the current letter, in which case a flag is marked as true and the process continues
    # There may be multiple instances of the first letter in the word in the grid, therefore the process then has to repeat on the same word but for the letter in a different grid location
    # The final result is a list of words that obey the rules of the game that the user could have found
    ############################
    def __getValidWords(self):
        letters = []
        validwords = []
        for row in range(self._BoardSize):
            for col in range(self._BoardSize):
                letters.append(self._Board[row][col].lower())
        for word in self._dictionary.wordset:
            self.__usedcoords = []
            self.__foundcounter = 0
            first_rows = []
            first_cols = []
            n=0
            i=1
            for row in range(self._BoardSize):
                for col in range(self._BoardSize):
                    if self._Board[row][col].lower() == word[0]:
                        first_rows.append(row)
                        first_cols.append(col)
            for x in range(len(first_rows)):
                if self.__checkSurroundingLetters(word[1], first_rows[x], first_cols[x]) == True:
                    self._temp_surr_rows = self.__surrrows
                    self._temp_surr_cols = self.__surrcols
                    while n != -1:
                        for x in range(len(self._temp_surr_rows)):
                            if word not in validwords:
                                if i != len(word):
                                    if i >= 2:
                                        self._temp_surr_rows = self.__surrrows
                                        self._temp_surr_cols = self.__surrcols
                                    try:
                                        curr_row = self._temp_surr_rows[x]
                                        curr_col = self._temp_surr_cols[x]
                                    except IndexError:
                                        try:
                                            curr_row = self._temp_surr_rows[x-1]
                                            curr_col = self._temp_surr_cols[x-1]
                                        except IndexError:
                                            n=-1 # Array would be empty so word isn't in grid anyway
                                    if i == 1 and len(word) != 2:
                                        if self.__checkSurroundingLetters(word[i+1], curr_row, curr_col) == True:
                                            if self.__foundcounter == len(word)-1:
                                                validwords.append(word)
                                                n=-1
                                            i += 1
                                            if i == len(word):
                                                n = -1
                                                for letter in word:
                                                    if letter in letters:
                                                        if word not in validwords:
                                                            validwords.append(word)
                                                            self.__surrcols = []
                                                            self.__surrcols = []
                                                            self._temp_surr_cols = []
                                                            self._temp_surr_rows = []
                                        else:
                                            self.__surrrows = []
                                            self.__surrcols = []
                                            n = -1
                                    elif i >= 1 or len(word) == 2:
                                        if i+1 == len(word):
                                            validwords.append(word)
                                            n=-1
                                        if word not in validwords:
                                            if self.__checkSurroundingLetters(word[i+1], curr_row, curr_col) == True:
                                                if self.__foundcounter == len(word):
                                                    validwords.append(word)
                                                i += 1
                                                if i == len(word):
                                                    n = -1
                                                    if len(word) == 2:
                                                        for letter in word:
                                                            if letter in letters:
                                                                if word not in validwords:
                                                                    validwords.append(word)
                                                                    self.__surrcols = []
                                                                    self.__surrcols = []
                                                                    self._temp_surr_cols = []
                                                                    self._temp_surr_rows = []
                                                    else:
                                                        validwords.append(word)
                                            else:
                                                self.__surrrows = []
                                                self.__surrcols = []
                                                n = -1
                            else:
                                n = -1
        for word in validwords:
            if len(word) < self._MinLength:
                validwords.remove(word)
        self._validwords = validwords

    # Calculates surrounding positions on the board to a given position from row and column passed in as parameters
    # Uses nextletter parameter to see if the next letter of the word is in any adjacent positions to the row and column passed in
    ############################
    # Excellent Coding Style Demonstrated through:
    # Subroutine with appropriate interface
    ############################
    def __checkSurroundingLetters(self,nextletter,row,col):
        self.__surrrows = []
        self.__surrcols = []
        surrletters = []
        if (row,col) in self.__usedcoords:
            return False
        else:
            self.__usedcoords.append((row,col))
            if row == 0 and col != 0 and col != self._BoardSize-1:
                next_surrounding = [(row, col-1), (row, col+1), (row+1,col+1), (row+1, col), (row+1, col-1)]
            elif row == self._BoardSize-1 and col != 0 and col != self._BoardSize-1:
                next_surrounding = [(row, col-1), (row, col+1), (row-1,col+1), (row-1, col), (row-1, col-1)]
            elif col == 0 and row != 0 and row != self._BoardSize-1:
                next_surrounding = [(row+1, col), (row-1, col), (row+1, col+1), (row-1, col+1), (row, col+1)]
            elif col == self._BoardSize-1 and row != 0 and row != self._BoardSize-1:
                next_surrounding = [(row+1, col), (row-1, col), (row+1, col-1), (row-1, col-1), (row, col-1)]
            elif row == self._BoardSize-1 and col == self._BoardSize-1:
                next_surrounding = [(row-1, col), (row, col-1), (row-1, col-1)]
            elif row == self._BoardSize-1 and col == 0:
                next_surrounding = [(row-1, col), (row, col+1), (row-1, col+1)]
            elif row == 0 and col == self._BoardSize-1:
                next_surrounding = [(row+1, col), (row, col-1), (row+1, col-1)]
            elif row == 0 and col == 0:
                next_surrounding = [(row+1, col), (row, col+1), (row+1, col+1)]
            else:
                next_surrounding = [(row, col-1), (row, col+1), (row+1,col+1), (row+1, col), (row-1, col), (row-1, col-1), (row-1, col+1), (row+1, col-1)]
            for coord in next_surrounding:
                surrletters.append(self._Board[coord[0]][coord[1]].lower())
            if nextletter in surrletters:
                for coord in next_surrounding:
                    if self._Board[coord[0]][coord[1]].lower() == nextletter:
                        if (coord[0],coord[1]) not in self.__usedcoords:
                            self.__surrrows.append(coord[0])
                            self.__surrcols.append(coord[1])
            if self.__surrrows != []:
                self.__foundcounter += 1
                return True
            else:
                self.__foundcounter = 0
                return False

############################
# Group A Skill
# OOP: Classes
############################

class AI():
    ############################
    # Group A Skill
    # AI
    # Logic behind the AI Modes in the GUI game
    # Uses random number generation depending on difficulty to simulate whether the AI finds a word or not within the list of valid words
    # The user then has to try and beat this score
    ############################
    ############################
    # Excellent Coding Style Demonstrated through:
    # Subroutine with appropriate interface
    # Loosely Coupled Module
    ############################
    def _beatTheirScore(self, validwords, timeleft):
        words = []
        for word in validwords:
            if timeleft > 179:
                randint = random.randint(1,8)
            elif 179 >= timeleft >= 119:
                randint = random.randint(1,9)
            elif 119 > timeleft >= 59:
                randint = random.randint(1,10)
            elif timeleft < 59:
                randint = random.randint(1,6)
            if randint == 1:
                words.append(word)
        letterscore = 0
        wordscore = 0
        totalscore = 0
        for word in words:
            for letter in word:
                letterscore += Game.LETTERSCORE[letter.upper()]
            letterscore *= Game.WORDLENGTHMULTIPLIER[len(word)]
            wordscore += letterscore
            letterscore = 0
            totalscore += wordscore
        scoreToBeat = totalscore
        if len(validwords) > 50:
            scoreToBeat = math.trunc(scoreToBeat / 1.5)
        while scoreToBeat > 700:
            scoreToBeat -= 50
        if timeleft < 120:
            while scoreToBeat < 325:
                scoreToBeat += 50
        return scoreToBeat

    # Sets the AI difficulty
    # The amount of attempts the AI gets at finding a word increases as the difficulty gets harder
    ############################
    # Excellent Coding Style Demonstrated through:
    # Subroutine with appropriate interface
    # Cohesive Module
    # Loosely Coupled Module
    ############################
    def _setAITurnTimes(self, difficulty, aitimes):
        if difficulty == "Easy":
            difficulty = 3
        elif difficulty == "Medium":
            difficulty = 4
        elif difficulty == "Hard":
            difficulty = 6
        for x in range(difficulty):
            time = random.randint(1,14)
            while time in aitimes:
                time = random.randint(1,14)
            aitimes.append(time)
        return aitimes

    # Uses random number generation and factors in how many words there are to be found to determine whether the AI finds a word on each call
    ############################
    # Excellent Coding Style Demonstrated through:
    # Subroutine with appropriate interface
    # Cohesive Module
    # Loosely Coupled Module
    ############################
    def _doVersusTurn(self, turncount, validwords, minlength, aifound, words):
            num = random.randint(1,3)
            if num != 3:
                wordtopick = random.randint(1,len(validwords))
                word = validwords[wordtopick-1]
                midpoint = len(validwords) / 2
                if wordtopick-1 < int(math.trunc(midpoint)) or turncount <= 1:
                    if len(word) >= minlength and word not in aifound and word.upper() not in words:
                        return word
                    else:
                        return None
                else:
                    return None
            else:
                return None

# Allows code to be imported, creates initial instance of the game
if __name__ == "__main__":
    g = Game()
    print(g)