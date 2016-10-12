import sys
import os
import math
import pygame
from pygame.locals import *
from Player import Player
from Lasers import Laser
from Lasers import EnemyLaser
from Enemy import Enemy
from GameOver import GameOver
from Background import Background
from Healthbar import Healthbar
from HealthPickup import HealthPickup
from Cat import Sushi_Cat
from OctoKing import OctoKing
from Item import Item
from Client import ClientConnFactory
from Client import ClientConnection

class GameSpace(object):
	def __init__(self,reactor,comm,status):
		self.reactor = reactor
		self.comm = comm
		self.status = status #client or server
		self.client_conn_count = 0
		#self.gs = self
	def main(self):
		# 1)  #init
		pygame.init()
		pygame.key.set_repeat(25,25)
		self.slowmotion = 100
		# self.screen = screen
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.counter = 0
		#screen size
		self.screen = pygame.display.set_mode(self.size)
		#create game clock
		#self.clock = pygame.time.Clock()

		#2) set up game objects
		self.level = 1
		self.hearts = 5
		self.fire_count = 0
		self.health_pickup_array = []
		self.laser_array = []
		self.enemies_spawned = False
		self.enemy_array = []
		self.enemy_laser_array = []
		self.player = Player(self)
		self.background = Background(self)
		self.healthbar = Healthbar(self)
		self.gameover = GameOver(self)
		self.cat = Sushi_Cat(self)
		self.octoking = OctoKing(self)
		self.item = Item(self)

		# 3) start game loop
	def gameloop(self):
		self.counter += 1
		# 4) tick regulation
		#self.clock.tick(60) #stay here for 1/60th of a second, Framerate
		# 5) user input reading
		for event in pygame.event.get():   #writing event loop and processor
			if event.type == MOUSEBUTTONDOWN:
				#if self.comm.client_conn and self.level == 0:
				#self.start_level(self.level)
				pass
			if event.type == MOUSEBUTTONUP:
				self.update()
			if event.type == KEYDOWN: #on key down press, here is where we do all ticks so that time moves on movement
				self.player.move(event.key)
				self.update()
			if event.type == KEYUP:
				pass
			if event.type == QUIT: #catch the exit button
				self.reactor.stop()

		# 6) tick updating
		#self.player.tick()
		if (self.counter % self.slowmotion == 0): #slowmotion, update whole game only 2 every second
			self.update()
			self.counter = 1
		
		# 7) display
		if self.player.alive:
			self.display()
		else:
			self.display_game_over()

		pygame.display.flip() #swap the buffer with the display
	def update(self):
		if self.player.alive:
			if (len(self.enemy_array) == 0) & (self.enemies_spawned == True):
				self.enemies_spawned = False
				self.item.visable = True
				#also need to show item
				#self.background.image = pygame.image.load("final_media/forrest.png")
				# self.display_background()

			self.player.tick()
			self.cat.tick()
			self.octoking.tick()
			self.item.tick()
			if self.comm.client_conn == True:
				self.player2.tick()
			self.healthbar.tick()
			for enemy in self.enemy_array:
				enemy.tick()
			for laser in self.laser_array:
				laser.tick()
			for laser in self.enemy_laser_array:
				laser.tick()
		if self.status == 1 and self.comm.client_conn == False and self.client_conn_count <= 400:
			self.client_conn_count = 0
			self.reactor.connectTCP(self.comm.SERVER_HOST, self.comm.SERVER_PORT, ClientConnFactory(self.comm,self))
		elif self.status == 1 and self.comm.client_conn == False:
			self.client_conn_count += 1
	def display(self):				
		#self.screen.fill(self.black)    #fills the buffer screen
		self.display_background()
		self.display_healthbar()
		for enemy in self.enemy_array:
			self.screen.blit(enemy.image,enemy.rect)
		for laser in self.laser_array:
			self.screen.blit(laser.image,laser.rect)
		for laser in self.enemy_laser_array:
			self.screen.blit(laser.image,laser.rect)
		for heart in self.health_pickup_array:
			self.screen.blit(heart.image,heart.rect)
		if self.comm.client_conn:
			self.screen.blit(self.player2.image, self.player2.rect)
		self.screen.blit(self.player.image, self.player.rect) #push object
		if self.cat.visable == True:
			self.screen.blit(self.cat.image, self.cat.rect)
		if self.octoking.visable == True:
			self.screen.blit(self.octoking.image, self.octoking.rect)
		if self.item.visable == True:
			self.screen.blit(self.item.image, self.item.rect)

	def display_background(self):
		self.screen.fill(self.black)
		self.screen.blit(self.background.image,self.background.rect)

	def display_healthbar(self):
		self.screen.blit(self.healthbar.image,self.healthbar.rect)

	def display_game_over(self):
		self.screen.fill(self.black)
		self.screen.blit(self.gameover.image,self.gameover.rect)

	def win_screen(self):
		self.background.image = pygame.image.load("final_media/win.png")

	def start_level(self,level):
		if level == 1:
			self.start_level_1()
		elif level == 2:
			self.start_level_2()
		elif level == 3:
			self.start_level_3()
		elif level == 4:
			self.win_screen()
			self.health_pickup_array = []
			self.octoking.visable = True
		else:
			pass
		self.level += 1
		if self.comm.status == "server":
			for enemy in self.enemy_array:
				if enemy.id % 2 == 0: #every even enemy
					enemy.player = self.player2
		elif self.comm.status == "client":
			for enemy in self.enemy_array:
				if enemy.id % 2 == 1: #every even enemy
					enemy.player = self.player2

	def start_level_1(self):
		self.enemies_spawned = False
		Enemy(self,"fish",(550,400),1)
		Enemy(self,"squid",(550,200),2)

	def start_level_2(self):
		self.background.image = pygame.image.load("final_media/forrest.png")
		self.enemies_spawned = False
		Enemy(self,"fish",(550,400),1)
		Enemy(self,"fish",(550,200),2)
		Enemy(self,"squid",(450,350),3)

	def start_level_3(self):
		self.enemies_spawned = False
		self.background.image = pygame.image.load("final_media/hallway.png")
		Enemy(self,"king",(550,100),1)


	def create_player(self):
		self.player2 = Player(self)
		if self.comm.status == "client":
			self.player.image = self.player.player2_image
			self.player.original_image = self.player.player2_image
			self.player.rect.center = (75,150)
		elif self.comm.status == "server":
			self.player2.image = self.player.player2_image
			self.player2.original_image = self.player.player2_image
			self.player2.rect.center = (75,150)
			self.player.rect.center = (75,75)
		#append to player array
