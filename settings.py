#game settings

TITLE = "Platform Sky"
WIDTH = 800
HEIGHT = 400
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "Sprites_Characters.png"

#Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = - 0.12
PLAYER_GRAVITY = 0.5

#Starting Map
PLATFORM_LIST = [(0, HEIGHT - 20, WIDTH / 4, 20),
				 (WIDTH / 3 - 50, HEIGHT * 3/4, 100, 20),
				 (125, HEIGHT - 350, 100, 20),
				 (450, 200, 100, 20),
				 (300, 100, 50, 20),
				 (WIDTH * 2 - 100, HEIGHT - 20, WIDTH / 4, 20),
				 (WIDTH / 2 , HEIGHT / 1.5, 25, 20),
				 (WIDTH - 50, HEIGHT - 40, 100, 20),
				 (WIDTH + 100, HEIGHT - 100, 50, 20),
				 (WIDTH + 150, HEIGHT - 200, 200, 20),
				 (WIDTH + 75, (HEIGHT / 3) - 30, 100, 20),
				 (WIDTH * 2 - 300, HEIGHT - 100, 50, 20),]

GOLD_LIST = [((50) - WIDTH / 200,(HEIGHT - 50) - HEIGHT / 100),
			(WIDTH * 2, HEIGHT - 45),
			(210, 30),
			(WIDTH * 2 - 300, HEIGHT - 130),
			(WIDTH + 80, 70)
			]
#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (89, 173, 242)
BGCOLOR = LIGHTBLUE
