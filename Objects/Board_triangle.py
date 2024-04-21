import pygame
import soft_config_const as const

class Board_triangle():
    def __init__(self, point_x, point_y, point_z, color, pos_on_board) -> None:
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
        pygame.draw.polygon(screen, self.current_color, (self.point_x, self.point_y, self.point_z))
        
    def switch_highlight(self) -> None:
        if self.current_color == self.color:
            self.current_color = self.other_color
            self.is_highlighted = True
        else:
            self.current_color = self.color
            self.is_highlighted = False

    def sign(point_1, point_2, point_3) -> float:
        return float(point_1[0] - point_3[0]) * (point_2[1] - point_3[1]) - (point_2[0] - point_3[0]) * (point_1[1] - point_3[1]) # return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);

    def point_inside_triangle(self, point) -> bool:
        d1 = Board_triangle.sign(point,self.point_x, self.point_y)
        d2 = Board_triangle.sign(point,self.point_y, self.point_z)
        d3 = Board_triangle.sign(point,self.point_z, self.point_x)

        has_neg = d1 < 0 or d2 < 0 or d3 < 0
        has_pos = d1 > 0 or d2 >  0 or d3 > 0

        return not (has_neg and has_pos)