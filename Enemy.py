import sys
import os
import math
import pygame
from pygame.locals import *
from Lasers import EnemyLaser
from Lasers import OctoLaser
from HealthPickup import HealthPickup
import cPickle as pickle

class Enemy(pygame.sprite.Sprite):

	def __init__(self, gs, type_enemy, center, id_enemy):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.gs.enemies_spawned = True
		self.player = self.gs.player
		self.id = id_enemy
		if type_enemy == "fish":
			self.type = "fish"
			self.original_image = pygame.image.load("final_media/fish.png")
			self.blank_image = pygame.image.load("final_media/empty.png")
			self.health = 20
			# self.image = self.original_image #save original
			# self.rect = self.image.get_rect()
			# #self.rect.center = (550,400)
			# self.rect.center = center
			# self.rad = -math.atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])
			# self.deg = 180 * self.rad / 3.14159 + 180
			# self.image = pygame.transform.rotate(self.original_image, self.deg) #get rotate from original image 
			# self.rect = self.image.get_rect()
			# self.rect.center = center
			# self.center_save = self.rect.center
			# self.n = 0.0
			
			# self.fire_count = 0
			# self.exploded = False
			# self.alive = True
			# self.c = 0
			# ###
			# self.dx = 0
			# self.dy = 0
			# ###
		elif type_enemy == "squid":
			self.type = "squid"
			self.original_image = pygame.image.load("final_media/squid.png")
			self.blank_image = pygame.image.load("final_media/empty.png")
			self.health = 10
			# self.image = self.original_image #save original
			# self.rect = self.image.get_rect()
			# #self.rect.center = (550,400)
			# self.rect.center = center
			# self.rad = -math.atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])
			# self.deg = 180 * self.rad / 3.14159 + 180
			# self.image = pygame.transform.rotate(self.original_image, self.deg) #get rotate from original image 
			# self.rect = self.image.get_rect()
			# self.rect.center = center
			# self.center_save = self.rect.center
			# self.n = 0.0
			# self.health = 10
			# self.exploded = False
			# self.alive = True
			# self.c = 0
			# self.fire_count = 0
			# ###
			# self.dx = 0
			# self.dy = 0
			# ###
		elif type_enemy == "king":
			self.type = "king"
			self.original_image = pygame.image.load("final_media/octo_king.png")
			self.blank_image = pygame.image.load("final_media/empty.png")
			self.health = 150
		self.deg2 = 0
		self.rad2 = 0
		self.image = self.original_image #save original
		self.rect = self.image.get_rect()
		#self.rect.center = (550,400)
		self.rect.center = center
		self.rad = -math.atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])
		self.deg = 180 * self.rad / 3.14159 + 180

		self.image = pygame.transform.rotate(self.original_image, self.deg) #get rotate from original image 
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.center_save = self.rect.center
		self.n = 0.0
		
		self.fire_count = 0
		self.exploded = False
		self.alive = True
		self.c = 0
		###
		self.dx = 0
		self.dy = 0
		###
		self.gs.enemy_array.append(self)

	def tick(self):
		#make fish follow person
		if self.gs.comm.status == "client" and self.type == "king":
			self.player = self.gs.player
		self.rad = -math.atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])
		self.deg = 180 * self.rad / 3.14159 + 180
		if self.gs.comm.client_conn:
			self.rad2 = -math.atan2(self.gs.player2.rect.center[1] - self.rect.center[1], self.gs.player2.rect.center[0] - self.rect.center[0])
			self.deg2 = 180 * self.rad2 / 3.14159 + 180
		if self.type == "fish" or self.type == "squid":
			#self.rect = self.image.get_rect()	
			#self.center_save = self.rect.center #save old center
			self.image = pygame.transform.rotate(self.original_image, self.deg) #get rotate from original image
			self.rect = self.image.get_rect() #replace old center
			self.rect.center = self.center_save
			self.n = self.n - .2
		if self.gs.comm.status == "server": #make is so only the server ones fire.
			if self.type == "fish":
				self.fire_count += 1
			elif self.type == "squid":
				self.fire_count += 2
			elif self.type == "king":
				self.fire_count += 1.2

		#self.move() # move enemies toward player

		if (self.fire_count >= 40):
			#print "fire", self.id
			self.fire()
			self.fire_count = 0

		for laser in self.gs.laser_array:
			if self.rect.colliderect(laser.rect) and laser.collide == False:
				laser.collide = True
				self.health = self.health - 1
				self.gs.laser_array.remove(laser)
				# print self.health
		if self.health < 0:
			self.c += 1
			self.alive = False
			# self.gs.enemy.original_image = self.gs.enemy.blank_image
			# self.rect = self.gs.enemy.original_image.get_rect()
			# self.gs.screen.blit(self.image,self.rect)
			self.gs.health_pickup_array.append(HealthPickup(self.gs,self.rect.center)) # drop a health pickup
			self.gs.enemy_array.remove(self)

	def fire(self):
		if self.type == "king":
			self.gs.comm.write(str(self.id))
			laser = OctoLaser(self.gs,self,self.rad2)
			laser1 = OctoLaser(self.gs,self,self.rad)
			self.gs.enemy_laser_array.append(laser)
			self.gs.enemy_laser_array.append(laser1)

		else:
			self.gs.comm.write(str(self.id))
			laser = EnemyLaser(self.gs,self)
			self.gs.enemy_laser_array.append(laser)
		
	
	def simple_fire(self): #simple fire does not write so that the updates can be made silently
		if self.type == "king":
			laser = OctoLaser(self.gs,self,self.rad2)
			laser1 = OctoLaser(self.gs,self,self.rad)
			self.gs.enemy_laser_array.append(laser)
			self.gs.enemy_laser_array.append(laser1)

		else:
			laser = EnemyLaser(self.gs,self)
			self.gs.enemy_laser_array.append(laser)
		#pd = pickle.dumps(self.gs.enemy_laser_array)
		#self.gs.comm.write(pd)
		#pd = pickle.dumps(self.gs.enemy_laser_array)
		#sd = zlib.compress(pd)
		#self.gs.comm.write(sd)		
	"""
	def move(self):
		#####################################################
		self.dx = 15 * math.cos(self.gs.player.rad)
		self.dy = -15 * math.sin(self.gs.player.rad)
		self.center_save[0] += self.dx/10
		self.center_save[1] += self.dy/10
		#####################################################
	"""