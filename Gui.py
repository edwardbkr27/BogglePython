from Game import Game
from Game import AI
from Game import Database
from abc import ABC, abstractmethod
from tkinter import *
from itertools import *
import time as time
import threading
import random
import pickle
from datetime import date

############################
# Group A Skill
# OOP: Classes
############################

class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError()

############################
# Group A Skill 
# OOP: Inheritance
############################

############################
# Group A Skill
# OOP: Classes
############################

class Gui(Ui):
    ############################
    # Group A Skill 
    # Complex Graphical Interface
    ############################
    ############################
    # Good Coding Style demonstrated through:
    # Use of Constants
    ############################
    BACKGROUND = "#7891c4"
    FOREGROUND = "white"
    FONT = "Calibri"

    def __init__(self):
        # Creating the root (my main menu) of the graphical interface, every other window stems from the root
        root = Tk()
        root.title("Main Menu")
        root.configure(background="#9bafd9")
        frame = Frame(root)
        frame.configure(background="#9bafd9")
        frame.pack()
        root.geometry("800x600")
        self.__root = root

        # Initialising tkinter StringVars which are representations of text in the interface
        self.__correctcolour = StringVar()
        self.__incorrectcolour = StringVar()
        self.__wordcount = StringVar()
        self.__timeleft = StringVar()
        self.__aidifficulty = StringVar()
        self.__pausetext = StringVar()
        self.__showdefinitions = StringVar()
        self.__gametype = StringVar()
        self.__difficulty = StringVar()
        self.__gamemode = StringVar()
        self.__changeboard = StringVar()
        self.__multiplayergamemode = StringVar()
        self.__gamemodeinfo = StringVar()

        # Setting some StringVars to default values
        self.__correctcolour.set("spring green")
        self.__incorrectcolour.set("red")
        self.__pausetext.set("Pause")
        self.__multiplayergamemode.set("None")

        self.__buttontoggle = False
        self.__gamestarted = False
        self.__loadinggame = False
        self.__savedgame = False
        self.__stoptimer = False
        self.__multiplayer = False
        self.__scorebeaten = False
        self.__onevsone = False
        self.__aiturn = False
        self.__quitting = False
        self.__online = False
        self.__inprogress = False
        self.__loadproceed = False
        self.__cancelOnline = False

        self.__clicked = []
        self.__aifound = []

        self.__timeadd = 0
        self.__scoreToBeat = 0
        self.__aiturncounter = 0
        self.__loginattempts = 0
        self.__gameduration = 0
        self.__id = -1

        self.__username = ""
        self.__password = ""

        ############################
        # Group A Skill 
        # Dynamic Generation of Objects
        # Creating instances of AI, Database and Game Classes
        ############################
        self.__AI = AI()
        self.__game = Game()
        self.__database = Database()

        # Allows the game class to know the game is run with the GUI so some terminal game based methods don't need to run
        self.__game._gui = True

        # Loading the images that are overlayed onto buttons in the main menu
        self.__singleplayerimg = PhotoImage(file='images/singleplayer.png')
        self.__multiplayerimg = PhotoImage(file='images/multiplayer.png')
        self.__quitimg = PhotoImage(file='images/quit.png')
        self.__howtoplayimg = PhotoImage(file='images/howtoplay.png')
        self.__settingsimg = PhotoImage(file='images/settings.png')
        self.__loginimg = PhotoImage(file='images/login.png')
        self.__loadsaveimg = PhotoImage(file='images/loadsave.png')
        self.__boggleimg = PhotoImage(file='images/boggle.png')
        self.__helpimg = PhotoImage(file='images/help.png')

        # Overlaying images onto the buttons
        # Buttons can display text or an image and when pressed can execute another subroutine
        # Lambda can be used to execute multiple subroutines with one button push
        Label(root, image=self.__boggleimg, border=0,background='#9bafd9').pack(pady=15)
        Singleplayer = Button(root,image=self.__singleplayerimg,border=0,background='#9bafd9',command=self.__singleplayerButton)
        Singleplayer.place(relx=0.5, rely=0.35, anchor=CENTER)
        Multiplayer = Button(root,image=self.__multiplayerimg,border=0,background='#9bafd9',command=self.__multiplayerButton)
        Multiplayer.place(relx=0.5, rely=0.4, anchor=CENTER)
        Load = Button(root,image=self.__loadsaveimg,border=0,background='#9bafd9',command=self.__loadButton)
        Load.place(relx=0.5, rely=0.45, anchor=CENTER)
        Settings = Button(root,image=self.__settingsimg,border=0, background='#9bafd9',command=self.__settingsButton)
        Settings.place(relx=0.5, rely=0.5, anchor=CENTER)
        Login = Button(root,image=self.__loginimg,border=0,background='#9bafd9',command=self.__loginButton)
        Login.place(relx=0.5, rely=0.55, anchor=CENTER)   
        Howtoplay = Button(root,image=self.__howtoplayimg,border=0,background='#9bafd9',command=self.__helpCallback)
        Howtoplay.place(relx=0.5, rely=0.6, anchor=CENTER)               
        Quit = Button(root,image=self.__quitimg,border=0,background='#9bafd9',command=self.__quitCallback)
        Quit.place(relx=0.5, rely=0.65, anchor=CENTER)

#############################
##### MAIN MENU BUTTONS #####
#############################
# Clicking a main menu button calls another method to make
# sure that no game is in progress before performing button function
    def __singleplayerButton(self):
        if not self.__inprogress:
            self.__resetGame() 
            self.__gametypeCallback()
        else:
            window = Toplevel(self.__root)
            window.title("Error!")
            window.geometry("250x75")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Please close the game window to use this!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

    def __multiplayerButton(self):
        if not self.__inprogress:
            self.__resetGame() 
            self.__multiplayerCallback()
        else:
            window = Toplevel(self.__root)
            window.title("Error!")
            window.geometry("250x75")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Please close the game window to use this!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

    def __loadButton(self):
        if not self.__inprogress:
            self.__getFileName()
        else:
            window = Toplevel(self.__root)
            window.title("Error!")
            window.geometry("250x75")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Please close the game window to use this!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)
    
    def __settingsButton(self):
        if not self.__inprogress:
            self.__settingsCallback()
        else:
            window = Toplevel(self.__root)
            window.title("Error!")
            window.geometry("250x75")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Please close the game window to use this!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

    def __loginButton(self):
        if not self.__inprogress:
            self.__loginCallback()
        else:
            window = Toplevel(self.__root)
            window.title("Error!")
            window.geometry("250x75")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Please close the game window to use this!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)


####################
##### ACCOUNTS #####
####################

    # Creates the window for the user to enter credentials
    # Uses entry widgets in which the user can enter text to then be stored to a variable/attribute
    def __loginCallback(self):
        window = Toplevel(self.__root)
        window.title("Log in")
        window.geometry("600x400")
        window.configure(bg=self.BACKGROUND)
        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack()
        login_label = Label(window, text="Log in", bg=self.BACKGROUND, fg=self.FOREGROUND)
        login_label.pack(pady=10)
        name_label = Label(window, text="Username", bg=self.BACKGROUND, fg=self.FOREGROUND)
        name_label.pack(pady=10)
        self.__usernameEntry = Entry(window, width=25)
        self.__usernameEntry.pack()
        password_label = Label(window, text="Password", bg=self.BACKGROUND, fg=self.FOREGROUND)
        password_label.pack(pady=5)
        self.__passwordEntry = Entry(window, width=25, show="*")
        self.__passwordEntry.pack()
        login_btn = Button(window, text="Log in", command=lambda:[self.__loginCheck(), window.destroy()], background=self.BACKGROUND)
        login_btn.pack(pady=7) 
        register_btn = Button(window, text="Register", command=lambda:[self.__registerCallback(), window.destroy()], background=self.BACKGROUND)
        register_btn.pack(side="top")

        Button(window, text="Exit",command=window.destroy, background=self.BACKGROUND).pack(side=BOTTOM,pady=5)       

    def __registerCallback(self):
        window = Toplevel(self.__root)
        window.title("Create Account")
        window.geometry("600x400")
        window.configure(bg=self.BACKGROUND)
        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack()
        login_label = Label(window, text="Register", bg=self.BACKGROUND, fg=self.FOREGROUND)
        login_label.pack(pady=10)
        name_label = Label(window, text="Username", bg=self.BACKGROUND, fg=self.FOREGROUND)
        name_label.pack(pady=10)
        self.__usernameEntry = Entry(window, width=25)
        self.__usernameEntry.pack()
        password_label = Label(window, text="Password", bg=self.BACKGROUND, fg=self.FOREGROUND)
        password_label.pack(pady=5)
        self.__passwordEntry = Entry(window, width=25, show="*")
        self.__passwordEntry.pack()
        login_btn = Button(window, text="Create Account", command=self.__registerCheck, background=self.BACKGROUND)
        login_btn.pack(pady=25)

    # Calls a method from the game class to add the credentials to the database
    # If the name is already in the database, a failure message pops up
    ############################
    # Excellent Coding Style Demonstrated through:
    # Defensive Programming
    ############################
    def __registerCheck(self):
        if not isinstance(self.__correctcolour, str):
            self.__correctcolour = self.__correctcolour.get()
        if not isinstance(self.__incorrectcolour, str):
            self.__incorrectcolour = self.__incorrectcolour.get()
        if not isinstance(self.__usernameEntry, str):
            self.__usernameEntry = self.__usernameEntry.get()
        if not isinstance(self.__passwordEntry, str):
            self.__passwordEntry = self.__passwordEntry.get()
        if self.__database._checkIfUsernameTaken(self.__usernameEntry):
            self.__registerFailure()
        else:
            userinfo = self.__database._doRegister(self.__usernameEntry, self.__passwordEntry, self.__correctcolour, self.__incorrectcolour)
            self.__username = userinfo[0]
            self.__password = userinfo[1]
            self.__correctcolour = userinfo[2]
            self.__incorrectcolour = userinfo[3]
            self.__id = self.__database._getIDFromUsername(self.__username)
            self.__registerSuccess()

    # The data type of the relevant attributes/variables need to be checked
    # Tkinter StringVars have to be converted into a string using the ".get" method before they can be used
    # Making use of the isinstance method to check the data type
    # The password is encoded into utf-8 so that it can then be encrypted
    ############################
    # Excellent Coding Style Demonstrated through:
    # Defensive Programming
    # Good Exception Handling
    ############################
    def __loginCheck(self):
        self.__loginattempts += 1
        if not isinstance(self.__username, str):
            username = self.__usernameEntry.get()
            password = self.__passwordEntry.get()
            password = password.encode('utf-8')
        elif self.__loginattempts >= 1:
            try:
                if not isinstance(self.__usernameEntry, str):
                    username = self.__usernameEntry.get()
                    password = self.__passwordEntry.get()
                    password = password.encode('utf-8')   
                else:
                    username = self.__usernameEntry
                    password = self.__passwordEntry
                    password = password.encode('utf-8')   
            except TclError:
                username = self.__usernameEntry
                password = self.__passwordEntry
                password = password.encode('utf-8')       
        else:
            username = self.__username
            password = self.__password
        userinfo = self.__database._doLogin(username, password)
        if userinfo != None:
            self.__username = userinfo[0]
            self.__password = userinfo[1]
            self.__id = userinfo[2]
            self.__correctcolour = StringVar()
            self.__correctcolour.set(userinfo[3])
            self.__incorrectcolour = StringVar()
            self.__incorrectcolour.set(userinfo[4])
            self.__loginSuccess()
        else:
            self.__loginFailure()

    ############################
    # Excellent Coding Style Demonstrated through:
    # Subroutines with appropriate interfaces
    # Cohesive Modules
    # Moduels with common purpose grouped
    ############################

    def __loginSuccess(self):
        window = Toplevel(self.__root)
        window.title("Login Status")
        window.geometry("150x75")
        window.configure(bg=self.BACKGROUND)
        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack()
        login_label = Label(window, text="Login Successful!", bg=self.BACKGROUND, fg="#08fa00")
        login_label.pack()
        username_label = Label(window, text="Logged in as: " + str(self.__username),  bg=self.BACKGROUND, fg="#08fa00")
        username_label.pack()
        Button(window, text="Exit",command=window.destroy, background=self.BACKGROUND).pack(side=BOTTOM,pady=5)   

    def __registerSuccess(self):
        window = Toplevel(self.__root)
        window.title("Login Status")
        window.geometry("150x75")
        window.configure(bg=self.BACKGROUND)
        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack()
        login_label = Label(window, text="Register Successful!", bg=self.BACKGROUND, fg="#08fa00")
        login_label.pack()
        username_label = Label(window, text="You may now login!",  bg=self.BACKGROUND, fg="#08fa00")
        username_label.pack()
        Button(window, text="Exit",command=window.destroy, background=self.BACKGROUND).pack(side=BOTTOM,pady=5)   

    def __registerFailure(self):
        window = Toplevel(self.__root)
        window.title("Login Status")
        window.geometry("150x75")
        window.configure(bg=self.BACKGROUND)
        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack()
        login_label = Label(window, text="Register Failure!", bg=self.BACKGROUND, fg="#fa0000")
        login_label.pack()
        username_label = Label(window, text="Username already taken!",  bg=self.BACKGROUND, fg="#fa0000")
        username_label.pack()
        Button(window, text="Exit",command=window.destroy, background=self.BACKGROUND).pack(side=BOTTOM,pady=5)    

    def __loginFailure(self):
        window = Toplevel(self.__root)
        window.title("Login Status")
        window.geometry("150x50")
        window.configure(bg=self.BACKGROUND)
        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack()
        login_label = Label(window, text="Invalid Credentials!", bg=self.BACKGROUND, fg="#fa0000")
        login_label.pack()
        Button(window, text="Exit",command=window.destroy, background=self.BACKGROUND).pack(side=BOTTOM,pady=5)   

    # Feeds all the information about a game to a method in the game class to be added to the database
    def __addGameEntry(self):
        id = self.__id
        gamemode = self.__gamemode.get()
        difficulty = self.__difficulty.get()
        duration = self.__gameduration
        score = self.__game._totalscore
        wordsfound = self.__correctcounter
        if id == -1:
            pass
        else:
            today = date.today()
            datenow = today.strftime("%d/%m/%Y")
            self.__database._addGameEntry(id, gamemode, difficulty, duration, score, wordsfound, datenow)

    # The visual side of the previous games panel
    # If the user is logged in, the user can use a dropdown menu to select a gamemode to see previous games they have played
    # Calls the getPreviouslyPlayedGames method in the game class which returns data from both tables to then be displayed
    def __searchForGames(self):
        window = Toplevel(self.__root)
        window.geometry("725x900")
        window.configure(bg=self.BACKGROUND)
        window.grid_columnconfigure(2, weight=1)
        window.title(f"Previous Games on Gamemode: {self.__gamemodeToSearch.get()}")
        gameidcol = 0
        difficultycol = 2
        durationcol = 4
        wordsfoundcol = 6
        scorecol = 8
        datecol = 10
        gameid = Label(window, text="Game ID", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        gameid.grid(row=1,column=0, padx=30, pady=15)
        diff = Label(window, text="Difficulty", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        diff.grid(row=1,column=2, padx=30, pady=15)
        duration = Label(window, text="Duration", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        duration.grid(row=1,column=4, padx=30, pady=15)
        wordsfound = Label(window, text="Words Found", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        wordsfound.grid(row=1,column=6, padx=30, pady=15)
        scoremainlabel = Label(window, text="Score", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        scoremainlabel.grid(row=1,column=8, padx=30, pady=15)
        datemainlabel = Label(window, text="Date", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        datemainlabel.grid(row=1,column=10, padx=30, pady=15)
        data = self.__database._getPreviouslyPlayedGames(self.__username, self.__gamemodeToSearch.get())
        for dataset in data:
            fg = self.FOREGROUND
            if data.index(dataset) < 15:
                userid = data[0]
                gameid = dataset[1]
                difficulty = dataset[2]
                duration = dataset[3]
                score = dataset[4]
                wordsfound = dataset[5]
                date = dataset[6]
                gameidlabel = Label(window, text=str(gameid), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                gameidlabel.grid(row=(data.index(dataset)+2), column=gameidcol, padx=35, pady=15)
                difficultylabel = Label(window, text=str(difficulty), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                difficultylabel.grid(row=(data.index(dataset)+2), column=difficultycol, padx=35, pady=15)
                durationlabel = Label(window, text=str(duration) + "s", font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                durationlabel.grid(row=(data.index(dataset)+2), column=durationcol, padx=35, pady=15)
                wordsfoundlabel = Label(window, text=str(wordsfound), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                wordsfoundlabel.grid(row=(data.index(dataset)+2), column=wordsfoundcol, padx=35, pady=15)
                scorelabel = Label(window, text=str(score), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                scorelabel.grid(row=(data.index(dataset)+2), column=scorecol, padx=35, pady=15)
                datelabel = Label(window, text=str(date), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                datelabel.grid(row=(data.index(dataset)+2), column=datecol, padx=35, pady=15)
        Button(window, text="<- Back",command=lambda:[window.destroy()], background=self.BACKGROUND).grid(row=0,column=0,columnspan=10,sticky="nw")

    def __saveSettingsToAccount(self):
        correctcolour = self.__correctcolour.get()
        incorrectcolour = self.__incorrectcolour.get()
        self.__database._updateSettings(correctcolour, incorrectcolour, self.__id)

###############################################
##### SETTINGS/PREFERENCES/CREATING GAMES #####
###############################################

    # User settings, allowing the user to select a correct/incorrect colour which is saved to the account
    # User can also access previous games panel from here
    def __settingsCallback(self):
        if self.__inprogress != True:
            gamemodes = ["None", "Time Battle", "One-Time Use", "Length Challenge", "Letter Challenge", "AI: 1v1", "AI: Beat Their Score"]
            self.__gamemodeToSearch = StringVar()
            self.__gamemodeToSearch.set("None")
            self.__colours = ["ghost white", "peach puff", "slate gray", "navy", "cornflower blue", "blue", "deep sky blue", "sky blue", "cyan", "dark green", "spring green", "green", "lime green", "yellow", "gold", "salmon", "tomato", "orange", "red", "hot pink", "dark violet", "purple", "black"]

            window = Toplevel(self.__root)
            window.title("Settings")
            window.geometry("450x300")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Change colours", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)

            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)

            correct = OptionMenu(window, self.__correctcolour, *self.__colours)
            correct.pack()

            incorrect = OptionMenu(window, self.__incorrectcolour, *self.__colours)
            incorrect.pack()

            if self.__username != "":
                Label(window, text=f"Search for Previous Games by Gamemode on Account: {self.__username}", bg=self.BACKGROUND, fg=self.FOREGROUND).pack(pady=10)
                gamemodeToSearch = OptionMenu(window, self.__gamemodeToSearch, *gamemodes).pack()
                Button(window, text="Search", command=self.__searchForGames).pack()


            Button(window, text="Exit",command=window.destroy).pack(side=BOTTOM)
            if self.__username != "":
                Button(window, text="Save Settings to Account", command=self.__saveSettingsToAccount).pack(side=BOTTOM)
        else:
            self.__consoleMsg("\nYou can't open the settings right now!")

    # Validates the settings the user wants to launch a game with
    def __checkSettings(self):
        if self.__inprogress != True:
            if self.__settingscheck == True:
                self.__playCallback()
            else:
                try:
                    if int(self.__boardsizesetting.get()) >= 5 and int(self.__boardsizesetting.get()) <= 10:
                        if int(self.__timesetting.get()) >= 0 and int(self.__timesetting.get()) <= 3600:
                                self.__playCallback()
                        else:
                            window = Toplevel(self.__root)
                            window.title("Error")
                            window.geometry("300x150")
                            window.configure(bg=self.BACKGROUND)
                            window_label = Label(window, text="Incorrect Time Limit Entered \n Please Change!", bg=self.BACKGROUND, fg=self.FOREGROUND)
                            window_label.pack(pady=10)

                            frame = Frame(window, bg=self.BACKGROUND)
                            frame.pack(pady=5)
                            exit = Button(window, text="Close", command=window.destroy)
                            exit.pack(side=BOTTOM)
                    else:
                            window = Toplevel(self.__root)
                            window.title("Error")
                            window.geometry("300x150")
                            window.configure(bg=self.BACKGROUND)
                            window_label = Label(window, text="Incorrect Board Size Entered \n Please Change!", bg=self.BACKGROUND, fg=self.FOREGROUND)
                            window_label.pack(pady=10)

                            frame = Frame(window, bg=self.BACKGROUND)
                            frame.pack(pady=5)
                            exit = Button(window, text="Close", command=window.destroy)
                            exit.pack(side=BOTTOM)
                except:
                    window = Toplevel(self.__root)
                    window.title("Error")
                    window.geometry("200x150")
                    window.configure(bg=self.BACKGROUND)
                    window_label = Label(window, text="Incorrect Settings! \n Please try again!", bg=self.BACKGROUND, fg=self.FOREGROUND)
                    window_label.pack(pady=10)
                    frame = Frame(window, bg=self.BACKGROUND)
                    frame.pack(pady=5)
                    exit = Button(window, text="Close", command=window.destroy)
                    exit.pack(side=BOTTOM)
        else:
            window = Toplevel(self.__root)
            window.title("Error")
            window.geometry("300x150")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Error: Game is already in progress!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)

            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

        if self.__onevsone == True:
            self.__setAIDifficulty()

    # User selects game settings such as gamemode or difficulty
    def __gametypeCallback(self):
        yesorno = ["Yes", "No"]
        difficulties = ["Custom", "Easy", "Medium", "Hard"]
        gamemodes = ["None", "Time Battle", "Letter Challenge", "One-Time Use", "Length Challenge"]
        self.__difficulty = StringVar()
        self.__difficulty.set("Medium")
        self.__gametype = StringVar()
        self.__gametype.set("Singleplayer")
        self.__gamemode = StringVar()
        self.__gamemode.set("None")
        self.__showdefinitions = StringVar()
        self.__showdefinitions.set("No")
        window = Toplevel(self.__root)
        window.title("Game Type Configuration")
        window.geometry("640x480")
        window.configure(bg=self.BACKGROUND)
        window_label = Label(window, text="Game Type Configuration", bg=self.BACKGROUND, fg=self.FOREGROUND)
        window_label.pack(pady=10)

        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack(pady=5)

        difficultylabel = Label(window, text="Difficulty", bg=self.BACKGROUND, fg=self.FOREGROUND)
        difficultylabel.pack(pady=5)
        difficulty = OptionMenu(window, self.__difficulty, *difficulties)
        difficulty.pack()

        gamemodelabel = Label(window, text="Gamemode", bg=self.BACKGROUND, fg=self.FOREGROUND)
        gamemodelabel.pack(pady=5)
        gamemode = OptionMenu(window, self.__gamemode, *gamemodes)
        gamemode.pack()

        definitions = Label(window, text="Show definitions window?",bg=self.BACKGROUND, fg=self.FOREGROUND)
        definitions.pack(pady=5)
        showdefinitions = OptionMenu(window, self.__showdefinitions, *yesorno)
        showdefinitions.pack()        

        exit = Button(window, text="Start Game", command=lambda:[self.__gametypeCheck(), window.destroy()])
        exit.pack(pady=10,side=BOTTOM)

    # Sets settings like the board size, minimum word length and time limit depending on the gamemode or difficulty
    def __gametypeCheck(self):
        self.__gamemodeapproved = False
        self.__timebattle = False
        self.__lengthchallenge = False
        self.__letterchallenge = False
        self.__onetimeuse = False
        self.__availableletters = []
        if self.__difficulty.get() == "Easy":
            self.__game._BoardSize = 10
            self.__game._MinLength = 2
            self.__game.time = 180
            self.__settingscheck = True
        elif self.__difficulty.get() == "Medium":
            self.__game._BoardSize = 7
            self.__game._MinLength = 3
            self.__game.time = 120
            self.__settingscheck = True
        elif self.__difficulty.get() == "Hard":
            self.__game._BoardSize = 5
            self.__game._MinLength = 3
            self.__game.time = 60
            self.__settingscheck = True
        else:
            self.__gameSettingsCallback()

        if self.__gamemode.get() == "Time Battle":
            self.__timebattle = True
            self.__gamemodeapproved = True
            self.__game.time = 10
            if self.__difficulty.get() == "Easy":
                self.__timeadd = 10
            if self.__difficulty.get() == "Medium":
                self.__timeadd = 7
            if self.__difficulty.get() == "Hard":
                self.__timeadd = 4
            if self.__difficulty.get() != "Custom":
                self.__playCallback()                
        elif self.__gamemode.get() == "Letter Challenge":
            self.__letterchallenge = True
            self.__currletter = Game.LETTERCHALLENGELETTERS[random.randint(0,len(Game.LETTERCHALLENGELETTERS)-1)]
            self.__game.time = 20
            if self.__difficulty.get() != "Custom":
                self.__playCallback()
        elif self.__gamemode.get() == "One-Time Use":
            self.__onetimeuse = True
            self.__availableletters = Game.LETTERS
            self.__game.time = 20
            if self.__difficulty.get() != "Custom":
                self.__playCallback()
        elif self.__gamemode.get() == "Length Challenge":
            self.__lengthchallenge = True
            if self.__difficulty.get() == "Hard":
                self.__game._BoardSize = 8
                self.__game._MinLength = 3
            if self.__difficulty.get() == "Medium":
                self.__game._BoardSize = 9
                self.__game._MinLength = 2
            if self.__difficulty.get() == "Easy":
                self.__game._BoardSize = 10
                self.__game._MinLength = 2
            self.__lengthchall = random.randint(self.__game._MinLength,5)
            if self.__lengthchall == self.__game._MinLength:
                self.__time_left = 10
                self.__game.time = 10
            if self.__lengthchall == 3:
                self.__time_left = 25
                self.__game.time = 25
            if self.__lengthchall == 4:
                self.__time_left = 40
                self.__game.time = 40
            if self.__lengthchall == 5:
                self.__time_left = 60
                self.__game.time = 60
            if self.__difficulty.get() != "Custom":
                self.__playCallback()
        elif self.__gamemode.get() == "None" and self.__difficulty.get() != "Custom":
            self.__gamemodeapproved = True
            self.__playCallback() 

    # Methods called after pressing the 'Apply' button when creating game settings
    # Performs the validation
    ########################
    # Excellent coding style demonstrated through:
    # Defensive programming
    # Exception Handling
    ########################
    def __setTimeAdded(self):
        try:
            timeadded = self.__timeadded.get()
            timeadded = int(timeadded)
            if timeadded <= 30 and timeadded >= 0:
                timeadded = self.__timeadded.get()
                timeadded = int(timeadded)
                self.__timeadd = timeadded
            else:
                self.__timeadded.insert(0, "Error: Needs to be between 0 and 30!")
        except:
            window = Toplevel(self.__root)
            window.title("Error")
            window.geometry("200x50")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Invalid Entry!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

    def __setBoardSize(self):
        try:
            if int(self.__boardsizesetting.get()) >= 4 and int(self.__boardsizesetting.get()) <= 10:
                self.__game._BoardSize = int(self.__boardsizesetting.get())
            else:
                self.__boardsizesetting.insert(0, "Error: Size needs to be within 4 to 10")
        except:
            window = Toplevel(self.__root)
            window.title("Error")
            window.geometry("200x50")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Invalid Entry!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

    def __setMinLength(self):
        try:
            if int(self.__minlengthsetting.get()) >= 0:
                self.__game._MinLength = int(self.__minlengthsetting.get())
        except:
                window = Toplevel(self.__root)
                window.title("Error")
                window.geometry("200x50")
                window.configure(bg=self.BACKGROUND)
                window_label = Label(window, text="Invalid Entry!", bg=self.BACKGROUND, fg=self.FOREGROUND)
                window_label.pack(pady=10)
                frame = Frame(window, bg=self.BACKGROUND)
                frame.pack(pady=5)
                exit = Button(window, text="Close", command=window.destroy)
                exit.pack(side=BOTTOM)

    def __setGameTime(self):
        try:
            if int(self.__timesetting.get()) != 0:
                self.__game.time = int(self.__timesetting.get())
            else:
                self.__game.time = 9999999
        except:
            window = Toplevel(self.__root)
            window.title("Error")
            window.geometry("200x50")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Invalid Entry!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            exit = Button(window, text="Close", command=window.destroy)
            exit.pack(side=BOTTOM)

    # Resets all attributes, variables and creates new instances so that another game can be played withouth having to restart the program
    # Another occurance of dynamic object generation (group A)
    def __resetGame(self):
        self.__wordcount = StringVar()
        self.__timeleft = StringVar()
        self.__timelefttext = StringVar()
        self.__aidifficulty = StringVar()
        self.__timeadd = 0
        self.__pausetext = StringVar()
        self.__pausetext.set("Pause")
        self.__showdefinitions = StringVar()
        self.__gametype = StringVar()
        self.__difficulty = StringVar()
        self.__gamemode = StringVar()
        self.__changeboard = StringVar()
        self.__gamemodeinfo = StringVar()
        self.__loadinggame = False
        self.__stoptimer = False
        self.__multiplayer = False
        self.__scoreToBeat = 0
        self.__scorebeaten = False
        self.__onevsone = False
        self.__aiturn = False
        self.__availableletters = Game.LETTERS
        self.__aifound = []
        self.__aiturncounter = 0
        self.__inprogress = False
        self.__online = False
        self.__gameduration = 0
        self.__AI = AI()
        self.__game = Game()
        self.__game._gui = True
        self.__quitting = False
        self.__loadproceed = False
        self.__gamemodeapproved = False
        self.__cancelOnline = False

####################
##### GAMEPLAY #####
####################

    def run(self):
        self.__root.mainloop()

    # Uses same threading method as game class to create a timer
    # Uses same values as game class so that the times are synced up
    # However uses StringVars so that the time can be displayed on the game window
    # Also syncs other areas of the program such as the AI guess times
    def __calculateTimeLeft(self):
        try:
            if self.__game.time <= 3600:
                self.__time_left = self.__game.time
                while self.__time_left != 1:
                    if self.__game.pause == False:
                        self.__time_left -= 1
                        if self.__aiturn == False:
                            self.__timeleft.set(str(self.__game.time_left))
                        else:
                            if (self.__time_left in self.__aiturntimes):
                                self.__doAITurn()
                            if self.__time_left == 0 and self.__aiturn == True:
                                self.__consoleMsg("The AI was unable to find a word!")
                            self.__timeleft.set(str(self.__game.time_left))
                    self.__gameduration += 1
                    time.sleep(1)
                    if self.__stoptimer == True:
                        self.__time_left = 1
                        break
                if self.__online:
                    self.__consoleMsg("Waiting for other player to finish...")
                if not self.__quitting:
                    self.__finish()
            else:
                self.__timeleft.set("Unlimited")
        except AttributeError:
            self.__time_left = 1

    # Start Button which begins the timer and starts the game
    def __startBtn(self):
        if self.__gamestarted == False:
            if self.__loadinggame == False:
                self.__changecounter = 0
                self.__totalguesses = 0
                self.__correctcounter = 0
            self.__game._doStart()
            timecalc = threading.Thread(target = self.__calculateTimeLeft)
            timecalc.start()
            self.__gamestarted = True
            self.__console.insert(END, "Game has been started!\n")
            self.__selected.config(state="normal")
            self.__selected.delete(1.0, END)
            self.__selected.config(state="disabled")
            if self.__loadinggame == True:
                self.__selected.insert(INSERT, str(self.__game.wordstack))
                self.__wordcount.set(str(self.__correctcounter))
                self.__guesses.delete(1.0, END)
                self.__guesses.insert(INSERT, self.__game.words)
            if self.__multiplayer == True:
                if self.__multiplayergamemode.get() == "AI: Beat Their Score":
                    if not self.__loadproceed:
                        self.__setScoreToBeat(self.__AI._beatTheirScore(self.__game._validwords, self.__time_left))
                        self.__consoleMsg("\nScore to beat: " + str(self.__scoreToBeat))
                    else:
                        currscore = self.__game._getFinalScore(0,0)*3
                        self.__scoreToBeat = self.__scoreToBeat - currscore
                        self.__consoleMsg("\nScore to beat: " + str(self.__scoreToBeat))

    # What happens when a button is clicked, the letter is fetched and is passed as a parameter to the click method in the game class
    def __btnClickEvent(self, row, col):
        if self.__aiturn != True:
            self.__changeBoardColour(self.BACKGROUND)
            if self.__gamestarted == True and self.__game.pause == False:
                if self.__game.timeup == False:
                    self.__game._doLetterClick(row+1,col+1)
                    if self.__game.usedletter == True:
                        self.__consoleMsg("You have already used this letter!")
                    elif self.__game.nottouching:
                        self.__consoleMsg("This letter is not touching the previous letter!")
                    else:
                        self.__clicked.append((row,col))
                        self.__selected.config(state="normal")
                        self.__selected.insert(INSERT, self.__game.at(row+1,col+1))
                        self.__selected.config(state="disabled")
                else:
                    self.__consoleMsg("Time has run out!")
                    self.__clearSelection()
            else:
                self.__consoleMsg("Please start the game/toggle pause before selecting a letter!")
        else:
            self.__consoleMsg("It is currently the AI's turn!")

    # Clears all items from the stack
    def __clearSelection(self):
        if self.__gamestarted == True and self.__game.pause == False and self.__aiturn == False:
            if self.__game.timeup == False:
                    self.__game.wordstack = []
                    self.__game.usedlocations = []
                    self.__clicked = []
                    self.__selected.config(state="normal")
                    self.__selected.delete(1.0, END)
                    self.__selected.config(state="disabled")
            else:
                self.__consoleMsg("Time has run out!")
        else:
            if self.__gamestarted and self.__inprogress:
                if self.__time_left > 1:
                    self.__consoleMsg("Please start the game/toggle pause before trying to clear anything!")

    ############################
    # Group A Skill
    # Stack Operation
    # undo pops an item off the top of the stack (LIFO)
    # If the most recent action was submitting a word, the word is unsumbmitted
    # Score doesn't need to be subtracted as it is calculated based off submitted words at the end
    ############################
    def _undo(self):
        if self.__inprogress == True and self.__game.pause == False:
            if len(self.__game.wordstack) >= 1:
                self.__lettermarker = self.__game.wordstack[(len(self.__game.wordstack)-1)]
                self.__game.wordstack.pop()
                self.__game.usedlocations.pop()
                self.__clicked.pop()
                self.__selected.config(state="normal")
                self.__selected.delete(1.0, END)
                self.__selected.insert(INSERT, ''.join([str(i) for i in self.__game.wordstack]))
                self.__selected.config(state="disabled")
                self.__consoleMsg("Deselected letter " + str(self.__lettermarker))
            else:
                if len(self.__game.words) >= 1:
                    self.__wordmarker = self.__game.words[(len(self.__game.words)-1)]
                    self.__game.words.pop()
                    self.__guesses.delete(1.0, END)
                    self.__guesses.insert(INSERT, self.__game.words)
                    self.__consoleMsg("Deselected word " + str(self.__wordmarker))
                else:
                    self.__consoleMsg("Nothing to undo!")
        else:
            self.__consoleMsg("Please start the game/toggle pause before trying to undo!")

    # Runs through the process of submitting a word
    # Depending on different gamemodes, there are various factors that determine whether a word is valid or not
    # Letter challenge requires the word to contain the shown letter
    # Length challenge requires the word to be a minimum length
    # One-time use needs to remove letters from the grid after a word is submitted
    # AI: Beat their score needs to calculate and display the score remaining
    # AI: 1v1 needs to make it the AI's turn and ensure the AI can't select the same word
    # These are moderated with a "gamemode approved" variable, which is set to true is the word meets the gamemodes requirements
    # The colour of the selected letter locations changes to the correct/incorrect colour
    # Time may be added or the grid may be changed if the gamemode/settings include that
    def __submitWord(self):
        if self.__game.pause == False and self.__aiturn == False:
            self.__gamemodeapproved = False
            if self.__gamemode.get() == "Custom" or self.__gamemode.get() == "None" or self.__onevsone == True or self.__gamemode.get() == "AI: Beat Their Score":
                self.__gamemodeapproved = True
            if self.__gamestarted == True:
                if self.__game.timeup == False:
                    if len(self.__game.wordstack) >= self.__game._MinLength:
                            self.__consoleMsg("Submitting word " + ''.join([str(i) for i in self.__game.wordstack]))
                            word = (''.join([str(i) for i in self.__game.wordstack])).upper()
                            self.__game._doSubmit()
                            self.__totalguesses += 1
                            if self.__game.correct == True:
                                if self.__lengthchallenge == True:
                                    if len(self.__game.currword) >= self.__lengthchall:
                                        self.__gamemodeapproved = True
                                        self.__lengthchall = random.randint(self.__game._MinLength,5)
                                        self.__gamemodeinfo.set("Length: \n" + str(self.__lengthchall))
                                        if self.__lengthchall == self.__game._MinLength:
                                            self.__time_left = 10
                                            self.__game.time_left = 10
                                        if self.__lengthchall == 3:
                                            self.__time_left = 25
                                            self.__game.time_left = 25
                                        if self.__lengthchall == 4:
                                            self.__time_left = 40
                                            self.__game.time_left = 40
                                        if self.__lengthchall == 5:
                                            self.__time_left = 60
                                            self.__game.time_left = 60
                                if self.__timebattle == True:
                                    self.__addTime(self.__timeadd)
                                    self.__gamemodeapproved = True
                                if self.__letterchallenge == True:
                                    if self.__currletter in self.__game.currword:
                                        self.__gamemodeapproved = True
                                        self.__addTime(20)
                                        self.__currletter = Game.LETTERCHALLENGELETTERS[random.randint(0,len(Game.LETTERCHALLENGELETTERS))]
                                        self.__gamemodeinfo.set("Letter: \n" + str(self.__currletter))
                                if self.__onetimeuse == True:
                                    self.__gamemodeapproved = True
                                    self.__currletter = self.__game.currword[0]
                                    self.__game.time = 20
                                    self.__game.time_left = 20
                                    self.__time_left = 20
                                    self.__gamemodeinfo.set("Removing: \n" + str(self.__currletter))
                                if self.__difficulty.get() == "Custom":
                                    self.__addTime(int(self.__timeadd))
                                    self.__changecounter += 1
                                    if int(self.__changeboard.get()) > 0:
                                        if self.__changeboard.get() == 1:
                                            self.__changeLettersInBoard()
                                        elif self.__changecounter == int(self.__changeboard.get()):
                                            self.__changeLettersInBoard()
                                            self.__changecounter = 0
                                if self.__gamemodeapproved == True:
                                    if self.__onevsone == True:
                                        if word not in self.__aifound:   
                                            self.__consoleMsg("Correct Word!")
                                            if self.__showdefinitions.get() == "Yes":
                                                self.__sendDefinition(self.__game.meaning)
                                                self.__sendDefinition("\n")
                                            self.__correctcounter += 1
                                            self.__wordcount.set(str(self.__correctcounter))
                                            self.__guesses.delete(1.0, END)
                                            self.__guesses.insert(INSERT, self.__game.words)
                                            for row,col in self.__clicked:
                                                self.__changeBtnColour(row,col,self.__correctcolour.get())
                                            self.__clearSelection()
                                            self.__time_left = 15
                                            self.__game.time_left = 15
                                            self.__aiturn = True
                                            self.__changeBoardColour("#737373")
                                            self.__selected.config(state="normal")
                                            self.__selected.delete(1.0, END)
                                            self.__selected.insert(INSERT, "AI Turn...")
                                            self.__selected.config(state="disabled")
                                        else:
                                            self.__consoleMsg("The AI has already found this word!")
                                            for row,col in self.__clicked:
                                                self.__changeBtnColour(row,col,self.__incorrectcolour.get())
                                            self.__clearSelection()
                                    else:
                                        self.__consoleMsg("Correct Word!")
                                        if self.__showdefinitions.get() == "Yes":
                                            self.__sendDefinition(self.__game.meaning)
                                            self.__sendDefinition("\n")
                                        self.__correctcounter += 1
                                        self.__wordcount.set(str(self.__correctcounter))
                                        self.__guesses.delete(1.0, END)
                                        self.__guesses.insert(INSERT, self.__game.words)
                                    if self.__multiplayer == True:
                                        if self.__multiplayergamemode.get() == "AI: Beat Their Score":
                                            currscore = self.__game._getFinalScore(0,0)*3
                                            self.__consoleMsg("Current Score: " + str(currscore))
                                            scoreleft = self.__scoreToBeat - currscore
                                            self.__consoleMsg("\nScore left: " + str(scoreleft))
                                            for row,col in self.__clicked:
                                                self.__changeBtnColour(row,col,self.__correctcolour.get())
                                            self.__clearSelection()
                                            if scoreleft <= 0:
                                                self.__scorebeaten = True
                                                self.__finish()
                                        elif self.__online == True:
                                            for row,col in self.__clicked:
                                                self.__changeBtnColour(row,col,self.__correctcolour.get())
                                            self.__clearSelection()
                                    else:
                                        for row,col in self.__clicked:
                                            self.__changeBtnColour(row,col,self.__correctcolour.get())
                                        self.__clearSelection()
                                else:
                                    self.__game.words.pop()
                                    self.__consoleMsg("Incorrect Word!")
                                    for row,col in self.__clicked:
                                        self.__changeBtnColour(row,col,self.__incorrectcolour.get())
                                    self.__clearSelection()               
                            else:
                                self.__consoleMsg("Incorrect Word!")
                                if self.__game.tooshort == True:
                                    self.__consoleMsg("The word does not meet the minimum word length!")
                                for row,col in self.__clicked:
                                    self.__changeBtnColour(row,col,self.__incorrectcolour.get())
                                self.__clearSelection()
                            if self.__letterchallenge == True and self.__gamemodeapproved == True:
                                self.__changeLettersInBoard()
                            if self.__onetimeuse == True and self.__gamemodeapproved == True:
                                try:
                                    self.__removeLetterFromBoard(self.__currletter)
                                except:
                                    pass
                    else:
                        self.__consoleMsg("Your word is too short!")
                        for row,col in self.__clicked:
                            self.__changeBtnColour(row,col,self.__incorrectcolour.get())
                        self.__clearSelection()
                else:
                    self.__consoleMsg("Time has run out!")
                    self.__clearSelection()
            else:
                self.__consoleMsg("Please start the game before trying to submit anything!")
        else:
            self.__consoleMsg("Please click pause to resume!")

    def __changeBtnColour(self,row,col,colour):
        self.__button[row][col].config(bg=colour)
    
    def __changeBoardColour(self, colour):
        for row in range(len(self.__button)):
            for col in range(len(self.__button)):
                self.__button[row][col].config(bg=colour)

    def __addTime(self, time):
        if self.__timeleft.get() != "Unlimited":
            self.__game.time_left += time
            self.__time_left += time
        
    def __changeLettersInBoard(self):
        for _ in range(self.__game._BoardSize):
            for x in range(self.__game._BoardSize):
                    self.__game._Board[_][x] = Game.LETTERS[random.randint(0,25)]
        for row in range(self.__game._BoardSize):
            for col in range(self.__game._BoardSize):
                b = StringVar()
                b.set(self.__game.at(row+1,col+1))
                self.__buttons[row][col].set(b.get())

    def __removeLetterFromBoard(self, letter):
        self.__availableletters.remove(letter)
        for _ in range(self.__game._BoardSize):
            for x in range(self.__game._BoardSize):
                    self.__game._Board[_][x] = self.__availableletters[random.randint(0,len(self.__availableletters)-1)]
        for row in range(self.__game._BoardSize):
            for col in range(self.__game._BoardSize):
                b = StringVar()
                b.set(self.__game.at(row+1,col+1))
                self.__buttons[row][col].set(b.get())

    # Creates the definitions window
    # Contains a scrolling feature and displays the messages given by the send definition method
    def __definitionsWindow(self):
        window = Toplevel(self.__gamewindow)
        window.title("Definitions")
        window.geometry("650x400")
        window.configure(bg=self.BACKGROUND)

        frame = Frame(window, bg=self.BACKGROUND)
        frame.grid()

        definitionsconsole = Text(frame)
        self.__definitionsconsole = definitionsconsole
        definitionsconsole.configure(background=self.BACKGROUND)
        definitionsconsole.grid(sticky="N")
        scroll = Scrollbar(frame)     
        scroll.config(command=definitionsconsole.yview)
        definitionsconsole.config(yscrollcommand=scroll.set)

    # The play method for the GUI game
    # Creates the main game window
    # Using a for loop, buttons are created in an even grid of BoardSize length and width
    # Each button is overlayed with a StringVar of the letter at that location in the grid
    # Upon clicking that button, the button click event method is called and the row and column are passed as parameters
    # There are multiple buttons underneath the grid such as submit and play which are bound with the respective functions
    # There is a console on the right side of the game window which displays messages throughout the game
    # An extra widget displaying information about the game is sometimes underneath the timer depending on the gamemode
    def __playCallback(self):
        if self.__inprogress:
            return
        self.__inprogress = True
        self.__gamewindow = Toplevel(self.__root)
        self.__gamewindow.title("Boggle")
        frame = Frame(self.__gamewindow)
        self.__gamewindow.geometry("1366x768")
        self.__gamewindow.protocol("WM_DELETE_WINDOW", self._quitGame)
        if not self.__online:
            self.__game._createBoard()
        self.__selected = Text(self.__gamewindow,height=2,width=5, font=(self.FONT, 35))

        self.__buttons = [[None]*self.__game._BoardSize for _ in range(self.__game._BoardSize)]
        self.__button = [[None]*self.__game._BoardSize for _ in range(self.__game._BoardSize)]

        for row,col in product(range(self.__game._BoardSize), range(self.__game._BoardSize)):
            buttontext = StringVar()
            buttontext.set(self.__game.at(row+1,col+1))
            buttoncmd = lambda r=row, c=col: self.__btnClickEvent(r,c)
            button = Button(self.__gamewindow, textvariable=buttontext, font=(self.FONT, 20), bg=self.BACKGROUND, activebackground="#94bdff", command=buttoncmd, height=5, width=5)
            self.__button[row][col] = button
            button.grid(row=row,column=col,sticky="nesw")
            self.__buttons[row][col]=buttontext
        
        self.__button1 = Button(self.__gamewindow, text="Start", font=(self.FONT, 20), command=self.__startBtn, height=2, width=5)
        self.__button1.grid(row=self.__game._BoardSize+1,column=0,sticky="nsew")
        self.__button2 = Button(self.__gamewindow, text="Finish", font=(self.FONT, 20), command=self.__finish,height=5, width=5)
        self.__button2.grid(row=self.__game._BoardSize+1,column=1,sticky="nsew")
        self.__button3 = Button(self.__gamewindow, text="Exit", font=(self.FONT, 20), command = self.__confirmExit, height=2, width=5)
        self.__button3.grid(row=self.__game._BoardSize+1,column=2,sticky="nsew")
        self.__button4 = Button(self.__gamewindow, text="Submit", font=(self.FONT, 20), command= self.__submitWord, height=2, width=5)
        self.__button4.grid(row=self.__game._BoardSize+1,column=3,sticky="nsew")
        if self.__game._BoardSize == 5:
            self.__button5 = Button(self.__gamewindow, text="Toggle" + "\n" + "Controls", font=(self.FONT, 20), command=self.__toggleExtraButtons,height=5, width=5)
            self.__button5.grid(row=self.__game._BoardSize+1,column=4,sticky="nsew")
            self.__selected.grid(row=self.__game._BoardSize+1, column=5, columnspan=self.__game._BoardSize+1, sticky="nsew")
            self.__selected.config(state="disabled")
        else:
            self.__button5 = Button(self.__gamewindow, text="Clear", font=(self.FONT, 20), command = self.__clearSelection, height=2, width=5)
            self.__button5.grid(row=self.__game._BoardSize+1,column=4,sticky="nsew")
        if self.__game._BoardSize == 6:
            self.__button6 = Button(self.__gamewindow, text="Toggle" + "\n" + "Controls", font=(self.FONT, 20), command=self.__toggleExtraButtons,height=5, width=5)
            self.__button6.grid(row=self.__game._BoardSize+1,column=5,sticky="nsew")
            self.__selected.grid(row=self.__game._BoardSize+1, column=6, columnspan=self.__game._BoardSize+1, sticky="nsew")
            self.__selected.config(state="disabled")
        if self.__game._BoardSize == 7:
            self.__button6 = Button(self.__gamewindow, text="Undo", font=(self.FONT, 20), command=self._undo,height=5, width=5)
            self.__button6.grid(row=self.__game._BoardSize+1,column=5,sticky="nsew")
            self.__button7 = Button(self.__gamewindow, text="Toggle" + "\n" + "Controls", font=(self.FONT, 20), command=self.__toggleExtraButtons,height=5, width=5)
            self.__button7.grid(row=self.__game._BoardSize+1,column=6,sticky="nsew")
            self.__selected.grid(row=self.__game._BoardSize+1, column=7, columnspan=self.__game._BoardSize+1, sticky="nsew")
            self.__selected.config(state="disabled")
        if self.__game._BoardSize >= 8:
            self.__button6 = Button(self.__gamewindow, text="Undo", font=(self.FONT, 20), command=self._undo,height=5, width=5)
            self.__button6.grid(row=self.__game._BoardSize+1,column=5,sticky="nsew")
            self.__button7 = Button(self.__gamewindow, textvariable=self.__pausetext, font=(self.FONT, 20), command=self.__togglePause,height=5, width=5)
            self.__button7.grid(row=self.__game._BoardSize+1,column=6,sticky="nsew")
            self.__button8 = Button(self.__gamewindow, text="Save", font=(self.FONT, 20), command=self.__setFileName, height=5, width=5)
            self.__button8.grid(row=self.__game._BoardSize+1, column=7,sticky="nsew")
            self.__selected.grid(row=self.__game._BoardSize+1, column=8, columnspan=self.__game._BoardSize+1, sticky="nsew")
            self.__selected.config(state="disabled")            

        if self.__showdefinitions.get() == "Yes":
            self.__definitionsWindow()

        # Grid configuration
        num = self.__game._BoardSize
        for x in range(num):
            Grid.rowconfigure(self.__gamewindow, x, weight=1)
            Grid.columnconfigure(self.__gamewindow, x, weight=1)
        frame.grid(row=0,column=0,sticky="nswe")

        # Console and Gamemode Box
        if self.__gamemode.get() == "None" or self.__gamemode.get() == "Time Battle":
            if self.__game._BoardSize <= 6:
                width = self.__game._BoardSize*7
            else:
                width = self.__game._BoardSize*5
            console = Text(self.__gamewindow,height=7*self.__game._BoardSize,width=width, font=(self.FONT, 10))
            self.__console = console
            console.configure(background=self.BACKGROUND)
            console.grid(row=1, rowspan = self.__game._BoardSize,column=self.__game._BoardSize+1,sticky=E)
            scroll = Scrollbar(frame)
            scroll.grid(sticky=E)        
            scroll.config(command=console.yview)
            console.config(yscrollcommand=scroll.set)
        else:
            if self.__game._BoardSize <= 6:
                width = self.__game._BoardSize*7
            else:
                width = self.__game._BoardSize*5
            console = Text(self.__gamewindow,height=5*self.__game._BoardSize,width=width, font=(self.FONT, 10))
            self.__console = console
            console.configure(background=self.BACKGROUND)
            console.grid(row=2, rowspan = self.__game._BoardSize-1,column=self.__game._BoardSize+1,sticky=W)
            scroll = Scrollbar(frame)
            scroll.grid(sticky=E)        
            scroll.config(command=console.yview)
            console.config(yscrollcommand=scroll.set)
            self.__gamemodebox = Label(self.__gamewindow, textvariable=self.__gamemodeinfo, font=(self.FONT, 17))
            self.__gamemodebox.grid(row=1,column=self.__game._BoardSize+1)
            if self.__lengthchallenge == True:
                self.__gamemodeinfo.set("Length: " + str(self.__lengthchall))
            elif self.__letterchallenge == True:
                self.__gamemodeinfo.set("Letter: \n" + str(self.__currletter))
        
        self.__timelefttext = Label(self.__gamewindow, textvariable=self.__timeleft, font=(self.FONT, 20))
        self.__timelefttext.grid(row=0,column=self.__game._BoardSize+1)

        guesses = Text(self.__gamewindow,height=2,width=self.__game._BoardSize*40)
        self.__guesses = guesses
        guesses.configure(background=self.BACKGROUND)
        guesses.grid(row=self.__game._BoardSize+2,column=0,columnspan=self.__game._BoardSize)

    # In the case that the board size is too small to fit all the buttons, the right most button becomes a toggle button
    # If clicked, some buttons are replaced to insert the other buttons that couldn't fit on the game window
    # The toggle button remains regardless, so the user can toggle between buttons as required
    def __toggleExtraButtons(self):
        if self.__game._BoardSize == 5:
            if self.__buttontoggle == False:
                self.__button1.destroy()
                self.__button2.destroy()
                self.__button3.destroy()
                self.__button4.destroy()
                self.__button1 = Button(self.__gamewindow, text="Clear", font=(self.FONT, 20), command=self.__clearSelection, height=2, width=5)
                self.__button1.grid(row=self.__game._BoardSize+1,column=0,sticky="nsew")
                self.__button2 = Button(self.__gamewindow, text="Undo", font=(self.FONT, 20), command=self._undo,height=5, width=5)
                self.__button2.grid(row=self.__game._BoardSize+1,column=1,sticky="nsew")
                self.__button3 = Button(self.__gamewindow, textvariable=self.__pausetext, font=(self.FONT, 20), command = self.__togglePause, height=2, width=5)
                self.__button3.grid(row=self.__game._BoardSize+1,column=2,sticky="nsew")
                self.__button4 = Button(self.__gamewindow, text="Save", font=(self.FONT, 20), command= self.__setFileName, height=2, width=5)
                self.__button4.grid(row=self.__game._BoardSize+1,column=3,sticky="nsew")
                self.__buttontoggle = True
            else:
                self.__button1.destroy()
                self.__button2.destroy()
                self.__button3.destroy()
                self.__button4.destroy()
                self.__button1 = Button(self.__gamewindow, text="Start", font=(self.FONT, 20), command=self.__startBtn, height=2, width=5)
                self.__button1.grid(row=self.__game._BoardSize+1,column=0,sticky="nsew")
                self.__button2 = Button(self.__gamewindow, text="Finish", font=(self.FONT, 20), command=self.__finish,height=5, width=5)
                self.__button2.grid(row=self.__game._BoardSize+1,column=1,sticky="nsew")
                self.__button3 = Button(self.__gamewindow, text="Exit", font=(self.FONT, 20), command = self.__confirmExit, height=2, width=5)
                self.__button3.grid(row=self.__game._BoardSize+1,column=2,sticky="nsew")
                self.__button4 = Button(self.__gamewindow, text="Submit", font=(self.FONT, 20), command= self.__submitWord, height=2, width=5)
                self.__button4.grid(row=self.__game._BoardSize+1,column=3,sticky="nsew")
                self.__buttontoggle = False

        if self.__game._BoardSize == 6:
            if self.__buttontoggle == False:
                self.__button3.destroy()
                self.__button4.destroy()
                self.__button5.destroy()
                self.__button3 = Button(self.__gamewindow, text="Undo", font=(self.FONT, 20), command=self._undo, height=2, width=5)
                self.__button3.grid(row=self.__game._BoardSize+1,column=2,sticky="nsew")
                self.__button4 = Button(self.__gamewindow, textvariable=self.__pausetext, font=(self.FONT, 20), command=self.__togglePause,height=5, width=5)
                self.__button4.grid(row=self.__game._BoardSize+1,column=3,sticky="nsew")
                self.__button5 = Button(self.__gamewindow, text="Save", font=(self.FONT, 20), command = self.__setFileName, height=2, width=5)
                self.__button5.grid(row=self.__game._BoardSize+1,column=4,sticky="nsew")
                self.__buttontoggle = True
            else:
                self.__button3.destroy()
                self.__button4.destroy()
                self.__button5.destroy()
                self.__button3 = Button(self.__gamewindow, text="Exit", font=(self.FONT, 20), command=self.__confirmExit,height=5, width=5)
                self.__button3.grid(row=self.__game._BoardSize+1,column=2,sticky="nsew")
                self.__button4 = Button(self.__gamewindow, text="Submit", font=(self.FONT, 20), command = self.__submitWord, height=2, width=5)
                self.__button4.grid(row=self.__game._BoardSize+1,column=3,sticky="nsew")
                self.__button5 = Button(self.__gamewindow, text="Clear", font=(self.FONT, 20), command= self.__clearSelection, height=2, width=5)
                self.__button5.grid(row=self.__game._BoardSize+1,column=4,sticky="nsew")
                self.__buttontoggle = False

        if self.__game._BoardSize == 7:
            if self.__buttontoggle == False:
                self.__button5.destroy()
                self.__button6.destroy()
                self.__button5 = Button(self.__gamewindow, textvariable=self.__pausetext, font=(self.FONT, 20), command=self.__togglePause,height=5, width=5)
                self.__button5.grid(row=self.__game._BoardSize+1, column=4, sticky="nsew")
                self.__button6 = Button(self.__gamewindow, text="Save", font=(self.FONT, 20), command=self.__setFileName,height=5, width=5)
                self.__button6.grid(row=self.__game._BoardSize+1, column=5, sticky="nsew")
                self.__buttontoggle = True
            else:
                self.__button5.destroy()
                self.__button6.destroy()
                self.__button5 = Button(self.__gamewindow, text="Clear", font=(self.FONT, 20), command= self.__clearSelection, height=2, width=5)
                self.__button5.grid(row=self.__game._BoardSize+1,column=4,sticky="nsew")
                self.__button6 = Button(self.__gamewindow, text="Undo", font=(self.FONT, 20), command=self._undo,height=5, width=5)
                self.__button6.grid(row=self.__game._BoardSize+1,column=5,sticky="nsew")
                self.__buttontoggle = False

    def __consoleMsg(self, msg):
        self.__console.insert(END, msg + "\n")

    def __togglePause(self):
        if self.__inprogress == True:
            if self.__game.pause == False:
                self.__game.pause = True
                self.__pausetext.set("Resume")
            else:
                self.__game.pause = False
                self.__pausetext.set("Pause")
        else:
            self.__consoleMsg("Please start the game before pausing!")

    # Makes the user confirm quitting a game to avoid accidental game quitting
    def __confirmExit(self):
        if self.__inprogress:
            window = Toplevel(self.__root)
            window.title("Confirm Exit")
            window.geometry("275x50")
            window.configure(bg=self.BACKGROUND)
            confirm_label = Label(window, text="Are you sure you want to exit the game?", bg=self.BACKGROUND, fg=self.FOREGROUND)
            confirm_label.pack()
            Button(window, text="Yes",font=(self.FONT, 11),command=lambda: [self._quitGame(), self.__resetGame(), window.destroy()], background=self.BACKGROUND).pack(pady=5)

    # Retrives the definition of the submitted word
    # Manipulates the string to remove unnecessary characters and show a simple, clear definition of the word
    # Sends the definition to the definitions console which the user can opt in or out of 
    def __sendDefinition(self, msg):
        msg = str(msg)
        self.__definitionsconsole.insert(END, self.__game._getDefinition(msg))

    # Displays the help image 
    def __helpCallback(self):
        window = Toplevel(self.__root)
        window.title("Save Menu")
        window.geometry("1280x720")
        window.configure(bg=self.BACKGROUND)
        Label(window, image=self.__helpimg).pack(fill=BOTH)

##########################
##### SAVING/LOADING #####
##########################

    # Allows the user to enter the file name
    def __setFileName(self):
        if self.__game.pause == True:
            if self.__multiplayergamemode.get() != "Online: 1v1":
                if self.__inprogress == True:
                    window = Toplevel(self.__root)
                    window.title("Save Menu")
                    window.geometry("250x150")
                    window.configure(bg=self.BACKGROUND)

                    frame = Frame(window, bg=self.BACKGROUND)
                    frame.pack(pady=5)

                    Label(window, text="Enter File Name to create/override",bg=self.BACKGROUND, fg=self.FOREGROUND).pack(pady=5)
                    self.__filename = Entry(window, width=25)
                    self.__filename.pack(fill=X)
                    Button(window, text="Apply", command=self.__confirmFileName).pack()
                else:
                    self.__consoleMsg("You cannot save this game at this time!")
            else:
                self.__consoleMsg("You cannot save an online game!")
        else:
            self.__consoleMsg("Please pause the game first!")
    
    def __confirmFileName(self):
        if self.__filename.get() != "":
            self.__saveGame()
        else:
            self.__filename.delete(0, END)
            self.__filename.insert(INSERT, "Error: No File Name")

    # (Group B) Reading and writing to files
    # Performs the save
    # Adds all important game data to an array
    # This array is then dumped into a binary file using the pickle module and uses the user defined name
    def __saveGame(self):
        if self.__online:
            self.__consoleMsg("You can't save this game!")
        else:
            letters = []
            if self.__inprogress == True:
                if self.__game.pause == True:
                    self.__togglePause()
                    try:
                        data = [self.__game._BoardSize, self.__game._MinLength, self.__showdefinitions.get(), self.__incorrectcolour.get(), self.__correctcolour.get(), self.__game.words, self.__game.wordstack, self.__totalguesses, self.__correctcounter, self.__time_left, self.__clicked, self.__gametype.get(), self.__game.timelimit, self.__difficulty.get(), self.__gamemode.get(), self.__lengthchallenge, self.__letterchallenge, self.__onetimeuse, self.__timebattle, self.__gamemodeapproved, self.__wordcount.get(), self.__pausetext.get(), self.__showdefinitions.get(), self.__game._validwords, self.__multiplayergamemode.get()]
                    except AttributeError:
                        self.__gamemodeapproved = False
                        data = [self.__game._BoardSize, self.__game._MinLength, self.__showdefinitions.get(), self.__incorrectcolour.get(), self.__correctcolour.get(), self.__game.words, self.__game.wordstack, self.__totalguesses, self.__correctcounter, self.__time_left, self.__clicked, self.__gametype.get(), self.__game.timelimit, self.__difficulty.get(), self.__gamemode.get(), self.__lengthchallenge, self.__letterchallenge, self.__onetimeuse, self.__timebattle, self.__gamemodeapproved, self.__wordcount.get(), self.__pausetext.get(), self.__showdefinitions.get(), self.__game._validwords, self.__multiplayergamemode.get()]
                    for row in range(self.__game._BoardSize):
                        for col in range(self.__game._BoardSize):
                            letters.append(str(self.__game._Board[row][col]))
                    data.append(letters)
                    if self.__onetimeuse:
                        data.append(self.__availableletters)
                    if self.__difficulty.get() == "Custom":
                        data.append(self.__timeadd)
                        data.append(self.__changecounter)
                        data.append(self.__changeboard.get())
                    if self.__gamemode.get() == "Time Battle":
                        data.append(self.__timeadd)
                    if self.__multiplayergamemode.get() == "AI: Beat Their Score":
                        data.append(self.__scoreToBeat)
                    if self.__multiplayergamemode.get() == "AI: 1v1":
                        data.append(self.__settingscheck)
                        data.append(self.__onevsone)
                        data.append(self.__aidifficulty.get())
                        data.append(self.__aiturntimes)
                        data.append(self.__aiturncounter)
                        data.append(self.__aifound)
                        data.append(self.__aiturn)
                    outputfile = open((self.__filename.get().lower()), 'wb')
                    pickle.dump(data, outputfile)
                    self.__consoleMsg("Saved successfully!")
                    self.__savedgame = True
                    self.__togglePause()
                else:
                    self.__consoleMsg("Please pause the game first!")
            else:
                self.__consoleMsg("Please start the game first!")    

    # User can enter a file name to then be loaded
    def __getFileName(self):
        window = Toplevel(self.__root)
        window.title("Load Menu")
        window.geometry("250x150")
        window.configure(bg=self.BACKGROUND)

        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack(pady=5)

        Label(window, text="Enter File Name to Load",bg=self.BACKGROUND, fg=self.FOREGROUND).pack(pady=5)
        self.__loadfile = Entry(window, width=25)
        self.__loadfile.pack(fill=X)
        Button(window, text="Load Game", command=self.__loadGame).pack()        

    # Performs the load using the pickle module
    # Checks the file name exists before attempting to load, by handling the exception if it does not exist
    # Retrieves the array of data from the binary file
    # Loads all the data into variables/attributes using positions defined when saving
    # Game window reopens with loaded game data
    def __loadGame(self):
        self.__loadproceed = False
        if self.__savedgame == True:
            window = Toplevel(self.__root)
            window.title("Load Status")
            window.geometry("300x60")
            window.configure(bg=self.BACKGROUND)
            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack()
            login_label = Label(window, text="Please restart the application before loading a game!", bg=self.BACKGROUND, fg="#fa0000")
            login_label.pack()
            Button(window, text="Exit",command=window.destroy, background=self.BACKGROUND).pack(side=BOTTOM,pady=5)
        else:   
            self.__loadproceed = True
            filename = (self.__loadfile.get()).lower()
            try:
                inputfile = open(filename, 'rb')
            except FileNotFoundError:
                self.__loadfile.delete(0, END)
                self.__loadfile.insert(INSERT, "Error: Invalid File Name")
                self.__loadproceed = False
            if self.__loadproceed == True:
                data = pickle.load(inputfile)
                self.__loadinggame = True
                self.__game._BoardSize = data[0]
                self.__game._MinLength = data[1]
                self.__game.time = data[9]
                self.__time_left = data[9]
                self.__timeleft.set(data[9])
                self.__game.time = data[9]
                self.__lengthchallenge = data[15]
                if self.__lengthchallenge:
                    self.__lengthchall = random.randint(3,6)
                self.__letterchallenge = data[16]
                if self.__letterchallenge:
                    self.__currletter = Game.LETTERCHALLENGELETTERS[random.randint(0,len(Game.LETTERCHALLENGELETTERS)-1)]
                self.__onetimeuse = data[17]
                self.__timebattle = data[18]
                self.__showdefinitions.set(data[2])
                self.__playCallback()
                self.__game.words = data[5]
                self.__game.wordstack = data[6]
                self.__totalguesses = data[7]
                self.__correctcounter = data[8]
                self.__clicked = data[10]
                self.__gametype.set(data[11])
                self.__game.timelimit = data[12]
                self.__difficulty.set(data[13])
                self.__gamemode.set(data[14])
                self.__gamemodeapproved = data[19]
                self.__wordcount.set(data[20])
                self.__pausetext.set(data[21])
                self.__showdefinitions.set(data[22])
                self.__game._validwords = data[23]
                self.__multiplayergamemode.set(data[24])
                board = data[25]
                if self.__onetimeuse == True and self.__difficulty.get() != "Custom":
                    self.__availableletters = data[26]
                if self.__timebattle == True and self.__difficulty.get() != "Custom":
                    self.__timeadd = int(data[26])
                if self.__difficulty.get() == "Custom" and self.__timebattle != True and self.__onetimeuse != True:
                    self.__timeadded = int(data[26])
                    self.__changecounter = data[27]
                    self.__changeboard.set(data[28])
                if self.__difficulty.get() == "Custom" and self.__onetimeuse == True:
                    self.__availableletters = data[26]
                    self.__timeadd = int(data[27])
                    self.__changecounter = data[28]
                    self.__changeboard.set(data[29])
                if self.__difficulty.get() == "Custom" and self.__timebattle == True:
                    self.__timeadd = int(data[26])
                    self.__changecounter = data[27]
                    self.__changeboard.set(data[28])
                if self.__multiplayergamemode.get() == "AI: Beat Their Score":
                    self.__multiplayer = True
                    self.__scoreToBeat = data[26]
                if self.__multiplayergamemode.get() == "AI: 1v1":
                    self.__multiplayer = True
                    self.__settingscheck = data[26]
                    self.__onevsone = data[27]
                    self.__aidifficulty.set(data[28])
                    self.__aiturntimes = data[29]
                    self.__aiturncounter = data[30]
                    self.__aifound = data[31]
                    self.__aiturn = data[32]
                    if self.__aiturn == True:
                        self.__consoleMsg("It is currently the AIs turn!")
                        self.__changeBoardColour("#737373")
                i=0
                for _ in range(self.__game._BoardSize):
                    for x in range(self.__game._BoardSize):
                        self.__game._Board[_][x] = board[i]
                        i += 1
                for row in range(self.__game._BoardSize):
                    for col in range(self.__game._BoardSize):
                        b = StringVar()
                        b.set(self.__game.at(row+1,col+1))
                        self.__buttons[row][col].set(b.get()) 

    # Allows user to enter custom game settings to play
    def __gameSettingsCallback(self):
        self.__settingscheck = False
        changeboardfrequency = [0,1,2,3,4,5]
        self.__changeboard = StringVar()
        self.__changeboard.set(0)
        if not self.__inprogress:
            window = Toplevel(self.__root)
            window.title("Game Configuration")
            window.geometry("640x480")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Game Configuration", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)

            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            
            self.__boardsizesetting = Entry(window, width=25)
            self.__boardsizesetting.pack()
            self.__boardsizesetting.insert(0, "Enter Board Size (5-10)")
            sizeconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setBoardSize)
            sizeconfirm.pack()

            self.__minlengthsetting = Entry(window, width=25)
            self.__minlengthsetting.pack()
            self.__minlengthsetting.insert(0, "Enter Min Word Length")
            lengthconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setMinLength)
            lengthconfirm.pack()

            self.__timesetting = Entry(window, width=25)
            self.__timesetting.pack()
            self.__timesetting.insert(0, "Enter Time Limit (Seconds up to 3600)")
            timeconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setGameTime)
            timeconfirm.pack()

            self.__timeadded = Entry(window, width=25)
            self.__timeadded.pack()
            self.__timeadded.insert(0, "Enter Time Added on Correct Guess")
            timeaddedconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setTimeAdded)
            timeaddedconfirm.pack()

            change = Label(window, text="How often do you want to change the letters in the board?")
            change.pack(pady=5)
            changeboard = OptionMenu(window, self.__changeboard, *changeboardfrequency)
            changeboard.pack()

            exit = Button(window, text="Start Game", command=lambda:[self.__checkSettings(), window.destroy()])
            exit.pack(pady=10,side=BOTTOM)

#########################
##### CLIENT/SERVER #####
#########################

    # Allows user to select a multipler gamemode (AI or Online)
    def __multiplayerCallback(self):
        self.__multiplayergamemode = StringVar()
        self.__multiplayergamemode.set("AI: Beat Their Score")
        gamemodes = ["AI: Beat Their Score", "AI: 1v1", "Online: 1v1"]
        window = Toplevel(self.__root)
        window.title("Multiplayer Configuration")
        window.geometry("640x480")
        window.configure(bg=self.BACKGROUND)
        window_label = Label(window, text="Multiplayer Configuration", bg=self.BACKGROUND, fg=self.FOREGROUND)
        window_label.pack(pady=10)

        frame = Frame(window, bg=self.BACKGROUND)
        frame.pack(pady=5)

        gamemodelabel = Label(window, text="Gamemode", bg=self.BACKGROUND, fg=self.FOREGROUND)
        gamemodelabel.pack(pady=5)
        gamemode = OptionMenu(window, self.__multiplayergamemode, *gamemodes)
        gamemode.pack()

        exit = Button(window, text="Start Game", command=lambda:[self.__startMultiplayerGamemode(), window.destroy()])
        exit.pack(pady=10,side=BOTTOM)

    def __startMultiplayerGamemode(self):
        self.__multiplayer = True
        if self.__multiplayergamemode.get() == "AI: Beat Their Score":
            self.__gametypeCallback()
        elif self.__multiplayergamemode.get() == "AI: 1v1":
            self.__versusAISetup()
        elif self.__multiplayergamemode.get() == "Online: 1v1":
            self.__setupOnline()
        else:
            self.__multiplayer = False
            self.__gameSettingsCallback()
    
    # User can choose to host or join an online game
    def __setupOnline(self):
            window = Toplevel(self.__root)
            window.title("Online Configuration")
            window.geometry("400x225")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Online Configuration", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            self.__online = True

            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)

            Button(window, text="Host Game", command=lambda: [self.__setupOnlineSettings(), window.destroy()], background=self.BACKGROUND).pack(pady=5)
            Button(window, text="Join Game", command=lambda: [self.__tryJoin(), window.destroy()], background=self.BACKGROUND).pack(pady=5)

            close = Button(window, text="Close", command=window.destroy, bg=self.BACKGROUND, fg=self.FOREGROUND).pack(side=BOTTOM, pady=5)

    # Client can attempt to join a game 
    # If no game is available to join, user is redirected back to the main menu
    ############################
    # Excellent Coding Style Demonstrated through:
    # Good Exception Handling
    ############################
    def __tryJoin(self):
        thread = threading.Thread(target=self.__waitToStartOnlineGame)
        try:
            self.__game._joinServer()
            thread.start()
        except ConnectionRefusedError:
            window = Toplevel(self.__root)
            window.title("Connection Error")
            window.geometry("300x100")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Error: No game available to join!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)

            close = Button(window, text="Close", command=window.destroy, bg=self.BACKGROUND, fg=self.FOREGROUND).pack(side=BOTTOM, pady=5)

    # Allows the host to setup game settings for both players to use
    def __setupOnlineSettings(self):
        self.__settingscheck = False
        self.__gamemode.set("None")
        self.__difficulty.set("Medium")
        self.__onevsone = False
        self.__lengthchallenge = False
        self.__onetimeuse = False
        self.__timebattle = False
        self.__letterchallenge = False
        self.__game.time = 60
        self.__timesetting = StringVar()
        self.__timesetting.set(0)
        if not self.__inprogress:
            window = Toplevel(self.__root)
            window.title("Game Configuration")
            window.geometry("400x350")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Game Configuration", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)

            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            
            boardsizelabel = Label(window, text="Board Size", bg=self.BACKGROUND, fg=self.FOREGROUND)
            boardsizelabel.pack()
            self.__boardsizesetting = Entry(window, width=25)
            self.__boardsizesetting.pack()
            self.__boardsizesetting.insert(0, "Enter Board Size (5-10)")
            sizeconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setBoardSize)
            sizeconfirm.pack()

            minlengthlabel = Label(window, text="Minimum Word Length", bg=self.BACKGROUND, fg=self.FOREGROUND)
            minlengthlabel.pack(pady=5)
            self.__minlengthsetting = Entry(window, width=25)
            self.__minlengthsetting.pack()
            self.__minlengthsetting.insert(0, "Enter Min Word Length")
            lengthconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setMinLength)
            lengthconfirm.pack()

            timelabel = Label(window, text="Enter Time Limit", bg=self.BACKGROUND, fg=self.FOREGROUND)
            timelabel.pack(pady=5)
            self.__timesetting = Entry(window, width=25)
            self.__timesetting.pack()
            self.__timesetting.insert(0, "Enter Time Limit")
            lengthconfirm = Button(window, text="Apply", activebackground="spring green")
            lengthconfirm.pack()            

            exit = Button(window, text="Start Game", command=lambda:[self.__checkOnlineSettings(), window.destroy()])
            exit.pack(pady=10,side=BOTTOM)

    ####################
    # Excellent coding style demonstrated through:
    # Defensive programming
    # Exception Handling
    ####################
    # Validates any entries by user before starting game
    # Error messages are shown if the user enters a wrong input
    def __checkOnlineSettings(self):
        if self.__inprogress != True:
            try:
                if int(self.__timesetting.get()) >= 10:
                    self.__game.time = int(self.__timesetting.get())
                if (int(self.__boardsizesetting.get()) >= 5 and int(self.__boardsizesetting.get()) <= 9) and int(self.__timesetting.get()) >= 10:
                    self.__game._createServer()
                    thread = threading.Thread(target=self.__waitToStartOnlineGame)
                    thread.start()
                else:
                    window = Toplevel(self.__root)
                    window.title("Error")
                    window.geometry("325x150")
                    window.configure(bg=self.BACKGROUND)
                    window_label = Label(window, text="Incorrect Board Size/Time Limit Entered \n Please Change!", bg=self.BACKGROUND, fg=self.FOREGROUND)
                    window_label.pack(pady=10)
                    window_label2 = Label(window, text="(Board Size must be less than or equal to 9 for Online Mode)", bg=self.BACKGROUND, fg=self.FOREGROUND)
                    window_label2.pack()
                    window_label3 = Label(window, text="(Time limit must be greater than 10s for Online Mode)", bg=self.BACKGROUND, fg=self.FOREGROUND)
                    window_label3.pack()
                    frame = Frame(window, bg=self.BACKGROUND)
                    frame.pack(pady=5)
                    exit = Button(window, text="Close", command=window.destroy)
                    exit.pack(side=BOTTOM)
            except:
                window = Toplevel(self.__root)
                window.title("Error")
                window.geometry("400x150")
                window.configure(bg=self.BACKGROUND)
                window_label = Label(window, text="Incorrect Settings! \n Please try again!", bg=self.BACKGROUND, fg=self.FOREGROUND)
                window_label2 = Label(window, text="(Program may need to be restarted if already tried to host once)", bg=self.BACKGROUND, fg=self.FOREGROUND)               
                window_label.pack(pady=10)
                window_label2.pack()
                frame = Frame(window, bg=self.BACKGROUND)
                frame.pack(pady=5)
                exit = Button(window, text="Close", command=window.destroy)
                exit.pack(side=BOTTOM)
    
    # A thread which is started for both client and server
    # If client: The method sets the game settings retrieved from the host and starts the game
    # If server: The method forces the user to wait for the other player to join
    def __waitToStartOnlineGame(self):
        if self.__game.server:
            window = Toplevel(self.__root)
            window.title("Please Wait...")
            window.geometry("300x50")
            window.configure(bg=self.BACKGROUND)
            # defines a protocol on the window that calls the cancelWait method to end thread otherwise whole program continues running.
            window.protocol("WM_DELETE_WINDOW", self.__cancelWait)
            window_label = Label(window, text="Please wait for Player 2 to join!", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)
            while not self.__game._onlinestart:
                pass
            if self.__game._onlinestart and self.__cancelOnline == False:
                self.__playCallback()
            else:
                self.__game._endServer()
            window.destroy()
        if self.__game.client:
            self.__gamemode.set("None")
            self.__difficulty.set("Medium")
            self.__onevsone = False
            self.__lengthchallenge = False
            self.__onetimeuse = False
            self.__timebattle = False
            self.__letterchallenge = False
            while self.__game._onlinestart == False:
                pass
            if self.__game._onlinestart and self.__cancelOnline == False:
                self.__playCallback()

    # Ends threads, called if the user closes the waiting for player 2 window or closes program.
    def __cancelWait(self):
        self.__game._onlinestart = True
        self.__cancelOnline = True

##############
##### AI #####
##############

    # Sets the score for the user to beat
    def __setScoreToBeat(self, score):
        self.__aidifficulty = self.__difficulty
        self.__gamemode.set("AI: Beat Their Score")
        self.__scoreToBeat = score

    # Allows user to enter settings for an AI 1v1 Game
    def __versusAISetup(self):
        self.__settingscheck = False
        self.__gamemode.set("AI: 1v1")
        self.__onevsone = True
        self.__lengthchallenge = False
        self.__onetimeuse = False
        self.__timebattle = False
        self.__letterchallenge = False
        self.__game.time = 15
        self.__timesetting = StringVar()
        self.__timesetting.set(0)
        difficulties = ["Easy", "Medium", "Hard"]
        self.__aidifficulty = StringVar()
        self.__aidifficulty.set("Medium")
        if not self.__inprogress:
            window = Toplevel(self.__root)
            window.title("Game Configuration")
            window.geometry("400x300")
            window.configure(bg=self.BACKGROUND)
            window_label = Label(window, text="Game Configuration", bg=self.BACKGROUND, fg=self.FOREGROUND)
            window_label.pack(pady=10)

            frame = Frame(window, bg=self.BACKGROUND)
            frame.pack(pady=5)
            
            boardsizelabel = Label(window, text="Board Size", bg=self.BACKGROUND, fg=self.FOREGROUND)
            boardsizelabel.pack()
            self.__boardsizesetting = Entry(window, width=25)
            self.__boardsizesetting.pack()
            self.__boardsizesetting.insert(0, "Enter Board Size (5-10)")
            sizeconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setBoardSize)
            sizeconfirm.pack()

            minlengthlabel = Label(window, text="Minimum Word Length", bg=self.BACKGROUND, fg=self.FOREGROUND)
            minlengthlabel.pack(pady=5)
            self.__minlengthsetting = Entry(window, width=25)
            self.__minlengthsetting.pack()
            self.__minlengthsetting.insert(0, "Enter Min Word Length")
            lengthconfirm = Button(window, text="Apply", activebackground="spring green", command=self.__setMinLength)
            lengthconfirm.pack()

            difficultylabel = Label(window, text="Difficulty", bg=self.BACKGROUND, fg=self.FOREGROUND)
            difficultylabel.pack(pady=5)
            difficulty = OptionMenu(window, self.__aidifficulty, *difficulties)
            difficulty.pack()

            exit = Button(window, text="Start Game", command=lambda:[self.__checkSettings(), window.destroy()])
            exit.pack(pady=10,side=BOTTOM)

    def __setAIDifficulty(self):
        self.__aiturntimes = []
        self.__aiturntimes = self.__AI._setAITurnTimes(self.__aidifficulty.get(), self.__aiturntimes)
    
    # Calls the game method to do the AI turn
    # Gets the result, if none then nothing happens until the timer reaches another time for the AI to try again
    # If the AI did find a word then the turn swaps to the other player
    def __doAITurn(self):
        self.__changeBoardColour("#737373")
        self.__aiturncounter += 1
        self.__selected.config(state="normal")
        self.__selected.delete(1.0, END)
        self.__selected.insert(INSERT, "AI Turn...")
        self.__selected.config(state="disabled")
        word = self.__AI._doVersusTurn(self.__aiturncounter, self.__game._validwords, self.__game._MinLength, self.__aifound, self.__game.words)
        if word != None:
            self.__time_left = 15
            self.__game.time_left = 15
            self.__aifound.append(str(word).upper())
            self.__consoleMsg("AI has found word: " + str(word).upper())
            self.__changeBoardColour(self.BACKGROUND)
            self.__aiturn = False
            self.__selected.config(state="normal")
            self.__selected.delete(1.0, END)
            self.__selected.config(state="disabled")
            self.__time_left = 15
            self.__game.time_left = 15

##############################
##### FINISHING THE GAME #####
##############################

    # Ends the game and displays the statistics window
    def __finish(self):
        if self.__gamestarted == True:
            if self.__timeleft.get() != "Unlimited":
                self.__timeused = (self.__game.timelimit - self.__time_left)
            self.__game.wordstack = []
            self.__clicked = []
            self.__otherscore = self.__game._doFinish()
            self.__time_left = 1
            self.__timelefttext.destroy()
            if not self.__quitting:
                self.__consoleMsg("Ending game...")
                self.__clearSelection()
            self.__gamestarted = False
            self.__inprogress = False
            if not self.__quitting:
                self.__timeleft.set("Time is up!")
                self.__selected.config(state="normal")
                self.__selected.delete(1.0, END)
                self.__selected.insert(INSERT, "Words Found: " +  str(self.__correctcounter))
                self.__selected.config(state="disabled")
                self.__statistics()

    def _quitGame(self):
        if self.__multiplayergamemode.get() == "Online: 1v1":
            self.__consoleMsg("(This game window will not close until the other player finishes/exits!)")
            time.sleep(0.01)
        self.__inprogress = False
        if not self.__online:
            self.__game._doFinish()
        if self.__online:
            self.__game._endServer() 
        self.__finish() 
        self.__gamewindow.destroy()
        self.__resetGame()

    # Shows information such as score, words found, gamemode and difficulty
    # Shows gamemode specific information such as whether you beat the AI
    # Shows online information such as whether you beat your opponent and what their score was
    # Adds the game information to the database if the user is logged in
    def __statistics(self):
        stringofwords = ""
        window = Toplevel(self.__gamewindow)
        window.title("Game Statistics")
        if len(self.__game.words) >= 10:
            window.geometry("800x600")
        else:
            window.geometry("600x500")
        window.configure(bg=self.BACKGROUND)
        window_label = Label(window, text="Statistics", font=(self.FONT, 18), bg=self.BACKGROUND, fg=self.FOREGROUND)
        window_label.pack(pady=10)
        if self.__difficulty.get() == "Medium":
            difficultymultiplier = 2
        if self.__difficulty.get() == "Hard":
            difficultymultiplier = 3
        else:
            difficultymultiplier = 1
        finalscore = self.__game._totalscore * difficultymultiplier
        if self.__online:
            if int(self.__otherscore) < self.__game._totalscore:
                outcome = "You Won!"
            elif int(self.__otherscore) > self.__game._totalscore:
                outcome = "You Lost!"
            else:
                outcome = "You Drew!"
            beaten = Label(window, text="Outcome: " + str(outcome), font=(self.FONT, 12), bg=self.BACKGROUND, fg=self.FOREGROUND)
            beaten.pack(pady=5)
            otherscore = Label(window, text="Opponents Score: " + str(self.__otherscore), font=(self.FONT, 12), bg=self.BACKGROUND, fg=self.FOREGROUND)
            otherscore.pack(pady=5)
        if self.__gamemode.get() == "AI: 1v1":
            beaten = Label(window, text="Beaten AI: " + str(self.__aiturn), font=(self.FONT, 12), bg=self.BACKGROUND, fg=self.FOREGROUND)
            beaten.pack()
        score = Label(window, text="Total Score: " + str(finalscore), font=(self.FONT, 12), bg=self.BACKGROUND, fg=self.FOREGROUND)
        score.pack(pady=5)
        totalguesses = Label(window, text="Total Guesses: " + str(self.__totalguesses), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        totalguesses.pack()
        wordsfound = Label(window, text="Words Found: " + str(self.__correctcounter), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        wordsfound.pack()
        incorrectguesses = Label(window, text="Incorrect Guesses: " + str(self.__totalguesses-self.__correctcounter), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        incorrectguesses.pack()
        if self.__gamemode == "None":
            totaltime = Label(window, text="Time Limit: " + str(self.__game.timelimit) + "s", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
            totaltime.pack()
            timeused = Label(window, text="Time Used: " + str(self.__timeused+1) + "s", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
            timeused.pack()
        if "AI:" not in self.__gamemode.get():
            difficulty = Label(window, text="Difficulty: " + str(self.__difficulty.get()), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
            difficulty.pack()
        else:
            difficulty = Label(window, text="Difficulty: " + str(self.__aidifficulty.get()), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
            difficulty.pack()
        if self.__gamemode.get() != "None":
            gamemode = Label(window, text="Gamemode: " + str(self.__gamemode.get()), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
            gamemode.pack()
        if self.__multiplayer == True:
            if self.__multiplayergamemode.get() == "AI: Beat Their Score":
                scorebeaten = Label(window, text="Beaten AI Score: " + str(self.__scorebeaten), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
                scorebeaten.pack()
        for word in self.__game.words:
            if self.__game.words.index(word) != len(self.__game.words)-1:
                stringofwords += (word + ", ")
            else:
                stringofwords += word
        if len(self.__game.words) == 0:
            stringofwords = "No words found!"
        words = Label(window, text="Words Found: " + str(stringofwords), font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        words.pack()
        self.__addGameEntry()
        Button(window, text="Return to Menu",command=lambda:[self._quitGame(), window.destroy()], background=self.BACKGROUND).pack(side=BOTTOM)  
        Button(window, text="Leaderboard",command=self.__createLeaderboard, background=self.BACKGROUND, font=(self.FONT, 11)).pack(side=BOTTOM, pady=5)    

    # Retrieves all database entries from games on the same gamemode and difficulty
    # Displays this data in a leaderboard style with positions (highest score in 1st place etc)
    # If the user achieved a score higher than someone on the leaderboard, they are displayed in green
    def __createLeaderboard(self):
        window = Toplevel(self.__root)
        window.geometry("725x900")
        window.configure(bg=self.BACKGROUND)
        window.grid_columnconfigure(2, weight=1)
        data = []
        gamemode = self.__gamemode.get()
        difficulty = self.__difficulty.get()
        if gamemode == "None":
            gamemode = "No"
        window.title("Leaderboard for " + gamemode + " Gamemode on " + difficulty + " Difficulty:")
        positioncol = 0
        usernamecol = 2
        durationcol = 4
        wordsfoundcol = 6
        scorecol = 8
        datecol = 10
        position = Label(window, text="Position", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        position.grid(row=1,column=0, padx=30, pady=15)
        username = Label(window, text="Username", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        username.grid(row=1,column=2, padx=30, pady=15)
        duration = Label(window, text="Duration", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        duration.grid(row=1,column=4, padx=30, pady=15)
        wordsfound = Label(window, text="Words Found", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        wordsfound.grid(row=1,column=6, padx=30, pady=15)
        scoremainlabel = Label(window, text="Score", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        scoremainlabel.grid(row=1,column=8, padx=30, pady=15)
        scoremainlabel = Label(window, text="Date", font=(self.FONT, 10), bg=self.BACKGROUND, fg=self.FOREGROUND)
        scoremainlabel.grid(row=1,column=10, padx=30, pady=15)
        data = self.__database._getLeaderboardData(self.__gamemode.get(), self.__difficulty.get())
        for dataset in data:
            fg = self.FOREGROUND
            if data.index(dataset) < 15:
                username = self.__database._getUsernameFromID(dataset[0])
                gameid = dataset[1]
                gamelength = dataset[2]
                score = dataset[3]
                wordsfound = dataset[4]
                date = dataset[5]
                if gameid == self.__database._getLatestGameID() and self.__username != "":
                    fg = "#118000"
                positionlabel = Label(window, text=str(data.index(dataset)+1), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                positionlabel.grid(row=(data.index(dataset)+2), column=positioncol, padx=35, pady=15)
                usernamelabel = Label(window, text=str(username), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                usernamelabel.grid(row=(data.index(dataset)+2), column=usernamecol, padx=35, pady=15)
                gamelengthlabel = Label(window, text=str(gamelength) + "s", font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                gamelengthlabel.grid(row=(data.index(dataset)+2), column=durationcol, padx=35, pady=15)
                scorelabel = Label(window, text=str(score), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                scorelabel.grid(row=(data.index(dataset)+2), column=scorecol, padx=35, pady=15)
                wordsfoundlabel = Label(window, text=str(wordsfound), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                wordsfoundlabel.grid(row=(data.index(dataset)+2), column=wordsfoundcol, padx=35, pady=15)
                datelabel = Label(window, text=str(date), font=(self.FONT, 10), bg=self.BACKGROUND, fg=fg)
                datelabel.grid(row=(data.index(dataset)+2), column=datecol, padx=35, pady=15)
        Button(window, text="<- Back",command=lambda:[window.destroy()], background=self.BACKGROUND).grid(row=0,column=0,columnspan=10,sticky="nw")

    def __quitCallback(self):
        if self.__inprogress:
            if self.__game.pause:
                self.__togglePause()
            self.__stoptimer = True
        self.__quitAll()

    # Ends the whole program
    # Toggles pause if the game is paused as the while loop would keep the program open
    # Destroys and quits the root, closing the gui
    # If the server is still open it gets closed, wouldn't work if no online game was played so an exception is handled. 
    def __quitAll(self):
        if self.__online:
            if self.__game._onlinestart == False:
                self.__game._onlinestart = True
            self.__game._endServer()
        self.__quitting = True
        if self.__inprogress:
            self.__finish()
            if self.__game.pause:
                self.__togglePause()
        self.__database._closeConnection()
        self.__root.destroy()
        self.__root.quit()
        try:
            self.__cancelWait()
            self.__game.server.server.close()
        except:
            pass

############################
# Group A Skill
# OOP: Classes
############################

############################
# Group A Skill 
# OOP: Inheritance
############################

class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def run(self):
        self.__game._checkMultiplayer()

if __name__ == "__main__":
    g = Gui()