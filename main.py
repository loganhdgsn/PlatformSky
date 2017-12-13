# Platform Sky

#Art from Kenney.nl
#Jump sound created through Bfxr
#Yippee by Snabisch
#Sky Game Menu by Eric Matyas
#Death is just Another Path by Otto Halmen

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
	def __init__(self):
		self.running = True
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.font_name = pg.font.match_font(FONT_NAME)
		self.load_data()

	def load_data(self):
		#High Score
		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')
		self.snd_dir = path.join(self.dir, 'snd')

		#self.coin = pg.image.load(path.join(img_dir, '8-bit-Coin.jpg'))
		with open(path.join(self.dir, HS_FILE), 'w') as f:
			try:
				self.highscore = int(f.read())
			except:
				self.highscore = 0

		self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
		self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump2.wav'))
		self.coin_sound = pg.mixer.Sound(path.join(self.snd_dir, 'coin5.wav'))
		#self.walk_sound = pg.mixer.Sound(path.join(self.snd_dir, ''))
		#self.music = pg.mixer.Sound(path,join(self.snd_dir, 'Sky Game Menu.mp3'))

	def new(self):
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.gold = pg.sprite.Group()
		self.score = 0
		self.player = Player(self)
		self.all_sprites.add(self.player)
		for plat in PLATFORM_LIST:
			p = Platform(*plat)
			self.all_sprites.add(p)
			self.platforms.add(p)
		for gp in GOLD_LIST:
			g = Gold(*gp)
			self.all_sprites.add(g)
			self.gold.add(g)
		pg.mixer.music.load(path.join(self.snd_dir, 'Sky_Game_Menu.ogg'))
		self.run()

	def run(self):
		# Game loop
		pg.mixer.music.play(loops=-1)
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
		pg.mixer.music.fadeout(500)

	def update(self):
		# Game loop - update
		self.all_sprites.update()

		#platform collision
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
				self.player.pos.y = hits[0].rect.top + 1
				self.player.vel.y = 0

		#gold collision
		grab = pg.sprite.spritecollide(self.player, self.gold, True)
		if grab:
			self.coin_sound.play()
			self.score += 10
		#scrolling screen
		if self.player.rect.left >= WIDTH * (3/4):
			self.player.pos.x -= abs(self.player.vel.x)
			for plat in self.platforms:
				plat.rect.x -= abs(self.player.vel.x)
			for gp in self.gold:
				gp.rect.x -= abs(self.player.vel.x)
		if self.player.rect.left <= WIDTH / 4:
			self.player.pos.x += abs(self.player.vel.x)
			for plat in self.platforms:
				plat.rect.x += abs(self.player.vel.x)
			for gp in self.gold:
				gp.rect.x += abs(self.player.vel.x)

		#die
		if self.player.rect.top > HEIGHT:
			for sprite in self.all_sprites:
				sprite.rect.y -= max(self.player.vel.y, 10)
				if sprite.rect.top < 0:
					sprite.kill()
		if len(self.platforms) == 0:
			self.playing = False

	def events(self):
		# Game loop - events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump()

	def draw(self):
		# Game loop - draw
		self.screen.fill(BGCOLOR)
		self.all_sprites.draw(self.screen)
		self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
		pg.display.flip()

	def draw_text(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

	def show_start_screen(self):
		pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
		pg.mixer.music.play(loops=-1)
		self.screen.fill(BGCOLOR)
		self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 5)
		self.draw_text ("Use your arrow keys to move around and Space to jump!", 22, GREEN, WIDTH /2, HEIGHT /2.5)
		self.draw_text("Collect all the gold pieces!", 22, YELLOW, WIDTH / 2, HEIGHT * 3 / 5)
		self.draw_text ("Press any key to start!", 22, WHITE, WIDTH /2, HEIGHT * 4/5)
		pg.display.flip()
		self.wait_for_key()
		pg.mixer.music.fadeout(500)


	def show_go_screen(self):
		# Game over screen
		if not self.running:
			return
		pg.mixer.music.load(path.join(self.snd_dir, 'Death Is Just Another Path.ogg'))
		pg.mixer.music.play(loops=-1)
		self.screen.fill(RED)
		self.draw_text("GAME OVER!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
		if self.score > self.highscore:
			self.highscore = self.score
			with open(path.join(self.dir, HS_FILE), 'w') as f:
				f.write(str(self.score))
		self.draw_text ("Your Score: " + str(self.score) + "   Highscore: " + str(self.highscore), 22, GREEN, WIDTH /2, HEIGHT /2)
		self.draw_text ("Press any key to play again!", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
		pg.display.flip()
		self.wait_for_key()
		pg.mixer.music.fadeout(500)

	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.KEYUP:
					waiting = False

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()
