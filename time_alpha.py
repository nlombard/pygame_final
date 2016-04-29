import sys
import os
import math
import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite): #do not need much of sprite now, but for big team assignment we will

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs #access to the gamespace
		self.original_image = pygame.image.load("final_media/megaman_sprites.png") #create pygame image object
		self.image = self.original_image #keep original set
		self.rect = self.image.get_rect()
		self.rect.center = (75, 75)
		self.tofire = False
		(mx, my) = pygame.mouse.get_pos()
		self.rad = 0.8
		#self.rad = -math.atan2(my - self.rect.center[1], mx - self.rect.center[0])
		self.deg = 180 * self.rad / 3.14159 - 45
		self.moving = False
		self.move_speed = 10
		self.playing_explosion = False
		self.original_laser = pygame.image.load("final_media/fish.png")
		#self.original_laser = pygame.image.load("media/laser.png")
		pygame.mixer.music.load("media/screammachine.wav")
	def tick(self):
		#for laser in self.gs.laser_array:
		#		laser.rect = laser.rect.move(laser.dx,laser.dy)
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
			(mx, my) = pygame.mouse.get_pos()
			#self.rad = -math.atan2(my - self.rect.center[1], mx - self.rect.center[0])
			#self.deg = 180 * self.rad / 3.14159 - 45
			self.rad = 3.14159 * self.deg / 180
			#code to calculate angle between my current direction and mouse position
			self.image = pygame.transform.rotate(self.original_image, self.deg) #use original so not continued degration
			self.save_center = self.rect.center
			self.rect = self.image.get_rect()
			self.rect.center = self.save_center

	def move(self, keycode):
		if keycode == K_SPACE:
			#self.tofire = True
			self.fire()
		if keycode == K_UP:
			self.rect = self.rect.move(0,-self.move_speed) #use move command from deathstar function
		elif keycode == K_DOWN:
			self.rect = self.rect.move(0,self.move_speed) #use move command from deathstar function
		elif keycode == K_RIGHT:
			self.rect = self.rect.move(self.move_speed,0) #use move command from deathstar function 
		elif keycode == K_LEFT:
			self.rect = self.rect.move(-self.move_speed,0) #use move command from deathstar function
		elif keycode == K_a:
			self.deg = self.deg + 10
		elif keycode == K_d:
			self.deg = self.deg - 10
	def fire(self):
		laser = Laser(self.gs)
		self.gs.laser_array.append(laser)


class Laser(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.original_image = pygame.image.load("media/laser.png")
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = self.gs.player.rect.center #set to center of deathstar
		self.dx = 15 * math.cos(self.gs.player.rad)
		self.dy = -15 * math.sin(self.gs.player.rad)
		self.life = 0.0
		self.collide = False
		self.life_max = 2 #set max life in seconds right now

	def tick(self):
		self.life = self.life + 1.0/60.0
		self.rect = self.rect.move(self.dx,self.dy)
		if self.life > self.life_max:
			self.gs.laser_array.remove(self) #remove laser after its life is over

class Fish(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.original_image = pygame.image.load("final_media/fish.png")
		self.red_image = pygame.image.load("media/globe_red100.png")
		self.blank_image = pygame.image.load("media/empty.png")
		self.image = self.original_image #save original
		self.rect = self.image.get_rect() 
		self.rect.center = (580,430)
		self.n = 0.0
		self.health = 200
		self.low_health = 100
		self.exploded = False

	def tick(self):
		#self.image = pygame.transform.rotate(self.original_image, self.n) #get rotate from original image
		self.rect = self.image.get_rect()
		self.rect.center = (580,430)
		self.n = self.n - .2
		for laser in self.gs.laser_array:
			if self.rect.colliderect(laser.rect) and laser.collide == False:
				laser.collide = True
				self.health = self.health - 1
				print self.health
		if self.health < self.low_health and not self.exploded:
			self.gs.earth.original_image = self.gs.earth.red_image
		if self.health < 0 and not self.exploded:
			self.exploded = True
			pygame.mixer.music.stop()
			pygame.mixer.music.load("media/explode.wav")
			pygame.mixer.music.play()
			#self.gs.deathstar.playing_explosion = True
			#self.gs.earth.original_image = self.gs.earth.blank_image
			#delete object and remove hitpoints


class GameSpace(object):
	def main(self):
		# 1)  #init
		pygame.init()
		pygame.key.set_repeat(25,25)
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.counter = 0
		#screen size
		screen = pygame.display.set_mode(self.size)
		#create game clock
		self.clock = pygame.time.Clock()

		#2) set up game objects
		self.player = Player(self)
		self.earth = Fish(self)
		self.laser_array = []

		# 3) start game loop
		while 1:
			self.counter = self.counter + 1
			# 4) tick regulation
			self.clock.tick(60) #stay here for 1/60th of a second, Framerate

			# 5) user input reading
			for event in pygame.event.get():   #writing event loop and processor
				if event.type == MOUSEBUTTONDOWN:
					#self.object.tofire = True
					self.player.fire()
					self.update()
				if event.type == MOUSEBUTTONUP:
					self.player.tofire = False
					self.update()
				if event.type == KEYDOWN: #on key down press, here is where we do all ticks so that time moves on movement
					self.player.move(event.key)
					self.update()
				if event.type == KEYUP:
					self.player.tofire = False
				if event.type == QUIT: #catch the exit button
					sys.exit()

			# 6) tick updating
			self.player.tick()
			if (self.counter % 40 == 0): #slowmotion, update whole game only 2 every second
				self.update()
				self.counter == 1

			# 7) display
			screen.fill(self.black)    #fills the buffer screen
			for laser in self.laser_array:
				screen.blit(laser.image,laser.rect)
			screen.blit(self.player.image, self.player.rect) #push object
			screen.blit(self.earth.image, self.earth.rect)
			pygame.display.flip() #swap the buffer with the display
	def update(self):
		self.player.tick()
		self.earth.tick()
		for laser in self.laser_array:
				laser.tick()
						
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()