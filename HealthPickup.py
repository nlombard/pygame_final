import pygame
from pygame.locals import *

class HealthPickup(pygame.sprite.Sprite):

	def __init__(self,gs,center):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		self.image = pygame.image.load("final_media/1_heart.png")
		self.rect = self.image.get_rect()
		self.collide = False
		self.rect.center = center