import sys
import os
import math
import pygame
from pygame.locals import *
from Lasers import EnemyLaser
from HealthPickup import HealthPickup
import cPickle as pickle
import random

class OctoKing(pygame.sprite.Sprite):

	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.player = self.gs.player
		self.octo_image = pygame.image.load("final_media/octo_king.png")
		self.blank_image = pygame.image.load("final_media/empty.png")
		self.original_image = self.octo_image
		self.image = self.original_image #save original
		self.rect = self.image.get_rect()
		self.rect.center = (random.randrange(100,600),random.randrange(100,400))
		self.visable = False
	def tick(self):
		if self.visable:
			if self.rect.colliderect(self.gs.player.rect): #when one player runs, start next level
				self.rect.center = (random.randrange(100,600),random.randrange(100,400))