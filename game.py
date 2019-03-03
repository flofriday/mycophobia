import pygame, sys, random
from pygame.locals import *

# Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window 
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
#windowSurface = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH), 0, 32)
WINDOWFLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE 
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), WINDOWFLAGS) 
pygame.display.set_caption('Mycophobia')

# Some colors TODO: delete later
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BLUE = (0, 0, 255)

# Set up the player
PLAYERSPEED = 10
PLAYERWIDTH = 25
PLAYERHEIGHT = 50
player = pygame.Rect(400, WINDOWHEIGHT * 0.75, PLAYERWIDTH, PLAYERHEIGHT) # TODO: replace 400 here with the actuall value

# Set up the bullets
BULLETSPEED = 30
BULLETWIDTH = 10
BULLETHEIGHT = 20
bullets = []

# Run the game loop
while True:
	# Check for the quit event
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_UP:
				bullets.append(pygame.Rect(player.left + (PLAYERWIDTH - BULLETWIDTH) / 2,
					player.top - BULLETHEIGHT,
					BULLETWIDTH, BULLETHEIGHT))
		if event.type == KEYUP:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

	# Move the player
	keys = pygame.key.get_pressed()
	if keys[K_LEFT]: 
		player.left -= PLAYERSPEED
		if player.left < 0:
			player.left = 0
	if keys[K_RIGHT]:
		player.right += PLAYERSPEED
		if player.right > WINDOWWIDTH:
			player.right = WINDOWWIDTH

	# Draw the white background onto the surface
	windowSurface.fill(WHITE)

	# Draw the player
	pygame.draw.rect(windowSurface, BLUE, player)

	# Draw the bullets
	for bullet in bullets:
		pygame.draw.rect(windowSurface, GREY, bullet)

	# Move the bullets
	for bullet in bullets:
		bullet.top -= BULLETSPEED
		# Check if he is out of the frame
		if bullet.bottom < 0:
			bullets.remove(bullet)

	# Draw the window to the screen
	print ("fps:", mainClock.get_fps())
	pygame.display.update()
	mainClock.tick(60)


