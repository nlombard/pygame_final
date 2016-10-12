import sys
import os
import math
import pygame
from pygame.locals import *
from Lasers import EnemyLaser
from HealthPickup import HealthPickup
import cPickle as pickle
import random

class Item(pygame.sprite.Sprite):

	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.player = self.gs.player
		self.image = pygame.image.load("final_media/cute_sushi.png")
		self.blank_image = pygame.image.load("final_media/empty.png")
		self.original_image = self.image
		self.image = self.original_image #save original
		self.rect = self.image.get_rect()
		self.rect.center = (75,75)
		self.visable = False
	def tick(self):
		if self.visable:
			if self.gs.comm.client_conn:
				if self.rect.colliderect(self.gs.player.rect) and self.rect.colliderect(self.gs.player2.rect): #when either player runs, start next level
					self.gs.start_level(self.gs.level)
					self.visable = False