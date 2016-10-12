import sys
import os
import math
import pygame
from pygame.locals import *
from Lasers import EnemyLaser
from HealthPickup import HealthPickup
import cPickle as pickle
import random

class Sushi_Cat(pygame.sprite.Sprite):

	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.player = self.gs.player
		self.cat_image = pygame.image.load("final_media/cat_saying_1.png")
		self.blank_image = pygame.image.load("final_media/empty.png")
		self.original_image = self.cat_image
		self.image = self.original_image #save original
		self.rect = self.image.get_rect()
		self.rect.center = (random.randrange(100,600),random.randrange(100,400))
		self.visable = True
	def tick(self):
		if self.visable:
			if self.gs.comm.client_conn:
				self.rect.center = (100,400) #when connected send to bottom left
				if self.rect.colliderect(self.gs.player.rect) or self.rect.colliderect(self.gs.player2.rect): #when either player runs, start next level
					self.gs.start_level(self.gs.level)
					self.visable = False
			elif self.rect.colliderect(self.gs.player.rect): #case for just the client or server without the other
				self.rect.center = (random.randrange(100,600),random.randrange(100,400))