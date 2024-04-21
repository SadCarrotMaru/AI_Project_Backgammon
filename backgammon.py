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


    def AI_update(self):
        if self.turn == 'B' and self.need_to_roll == True: ## Reversed, B if it's White's turn and vice versa
            self.button_pressed()
        if self.turn == 'W' and self.need_to_update_rolls == False and self.need_to_roll == False:
            return self.board.frames, self.rolls
        return None, None


    def switch_game_status(self, board_frames, turn, rolls):
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
        possibilites = []
        if len(self.board.frames[position]) > 0 and self.board.frames[position][0] == self.turn:
            piece = Piece(self.turn, 0, 0, 0, position)
            if self.satisfy_special_condition(piece):
                possibilites = self.get_possible_moves(piece)
        return possibilites


    def update_board(self) -> None:
        board_triangles = self.board.get_triangles()
        for triangle in board_triangles:
            triangle.display(self.screen)


    def not_in_blocked_state(self) -> bool:     
        for sprite in self.all_sprites:
            if (self.turn == 'B' and sprite.color == const.BLACK) or (self.turn == 'W' and sprite.color == const.WHITE):
                possibilites = len(self.get_possible_moves(sprite))
                if possibilites != 0 and self.satisfy_special_condition(sprite) == True:
                    return True
        return False

    def update_dice(self) -> None:

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
    

    def able_to_retrieve_pieces(self, color):
        for sprite in self.all_sprites:
            if (color == 'B' and sprite.color == const.BLACK):
                if sprite.current_position_on_board <= 18:
                    return False           
            elif (color == 'W' and sprite.color == const.WHITE):     
                if sprite.current_position_on_board >= 7:
                    return False
        return True

    def update_pieces(self) -> None:
        self.all_sprites = pygame.sprite.Group()
        for piece in self.board.get_pieces():
            self.all_sprites.add(piece)
        
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

    def update(self) -> None:
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
        need_to_highlight = self.get_candidates_triangles_showlight(piece, list_candidates)
        triangles = self.board.get_triangles()
        for pos in need_to_highlight:
            self.currently_highlighted.append(triangles[pos])
            triangles[pos].switch_highlight()


    def show_possible_moves(self, piece) -> None:
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

    def check_win_status(self):
        no_white_pieces = len([x for x in self.all_sprites if x.color == const.WHITE])
        no_black_pieces = len(self.all_sprites) - no_white_pieces
        
        if no_white_pieces == 0:
            self.WIN_TRIGGERED = True
            self.WINNER = 'WHITE'
        elif no_black_pieces == 0:
            self.WIN_TRIGGERED = True
            self.WINNER = 'BLACK'

    def move_piece(self, piece, triangle) -> None:
        roll_used = triangle.position_on_board - piece.current_position_on_board
        if roll_used < 0 : roll_used *= -1
        if roll_used in self.rolls: 
            self.rolls.remove(roll_used)
        else:
            self.rolls.remove(max(self.rolls))
        self.board.move_piece(piece.current_position_on_board, triangle.position_on_board)

    def reset_highlighted(self) -> None:
        for element in self.currently_highlighted:
            if isinstance(element, Board_triangle):
                element.switch_highlight()
        self.currently_highlighted = []
        #self.current_piece_selected = None

    def sprite_is_at_turn(self, sprite):
        type_ = 'W'
        if sprite.color == const.BLACK:
            type_ = 'B'
        if self.turn == type_:
            return True
        return False
    

    def satisfy_special_condition(self, sprite):
        if sprite.color == const.BLACK and len(self.board.frames[0]) > 0 and sprite.current_position_on_board != 0:
            return False
        if sprite.color == const.WHITE and len(self.board.frames[25]) > 0 and sprite.current_position_on_board != 25:
            return False
        return True
    
    def button_pressed(self) -> None:
        self.start_time_roll = round(time.time() * 1000)
        self.need_to_roll = False
        self.need_to_update_rolls = True
        if self.turn == 'B':
            self.turn = 'W'
        else:
            self.turn = 'B'
        self.current_piece_selected = None

    def check(self, pos) -> None:
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

if __name__ == '__main__':
    app = Application(True)
    while True:
        app.update()


