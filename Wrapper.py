import backgammon as backgammon
import AI as AI


if __name__:
    app = backgammon.Application(True)
    AI_MODEL = AI.Engine(3)
    while True:
        Board, Rolls = app.AI_update()
        #print(Board)
        if Board is not None:
            print(Board, Rolls)
            app.update()
            New_State = AI_MODEL.get_prediction_for(Board, 'MAX', 'W', Rolls)
            print(New_State)
            app.need_to_roll = True 
            app.switch_game_status(New_State, 'W', [])
        app.update()



     