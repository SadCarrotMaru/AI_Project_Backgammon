import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, text, color) -> None:
        pygame.init()
        super().__init__()
        self.value = 0
        self.color = color
        self.width = 100
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.image.blit(self.text,(8,13))
