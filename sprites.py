#Sprite classes for Platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.walking = False
		self.jumping = False
		self.current_frame = 0
		self.last_update = 0
		self.load_images()
		self.image = self.standing
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)
		self.pos = vec(WIDTH/2, HEIGHT/2)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

	def load_images(self):
		self.standing = self.game.spritesheet.get_image(0, 840, 135, 165)
		self.standing.set_colorkey(BLACK)
		self.walking_l = [self.game.spritesheet.get_image(670, 498, 123, 166),
							self.game.spritesheet.get_image(671, 1655, 122, 166),
							self.game.spritesheet.get_image(671, 1823, 122, 166)
							]
		for frame in self.walking_l:
			frame.set_colorkey(BLACK)
		self.walking_r = [self.game.spritesheet.get_image(672, 834, 122, 166),
							self.game.spritesheet.get_image(672, 666, 122, 166),
							self.game.spritesheet.get_image(671, 1487, 123, 166)
							]
		for frame in self.walking_r:
			frame.set_colorkey(BLACK)
		self.jumping_up = self.game.spritesheet.get_image(0, 337, 135, 167)
		self.jumping_up.set_colorkey(BLACK)

	def jump(self):
		self.rect.y += 1
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y -= 1
		if hits:
			self.game.jump_sound.play()
			self.vel.y -= 10

	def update(self):
		self.animate()
		self.acc = vec(0, PLAYER_GRAVITY)
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_RIGHT]:
			self.acc.x = PLAYER_ACC

		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		if abs(self.vel.x) < 0.1:
			self.vel.x = 0
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		self.rect.midbottom = self.pos

	def animate(self):
		now = pg.time.get_ticks()
		if self.vel.x != 0:
			self.walking = True
		else:
			self.walking = False

		if self.vel.y !=0:
			self.jumping = True
		else:
			self.jumping = False

		if not self.jumping and not self.walking:
			if now - self.last_update > 100:
				self.last_update = now
				self.image = self.standing

		if self.walking:
			if now - self.last_update > 100:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walking_l)
				bottom = self.rect.bottom
				if self.vel.x > 0:
					self.image = self.walking_r[self.current_frame]
				else:
					self.image = self.walking_l[self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
	def __init__(self, x, y, w, h):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((w,h))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Gold(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((WIDTH/100, HEIGHT/50))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Spritesheet:
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert()

	def get_image(self, x, y, width, height):
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0,0), (x, y, width, height))
		image = pg.transform.scale (image, (width // 3, height // 3))
		return image
