import pygame
import random
import os.path

class Dice(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, seed) -> None:
        super().__init__()
        self.value = 0
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.split(current_directory)[0]
        path_ = parent_directory + f"/Assets/dice_face_1.png"
        self.image = pygame.image.load(path_)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.seed = seed
        
    def roll(self) -> None:
        random.seed(self.seed)
        random_value_rolled = random.SystemRandom().randint(1, 6)
        self.value = random_value_rolled
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.split(current_directory)[0]
        path_ = parent_directory + f"/Assets/dice_face_{random_value_rolled}.png"
        self.image = pygame.image.load(path_)