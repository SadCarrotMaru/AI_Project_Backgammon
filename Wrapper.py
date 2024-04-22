import backgammon as backgammon
import AI as AI
import sys

DEPTH = 3

# Wrapper for the whole project. This is the file that is ran when you want to play with the AI.
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == 'Easy':
            DEPTH = 1
        elif args[0] == 'Medium':
            DEPTH = 3
        else:
            DEPTH = 4
    app = backgammon.Application(True) # The game itself
    AI_MODEL = AI.Engine(DEPTH) # The AI
    while True:
        Board, Rolls = app.AI_update() # Gets the current configuration
        #print(Board)
        if Board is not None:  # Then it is its turn
            app.update()   # Updates
            New_State = AI_MODEL.get_prediction_for(Board, 'MAX', 'W', Rolls)  #Get the best move for the AI
            #print(New_State)
            app.need_to_roll = True  # Tells the Applications that the AI moved
            app.switch_game_status(New_State, 'W', []) # Switches the game to the state that the AI returned
        app.update() # Updates



     