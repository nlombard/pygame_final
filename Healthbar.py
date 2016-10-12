import pygame
from pygame.locals import *

class Healthbar(pygame.sprite.Sprite):

	def __init__(self,gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		self.five_hearts = pygame.image.load("final_media/5_hearts.png")
		self.four_hearts = pygame.image.load("final_media/4_hearts.png")
		self.three_hearts = pygame.image.load("final_media/3_hearts.png")
		self.two_hearts = pygame.image.load("final_media/2_hearts.png")
		self.one_heart = pygame.image.load("final_media/1_heart.png")
		self.blank_image = pygame.image.load("final_media/empty.png")
		self.image = self.five_hearts
		self.rect = self.image.get_rect()
		self.rect.center = (90,20)

	def tick(self):
		if self.gs.hearts == 5:
			self.image = self.five_hearts
		elif self.gs.hearts == 4:
			self.image = self.four_hearts
		elif self.gs.hearts == 3:
			self.image = self.three_hearts
		elif self.gs.hearts == 2:
			self.image = self.two_hearts
		elif self.gs.hearts == 1:
			self.image = self.one_heart
		elif self.gs.hearts == 0:
			self.image = self.blank_image
		else:
			self.image = self.five_hearts