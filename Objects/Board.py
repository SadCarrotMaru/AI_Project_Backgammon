from .Piece import Piece
from .Board_triangle import Board_triangle
import copy
import pygame
import soft_config_const as const
class Board(): 
    def __init__(self, initial_board = const.PIECES_POSITION_INITIAL) -> None:
        self.frames = copy.deepcopy(initial_board)
        self.pieces=[]
        self.board_triangles = []
        self.initialize_board()
    
    def initialize_board(self) -> None:
        for i  in range(0,26):
            before = 0
            for element in self.frames[i]:
                x = 0 
                y = 0
                radius = const.RADIUS
                if i <= 12:
                    y = const.LOWEST_POINT - (radius * 2 * before) - radius
                    x = const.LOWEST_POINT - (i-1)*2*radius - radius
                else:
                    y = const.HIGHEST_POINT + (radius* 2* before) + radius
                    x = const.HIGHEST_POINT + (i-13)*2*radius + radius 

                if i > 18:
                    x+= (const.BOARD_SEP + radius)
                if i > 6 and i <= 12:
                    x-= 12
                    x-= radius
                self.pieces.append(Piece(element,radius,x,y,i))
                before+=1
            # triangle coordinates 
            before = 0
            x = 0 
            y = 0
            radius = const.RADIUS
            if i <= 12:
                y = const.LOWEST_POINT - (radius * 2 * before) - radius
                x = const.LOWEST_POINT - (i-1)*2*radius - radius
                if i > 6:
                    x-= const.BOARD_SEP
                    x-= radius
                x1 = x - radius
                x2 = x + radius
                y1 = y + radius
                y2 = y + radius
                x3 = x
                y3 = const.INF_TRIANGLE_END
            else:
                y = const.HIGHEST_POINT + (radius* 2* before) + radius
                x = const.HIGHEST_POINT + (i-13)*2*radius + radius 
                if i > 18:
                    x+= (const.BOARD_SEP + radius)
                x1 = x - radius
                x2 = x + radius
                y1 = y - radius
                y2 = y - radius
                x3 = x
                y3 = const.SUP_TRIANGLE_END
            
            if i%2 == 1:
                triangle_color = 'B'
            else:
                triangle_color = 'W'

            self.board_triangles.append(Board_triangle((x1,y1),(x2,y2),(x3,y3),triangle_color, i))

    def update_board(self) -> None:
        self.pieces = []
        for i  in range(1,25):
            before = 0
            for element in self.frames[i]:
                x = 0 
                y = 0
                radius = const.RADIUS
                if i <= 12:
                    y = const.LOWEST_POINT - (radius * 2 * before) - radius
                    x = const.LOWEST_POINT - (i-1)*2*radius - radius
                else:
                    y = const.HIGHEST_POINT + (radius* 2* before) + radius
                    x = const.HIGHEST_POINT + (i-13)*2*radius + radius 

                if i > 18:
                    x+= (const.BOARD_SEP + radius)
                if i > 6 and i <= 12:
                    x-= 12
                    x-= radius
                self.pieces.append(Piece(element,radius,x,y,i))
                before+=1
        if len(self.frames[0]) + len(self.frames[25]) > 0:
            x = const.CENTER_PIECES_X
            y = const.CENTER_PIECES_Y - const.RADIUS * (len(self.frames[0]) - 1)
            for element in self.frames[0]:
                 self.pieces.append(Piece(element, const.RADIUS, x, y, 0))
                 y+=const.RADIUS*2
            for element in self.frames[25]:
                self.pieces.append(Piece(element, const.RADIUS, x, y, 25))
                y+=const.RADIUS*2
    
    def move_piece(self, source, destination) -> None:
        piece_color = self.frames[source][0]
        if destination != 0 and destination != 25:
            if len(self.frames[destination]) == 1 and self.frames[destination][0] != self.frames[source][0]:
                if self.frames[destination][0] == 'W':
                    self.frames[25].append('W')
                else:
                    self.frames[0].append('B')
                
                self.frames[destination] = []
        self.frames[source]=self.frames[source][:-1]
        if destination > 0 and destination < 25: self.frames[destination].append(piece_color)
        self.update_board()


    def get_pieces(self) -> list:
        return self.pieces
    
    def get_triangles(self) -> list:
        return self.board_triangles