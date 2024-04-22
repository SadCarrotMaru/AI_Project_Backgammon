import pygame
import soft_config_const as const

class Board_triangle():
    def __init__(self, point_x, point_y, point_z, color, pos_on_board) -> None:
        '''
        This class contains every information related to a triangle on board. It handles the generation and the updates.
        '''
        if color == 'B':
            self.color = const.TRIANGLE_TYPE_BLACK
            self.other_color = const.RED 
        else:
            self.color = const.TRIANGLE_TYPE_WHITE
            self.other_color = const.RED

        if pos_on_board == 0 or pos_on_board == 25:
            self.color = const.BOARD_BROWN

        self.point_x = point_x
        self.point_y = point_y
        self.point_z = point_z

        self.position_on_board = pos_on_board

        self.current_color = self.color
        self.is_highlighted = False

    def display(self, screen) -> None:
        '''
        Displays the triangle on the screen.
        '''
        pygame.draw.polygon(screen, self.current_color, (self.point_x, self.point_y, self.point_z))
        
    def switch_highlight(self) -> None:
        '''
        Changes the color of the triangle.
        '''
        if self.current_color == self.color:
            self.current_color = self.other_color
            self.is_highlighted = True
        else:
            self.current_color = self.color
            self.is_highlighted = False

    def sign(point_1, point_2, point_3) -> float:
        '''
        CCW, utlity method for the method downstairs.
        '''
        return float(point_1[0] - point_3[0]) * (point_2[1] - point_3[1]) - (point_2[0] - point_3[0]) * (point_1[1] - point_3[1]) # return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);

    def point_inside_triangle(self, point) -> bool:
        '''
        Being given a point (coordinates of the mouse when a click occurs), it checks if the click was inside the triangle.
        '''
        d1 = Board_triangle.sign(point,self.point_x, self.point_y)
        d2 = Board_triangle.sign(point,self.point_y, self.point_z)
        d3 = Board_triangle.sign(point,self.point_z, self.point_x)

        has_neg = d1 < 0 or d2 < 0 or d3 < 0
        has_pos = d1 > 0 or d2 >  0 or d3 > 0

        return not (has_neg and has_pos)