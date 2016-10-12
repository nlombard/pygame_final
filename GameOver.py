import pygame
from pygame.locals import *

class GameOver(pygame.sprite.Sprite):

	def __init__(self,gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		self.image = pygame.image.load("final_media/gameover.png")
		self.rect = self.image.get_rect()