import pygame
import soft_config_const as const

class Piece(pygame.sprite.Sprite):
    '''
    Anything related to the interface for the pieces.
    '''
    def __init__(self, color, radius, pos_x, pos_y, current_pos_on_board) -> None:
        super().__init__()
        if color == 'W':
            self.color = const.WHITE
            self.other_color = const.CYAN 
        else:
            self.color = const.BLACK
            self.other_color = const.DARK_BLUE
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.radius = radius
        self.current_position_on_board = current_pos_on_board
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.is_hovered = False

    def got_clicked(self):

        if self.is_hovered == True:
            pygame.draw.circle(self.image,self.color,(self.radius, self.radius), self.radius)
            self.is_hovered = False
        else:
            pygame.draw.circle(self.image,self.other_color,(self.radius, self.radius), self.radius)
            self.is_hovered = True