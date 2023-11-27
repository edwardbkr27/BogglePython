import Gui
from sys import argv

# Uses argv to allow user to enter t or g arguments to run the game as terminal or GUI
def usage():   
    print(f"""
Usage: {argv[0]} [g | t]
g  = play with a graphical user interface
t  = play using the terminal

Please relaunch and try again.""")
    quit()
# Creates either a terminal or gui game based on user input argument
if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    elif argv[1] == "t":
        ui = Gui.Terminal()
    elif argv[1] == "g":
        ui = Gui.Gui()
    else:
        usage()

    ############################
    # Group A Skill 
    # OOP: Polymorphism    
    ############################
    ui.run()
