import pygame
from pygame.locals import *

class Background(pygame.sprite.Sprite):

	def __init__(self,gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		self.image = pygame.image.load("final_media/dungeon.png")
		self.rect = self.image.get_rect()