import sys
import os
import math
import pygame
from pygame.locals import *

class Laser(pygame.sprite.Sprite):
	def __init__(self, gs, player):
		pygame.sprite.Sprite.__init__(self)
		self.player = player

		self.gs = gs
		self.original_image = pygame.image.load("final_media/laser.png")
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = self.player.rect.center #set to center of player
		self.dx = 14 * math.cos(self.player.rad)
		self.dy = -14 * math.sin(self.player.rad)
		self.life = 0.0
		self.collide = False
		self.life_max = 2 #set max life in seconds right now

	def tick(self):
		self.life = self.life + 1.0/60.0
		self.rect = self.rect.move(self.dx,self.dy)
		if self.life > self.life_max:
			self.gs.laser_array.remove(self) #remove laser after its life is over

class EnemyLaser(pygame.sprite.Sprite):
	def __init__(self, gs=None,enemy=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.enemy = enemy
		self.original_image = pygame.image.load("final_media/enemy_laser.png")
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = self.enemy.rect.center #set to center of enemy
		self.dx = 14 * math.cos(self.enemy.rad)
		self.dy = -14 * math.sin(self.enemy.rad)
		self.life = 0.0
		self.collide = False
		self.life_max = 2 #set max life in seconds right now

	def tick(self):
		self.life = self.life + 1.0/60.0
		self.rect = self.rect.move(self.dx,self.dy)
		if self.life > self.life_max:
			self.gs.enemy_laser_array.remove(self) #remove laser after its life is over

class OctoLaser(pygame.sprite.Sprite):
	def __init__(self, gs,enemy,rad):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.rad = rad
		self.enemy = enemy
		self.original_image = pygame.image.load("final_media/enemy_laser.png")
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = self.enemy.rect.center #set to center of enemy
		self.dx = 14 * math.cos(self.rad)
		self.dy = -14 * math.sin(self.rad)
		self.life = 0.0
		self.collide = False
		self.life_max = 2 #set max life in seconds right now

	def tick(self):
		self.life = self.life + 1.0/60.0
		self.rect = self.rect.move(self.dx,self.dy)
		if self.life > self.life_max:
			self.gs.enemy_laser_array.remove(self) #remove laser after its life is over
