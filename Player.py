import sys
import os
import math
import pygame
from pygame.locals import *
from Lasers import Laser
from HealthPickup import HealthPickup

class Player(pygame.sprite.Sprite): #do not need much of sprite now, but for big team assignment we will

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs #access to the gamespace
		self.player2_image = pygame.image.load("final_media/megaman_sprites_red.png")
		self.original_image = pygame.image.load("final_media/megaman_sprites.png") #create pygame image object
		self.blank_image = pygame.image.load("final_media/empty.png")
		self.image = self.original_image #keep original set
		self.rect = self.image.get_rect()
		self.rect.center = (75, 75)
		self.health = 4
		#(mx, my) = pygame.mouse.get_pos()
		self.start_rad = 0.8
		#self.rad = -math.atan2(my - self.rect.center[1], mx - self.rect.center[0])
		self.deg = 180 * self.start_rad / 3.14159 - 45
		self.rad = 3.14159 * self.deg / 180 #used to calculate for firing
		self.moving = False
		self.move_speed = 15
		self.playing_explosion = False
		self.original_laser = pygame.image.load("final_media/fish.png")
		# self.hits = 0
		self.alive = True
		#self.original_laser = pygame.image.load("media/laser.png")
		#pygame.mixer.music.load("media/screammachine.wav")
	def tick(self):
		'''
		if self.tofire == True:
			pygame.mixer.music.unpause()
			if not pygame.mixer.music.get_busy():
				self.playing_explosion = False
				pygame.mixer.music.load("media/screammachine.wav")
				pygame.mixer.music.play()
			self.fire()
			
		else:
			if not self.playing_explosion:
				pygame.mixer.music.pause()
		'''

		for laser in self.gs.enemy_laser_array:
			if self.rect.colliderect(laser.rect) and laser.collide == False: # player collision with laser
				laser.collide = True
				if self.gs.comm.status == "server":
					self.gs.hearts -= 1
					self.gs.comm.write("h")
				#self.health = self.health - 1
				self.gs.enemy_laser_array.remove(laser)

		for heart in self.gs.health_pickup_array:
			if self.rect.colliderect(heart.rect) and heart.collide == False: # player collision with heart
				#if self.gs.hearts < 5:  # check if at max health
				heart.collide = True
				self.gs.hearts += 1 # increment hearts and health
				#self.health += 1
				self.gs.health_pickup_array.remove(heart) # then, remove heart from array

		if self.gs.hearts <= 0:
			self.original_image = self.blank_image
			self.alive = False

		#(mx, my) = pygame.mouse.get_pos()
		#self.rad = -math.atan2(my - self.rect.center[1], mx - self.rect.center[0])
		#self.deg = 180 * self.rad / 3.14159 - 45
		self.rad = 3.14159 * self.deg / 180 #used to calculate for firing
		#code to calculate angle between my current direction and mouse position
		self.image = pygame.transform.rotate(self.original_image, self.deg) #use original so not continued degration
		self.save_center = self.rect.center
		self.rect = self.image.get_rect()
		self.rect.center = self.save_center

	def move(self, keycode):
		if self.alive:
			if keycode == K_SPACE:
				self.fire()
				self.gs.comm.write("f")
			elif keycode == K_UP:
				self.rect = self.rect.move(0,-self.move_speed) #use move command from deathstar function
				self.gs.comm.write("u")
			elif keycode == K_DOWN:
				self.rect = self.rect.move(0,self.move_speed) #use move command from deathstar function
				self.gs.comm.write("d")
			elif keycode == K_RIGHT:
				self.rect = self.rect.move(self.move_speed,0) #use move command from deathstar function 
				self.gs.comm.write("r")
			elif keycode == K_LEFT:
				self.rect = self.rect.move(-self.move_speed,0) #use move command from deathstar function
				self.gs.comm.write("l")
			elif keycode == K_a:
				self.gs.comm.write("q")
				self.deg = self.deg + 10
			elif keycode == K_d:
				self.gs.comm.write("e")
				self.deg = self.deg - 10

	def simple_move(self,code):
		if code == "f":
			self.fire()
		elif code == "u":
			self.rect = self.rect.move(0,-self.move_speed) #use move command from deathstar function
		elif code == "d":
			self.rect = self.rect.move(0,self.move_speed) #use move command from deathstar function
		elif code == "r":
			self.rect = self.rect.move(self.move_speed,0) #use move command from deathstar function 
		elif code == "l":
			self.rect = self.rect.move(-self.move_speed,0) #use move command from deathstar function
		elif code == "q":
			self.deg = self.deg + 10
		elif code == "e":
			self.deg = self.deg - 10	

	def fire(self):
		if self.alive:
			laser = Laser(self.gs,self)
			self.gs.laser_array.append(laser)
