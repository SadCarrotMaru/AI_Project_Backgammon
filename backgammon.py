import pygame
import copy
import sys
import os
import time
import random
import soft_config_const as const
from Objects.Board import Board
from Objects.Button import Button
from Objects.Dice import Dice
from Objects.Piece import Piece
from Objects.Board_triangle import Board_triangle

class Application():
    def __init__(self, interface_true = False) -> None:
        '''
        Constructor for the main application class. The game will be played in this class and so it contains 
        every variable there is needed to describe the status of the game.
        '''
        self.clock = pygame.time.Clock()
        if interface_true == True: self.screen = pygame.display.set_mode((const.HEIGHT,const.WIDTH))
        self.bg = pygame.image.load("Assets/board.png")
        self.board = Board()
        self.dice_1 = Dice(const.POS_X_DICE_1, const.POS_Y_DICE_1, const.SEED_DICE_1)
        self.dice_2 = Dice(const.POS_X_DICE_2, const.POS_Y_DICE_2, const.SEED_DICE_2)
        self.start_time_roll = round(time.time() * 1000) - 1005
        self.need_to_roll = True
        self.button_roll = Button(const.BUTTON_ROLL_X, const.BUTTON_ROLL_Y,"Roll dices!",const.SKY_BLUE)
        self.currently_highlighted = []
        self.current_piece_selected = None
        self.rolls = []
        self.need_to_update_rolls = False
        self.turn = 'B'
        self.BLACK_IS_ABLE_TO_RETRIEVE = False
        self.WHITE_IS_ABLE_TO_RETRIEVE = False
        self.WINNER = None
        self.WIN_TRIGGERED = False
        self.score_player_1 = 0
        self.score_player_2 = 0


    def AI_update(self) -> None:
        '''
        The update function which is called for the AI. If it's not its turn and it got called it has to roll the dices, and afterwards
        it will return the status of the game so that it knows what board to predict a move for.
        '''
        if self.turn == 'B' and self.need_to_roll == True: ## Reversed, B if it's White's turn and vice versa
            self.button_pressed()
        if self.turn == 'W' and self.need_to_update_rolls == False and self.need_to_roll == False:
            return self.board.frames, self.rolls
        return None, None


    def switch_game_status(self, board_frames, turn, rolls) -> None:
        '''
        This function helps as a utility function for its virtual instance in the AI. It emulates a board position so that it can use
        some of the existent methods in the class.
        '''
        self.board = Board(board_frames)
        self.board.update_board()
        self.turn = turn
        self.rolls = rolls


        self.all_sprites = pygame.sprite.Group()
        for piece in self.board.get_pieces():
            self.all_sprites.add(piece)
        self.BLACK_IS_ABLE_TO_RETRIEVE = self.able_to_retrieve_pieces('B')
        self.WHITE_IS_ABLE_TO_RETRIEVE = self.able_to_retrieve_pieces('W')

    def get_moves_for_position(self, position) -> list:
        '''
        Also used for the AI. Given a position, it generates a virtual piece that is used to see what rolls can be used with a piece from
        the given position.
        '''
        possibilites = []
        if len(self.board.frames[position]) > 0 and self.board.frames[position][0] == self.turn:
            piece = Piece(self.turn, 0, 0, 0, position)
            if self.satisfy_special_condition(piece):
                possibilites = self.get_possible_moves(piece)
        return possibilites


    def update_board(self) -> None:
        '''
        One of the main update functions which handles the triangles from the board. (highlighted or not).
        '''
        board_triangles = self.board.get_triangles()
        for triangle in board_triangles:
            triangle.display(self.screen)


    def not_in_blocked_state(self) -> bool:     
        '''
        Checks if there are any available moves for the player that has to move.
        '''
        for sprite in self.all_sprites:
            if (self.turn == 'B' and sprite.color == const.BLACK) or (self.turn == 'W' and sprite.color == const.WHITE):
                possibilites = len(self.get_possible_moves(sprite))
                if possibilites != 0 and self.satisfy_special_condition(sprite) == True:
                    return True
        return False

    def update_dice(self) -> None:
        '''
        Update dice is also one of the main functions. The way it works is:
            If the need to roll variable is true then a button that prompts the player to roll is displayed.
            If that condition is satisfied then for a second after the player pressed the buttons, the dices will 'roll', generating
            a random number every update. After a second, those final rolls are being cast into the game rolls and used afterwards
            as the numbers that were rolled by the player.
        '''
        if self.need_to_roll == True:
            self.screen.blit(self.button_roll.image, self.button_roll.rect)


        if round(time.time() * 1000) - self.start_time_roll < 1000:
            self.dice_1.roll()
            self.dice_2.roll()
        else:
            if self.need_to_update_rolls == True:
                self.rolls = []
                self.rolls = [self.dice_1.value, self.dice_2.value]
                if self.dice_1.value == self.dice_2.value:
                    self.rolls.append(self.dice_1.value)
                    self.rolls.append(self.dice_1.value)
                self.need_to_update_rolls = False
        self.screen.blit(self.dice_1.image, self.dice_1.rect) 
        self.screen.blit(self.dice_2.image, self.dice_2.rect) 
    

    def able_to_retrieve_pieces(self, color) -> None:
        '''
        Checks if the player with color 'color' is able to retrieve pieces (a.k.a all the pieces he has are in his home)
        '''
        for sprite in self.all_sprites:
            if (color == 'B' and sprite.color == const.BLACK):
                if sprite.current_position_on_board <= 18:
                    return False           
            elif (color == 'W' and sprite.color == const.WHITE):     
                if sprite.current_position_on_board >= 7:
                    return False
        return True

    def update_pieces(self) -> None:
        '''
        One of the main update function that handles the update for every piece on the board.
        '''
        self.all_sprites = pygame.sprite.Group()
        for piece in self.board.get_pieces():
            self.all_sprites.add(piece)
        
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

    def show_final_screen(self) -> None:
        '''
        Endgame screen. Horribly written code but it fulfills its job.
        '''
        self.clock.tick(60)
        color_ = const.BLACK
        op_color_  = const.WHITE
        if self.WINNER == 'WHITE':
            color_=const.WHITE
            op_color_ = const.BLACK

        self.screen.fill(color_)
        pygame.init()
        font = pygame.font.SysFont(None, 50)
        text_surface = font.render(f"{self.WINNER} won the game!", True, op_color_)
        text_rect = text_surface.get_rect()
        text_rect.center = (const.WIDTH/2, 200)
        self.screen.blit(text_surface, text_rect) 

        text_surface = font.render(f"The score is {self.score_player_1} - {self.score_player_2}", True, op_color_)
        text_rect = text_surface.get_rect()
        text_rect.center = (const.WIDTH/2, 250)
        self.screen.blit(text_surface, text_rect) 

        button_width = 200
        button_height = 50
        button_x = (const.WIDTH - button_width) // 2
        button_y = 500
        button_color = (128, 128, 128)
        button_text = "Play Again"
        
        pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))
        text_surface = font.render(button_text, True, op_color_)
        text_rect = text_surface.get_rect()
        text_rect.center = (button_x + button_width / 2, button_y + button_height / 2)
        self.screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    self.need_to_roll = True
                    self.currently_highlighted = []
                    self.current_piece_selected = None
                    self.rolls = []
                    self.need_to_update_rolls = False
                    self.turn = 'B'
                    self.BLACK_IS_ABLE_TO_RETRIEVE = False
                    self.WHITE_IS_ABLE_TO_RETRIEVE = False
                    self.WINNER = None
                    self.WIN_TRIGGERED = False
                    self.board = Board(const.PIECES_POSITION_INITIAL)


        pygame.display.flip()
   
        
    
    def update(self) -> None:
        '''
        The update function which is called to make the game progress. It handles every update that has to be done in the game and
        any event that can happen during the game.
        '''
        if self.WIN_TRIGGERED == True:
            self.show_final_screen()
            return

        self.clock.tick(60)
        if self.turn == 'B':
            self.screen.fill(const.BLACK)
        else:
            self.screen.fill(const.WHITE)
        self.screen.blit(self.bg, (0, 0))
        self.x,self.y = pygame.mouse.get_pos()
       
        
        self.update_board()
        self.update_pieces()
        self.update_dice()
        self.check_win_status()

        if self.WIN_TRIGGERED == True:
            print(f"The player who won the game is *drum rolls* .. {self.WINNER}")

        self.BLACK_IS_ABLE_TO_RETRIEVE = self.able_to_retrieve_pieces('B')
        self.WHITE_IS_ABLE_TO_RETRIEVE = self.able_to_retrieve_pieces('W')
        
        if self.need_to_update_rolls == False and (len(self.rolls) == 0 or self.not_in_blocked_state() == False):
            self.need_to_roll = True 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check((self.x,self.y))

        pygame.display.flip()
        pygame.display.update()

    def get_candidates_triangles_showlight(self, piece, list_candidates) -> list:
        '''
        Being given a piece and the positions that can be reached with the rolls, it checks the special conditions that
        occur whilst playing backgammon.
        '''
        candidates = set(list_candidates)
        if piece.color == const.BLACK:
            type_piece = 'B'
        else:
            type_piece = 'W'

        list_triangle_positions = []
        for triangle_pos in candidates:
            it_is_okay = False
            if triangle_pos < 1 or triangle_pos > 24:
                if triangle_pos == 0 and self.WHITE_IS_ABLE_TO_RETRIEVE == True:
                    it_is_okay = True
                elif triangle_pos == 25 and self.BLACK_IS_ABLE_TO_RETRIEVE == True:
                    it_is_okay = True
            else:
                if len(self.board.frames[triangle_pos]) == 0:
                    it_is_okay = True
                else:
                    if len(self.board.frames[triangle_pos]) == 1 or type_piece == self.board.frames[triangle_pos][0]:
                        it_is_okay  = True
            if it_is_okay == True:
                list_triangle_positions.append(triangle_pos)

        return list_triangle_positions


    def triangles_showlight(self, piece, list_candidates):
        '''
        For user interface. It switches the color of the triangles that can be reached by the currently highlighted piece.
        '''
        need_to_highlight = self.get_candidates_triangles_showlight(piece, list_candidates)
        triangles = self.board.get_triangles()
        for pos in need_to_highlight:
            self.currently_highlighted.append(triangles[pos])
            triangles[pos].switch_highlight()


    def show_possible_moves(self, piece) -> None:
        '''
        Being given a piece, and knowing the rolls, it handles the logic for all the possible moves for that piece.
        '''
        direction = 1
        if piece.color == const.WHITE:
            direction = -1

        candidates = []
        special_rule_applicable = False
        if (piece.color == const.WHITE and self.WHITE_IS_ABLE_TO_RETRIEVE == True) or (piece.color == const.BLACK and self.BLACK_IS_ABLE_TO_RETRIEVE == True):
            special_rule_applicable = True
        for roll in self.rolls:
            candidates.append(piece.current_position_on_board + (direction * roll))
            if special_rule_applicable == True:
                if direction == 1:
                    not_okay = False
                    for position_needs_to_be_empty in range(19,piece.current_position_on_board,1):
                        if len([x for x in self.board.frames[position_needs_to_be_empty] if x == 'B']) != 0:
                            not_okay = True
                    if piece.current_position_on_board + (direction * roll) > 25 and not_okay == False:
                        candidates.append(25)
                else:
                    not_okay = False
                    for position_needs_to_be_empty in range(6,piece.current_position_on_board,-1):
                        if len([x for x  in self.board.frames[position_needs_to_be_empty] if x == 'W']) != 0:
                            not_okay = True
                    if piece.current_position_on_board + (direction * roll) < 0 and not_okay == False:
                        candidates.append(0)

        self.triangles_showlight(piece, candidates)

    def get_possible_moves(self, piece) -> list:
        '''
        Same thing as the previous function, however this is an utilitary method for its virtual instance, so that the AI can generate
        more easily its succesors.
        '''
        direction = 1
        if piece.color == const.WHITE:
            direction = -1
        candidates = []
        special_rule_applicable = False
        if (piece.color == const.WHITE and self.WHITE_IS_ABLE_TO_RETRIEVE == True) or (piece.color == const.BLACK and self.BLACK_IS_ABLE_TO_RETRIEVE == True):
            special_rule_applicable = True
        for roll in self.rolls:
            candidates.append(piece.current_position_on_board + (direction * roll))
            if special_rule_applicable == True:
                if direction == 1:
                    not_okay = False
                    for position_needs_to_be_empty in range(19,piece.current_position_on_board,1):
                        if len([x for x in self.board.frames[position_needs_to_be_empty] if x == 'B']) != 0:
                            not_okay = True
                    if piece.current_position_on_board + (direction * roll) > 25 and not_okay == False:
                        candidates.append(25)
                else:
                    not_okay = False
                    for position_needs_to_be_empty in range(6,piece.current_position_on_board,-1):
                        if len([x for x  in self.board.frames[position_needs_to_be_empty] if x == 'W']) != 0:
                            not_okay = True
                    if piece.current_position_on_board + (direction * roll) < 0 and not_okay == False:
                        candidates.append(0)
        return self.get_candidates_triangles_showlight(piece, candidates)

    def check_win_status(self) -> None:
        '''
        Checks if the win status was achieved by any player.
        '''
        no_white_pieces = len([x for x in self.all_sprites if x.color == const.WHITE])
        no_black_pieces = len(self.all_sprites) - no_white_pieces
        
        if no_white_pieces == 0:
            if self.WIN_TRIGGERED == False:
                if no_black_pieces == 15:
                    self.score_player_1 +=2
                else:
                    self.score_player_1 +=1
            self.WIN_TRIGGERED = True
            self.WINNER = 'WHITE'
        elif no_black_pieces == 0:
            if self.WIN_TRIGGERED == False:
                if no_white_pieces == 15:
                    self.score_player_2 +=2
                else:
                    self.score_player_2 +=1
            self.WIN_TRIGGERED = True
            self.WINNER = 'BLACK'

    def move_piece(self, piece, triangle) -> None:
        '''
        Moves a piece on the table and eliminates the roll that was used for it.
        '''
        roll_used = triangle.position_on_board - piece.current_position_on_board
        if roll_used < 0 : roll_used *= -1
        if roll_used in self.rolls: 
            self.rolls.remove(roll_used)
        else:
            self.rolls.remove(max(self.rolls))
        self.board.move_piece(piece.current_position_on_board, triangle.position_on_board)

    def reset_highlighted(self) -> None:
        '''
        After a piece was deselected, we want to remove all the highlighted pieces, so we created this method for this purpose.
        '''
        for element in self.currently_highlighted:
            if isinstance(element, Board_triangle):
                element.switch_highlight()
        self.currently_highlighted = []
        #self.current_piece_selected = None

    def sprite_is_at_turn(self, sprite) -> bool:
        '''
        Being given a piece, it returns if it is allowed to move or not.
        '''
        type_ = 'W'
        if sprite.color == const.BLACK:
            type_ = 'B'
        if self.turn == type_:
            return True
        return False
    

    def satisfy_special_condition(self, sprite) -> bool:
        '''
        When removing pieces from the board, sometimes if a higher value than all the possible ones is rolled, then it can be
        used to remove a piece. When this happens we say it satisfies the special condition.
        '''
        if sprite.color == const.BLACK and len(self.board.frames[0]) > 0 and sprite.current_position_on_board != 0:
            return False
        if sprite.color == const.WHITE and len(self.board.frames[25]) > 0 and sprite.current_position_on_board != 25:
            return False
        return True
    
    def button_pressed(self) -> None:
        '''
        Logic for the button to roll the dice. Here the players switch turns.
        '''
        self.start_time_roll = round(time.time() * 1000)
        self.need_to_roll = False
        self.need_to_update_rolls = True
        if self.turn == 'B':
            self.turn = 'W'
        else:
            self.turn = 'B'
        self.current_piece_selected = None

    def check(self, pos) -> None:
        '''
        This method handles the logic for every click that happened during the game. There are three different objects that can be 
        interacted with:
            The roll button
            The pieces
            The board itself
        '''
        if self.need_to_roll == True and self.button_roll.rect.collidepoint(pos):
            self.button_pressed()
        else:

            clicked_triangles = [tr for tr in self.board.get_triangles() if tr.point_inside_triangle(pos)]
            if len(clicked_triangles) > 0 and clicked_triangles[0].is_highlighted == True:
                self.move_piece(self.current_piece_selected, clicked_triangles[0])
                self.reset_highlighted()
                self.current_piece_selected = None


            clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]

            if len(clicked_sprites) > 0 and self.sprite_is_at_turn(clicked_sprites[0]) == True and self.satisfy_special_condition(clicked_sprites[0]) == True:
                if clicked_sprites[0].is_hovered == True and self.current_piece_selected == clicked_sprites[0]:
                    clicked_sprites[0].got_clicked()
                    self.current_piece_selected = None
                elif self.current_piece_selected == None:
                    clicked_sprites[0].got_clicked()
                if clicked_sprites[0].is_hovered == True:
                    self.current_piece_selected = clicked_sprites[0]
                    self.currently_highlighted.append(clicked_sprites[0])
                    self.show_possible_moves(clicked_sprites[0])
                else:
                    self.reset_highlighted()
                    if self.current_piece_selected != None:
                        self.current_piece_selected.got_clicked()
                    self.current_piece_selected = None

# Game Running
if __name__ == '__main__':
    app = Application(True)
    while True:
        app.update()


