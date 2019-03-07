import pygame, sys, random
from pygame.locals import *

# Set up pygame
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window 
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
#windowSurface = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH), 0, 32)
WINDOWFLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE 
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), WINDOWFLAGS) 
pygame.display.set_caption('Mycophobia')

# Some colors TODO: delete later
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the world
world_image = pygame.image.load('background.png')
world_image = pygame.transform.scale(world_image, (WINDOWWIDTH, WINDOWHEIGHT))
WORLDBOTTOM = WINDOWHEIGHT * 0.70
score = 0

# Set up the player
PLAYERSPEED = 10
PLAYERWIDTH = 25
PLAYERHEIGHT = 50
player = pygame.Rect(400, WORLDBOTTOM - PLAYERHEIGHT, PLAYERWIDTH, PLAYERHEIGHT) # TODO: replace 400 here with the actuall value

# Set up the bullets
BULLETSPEED = 20
BULLETWIDTH = 10
BULLETHEIGHT = 20
bullets = []

# Set up the enemy
ENEMYSPEED = 2
ENEMYSIZE = 50
enemy_counter = 0
enemies = []

# Run the game loop
while True:
	# Move the bullets
	for bullet in bullets[:]:
		bullet.top -= BULLETSPEED
		# Check if he is out of the frame
		if bullet.bottom < 0:
			bullets.remove(bullet)	

	# Move the enemies
	for enemy in enemies[:]:
		enemy.top += ENEMYSPEED

	# Check if a bulltet colides with an enemy
	for enemy in enemies[:]:
		for bullet in bullets[:]:
			if bullet.colliderect(enemy):
				bullets.remove(bullet)
				enemies.remove(enemy)
				score += 1

	# Spawn enemies
	enemy_counter += 1
	if enemy_counter > 40:
		enemy_counter = 0
		enemies.append(pygame.Rect(random.randint(0, WINDOWWIDTH - ENEMYSIZE), -ENEMYSIZE, ENEMYSIZE, ENEMYSIZE))

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

	# Check for the quit event
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE or event.key == K_RETURN:
				bullets.append(pygame.Rect(player.left + (PLAYERWIDTH - BULLETWIDTH) / 2,
					player.top - BULLETHEIGHT,
					BULLETWIDTH, BULLETHEIGHT))
		if event.type == KEYUP:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

	# Draw the white background onto the surface
	window_surface.blit(world_image, (0, 0))

	# Draw a line at the worldbottom
	line = pygame.Rect(0, WORLDBOTTOM, WINDOWWIDTH, 1)
	pygame.draw.rect(window_surface, BLACK, line)

	# Draw the enemies
	for enemy in enemies:
		pygame.draw.rect(window_surface, RED, enemy)

	# Draw the bullets
	for bullet in bullets:
		pygame.draw.rect(window_surface, GREY, bullet)

	# Draw the player
	pygame.draw.rect(window_surface, BLUE, player)

	# Check for gameover
	for enemy in enemies:
		if enemy.bottom > WORLDBOTTOM:
			# TODO: Display a proper gameover screen
			print("\nGAMEOVER\nsry bro\n\nbut hey you got ", score, " mushrooms")
			pygame.quit
			sys.exit()

	# Draw the window to the screen
	#print ("fps:", mainClock.get_fps())
	pygame.display.update()
	main_clock.tick(60)
