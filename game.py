import pygame, sys, random
from pygame.locals import *

# Set up pygame
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window 
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
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
font = pygame.font.SysFont(None, 32)

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
bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (BULLETWIDTH, BULLETHEIGHT))

# Set up the enemy
ENEMYSPEED = 2
ENEMYSIZE = 50
ENEMYNUMBER = 60
enemy_counter = 0
enemies = []

def terminate():
	pygame.quit()
	sys.exit()

def wait_for_key_press(keys):
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			if event.type == KEYDOWN:
				if event.key == K_q:
					terminate
				if event.key in keys:
					return
		main_clock.tick(60)


def draw_center_text(text, font, surface, y):
	textobj = font.render(text, 1, BLACK)
	textrect = textobj.get_rect()
	textrect.midtop = (WINDOWWIDTH / 2, y)
	surface.blit(textobj, textrect)

def pause_game():
	big_font = pygame.font.SysFont(None, 150)
	draw_center_text('PAUSE', big_font, window_surface, WINDOWHEIGHT/6)
	draw_center_text('Press SPACE to continue ...', font, window_surface, WINDOWHEIGHT/6 + 130)
	pygame.display.update()
	wait_for_key_press([K_SPACE, K_ESCAPE])

def gameover():
	# Use global vars 
	global score
	global bullets
	global enemies
	global player

	# Print the text and cry
	big_font = pygame.font.SysFont(None, 150)
	draw_center_text('GAMEOVER', big_font, window_surface, WINDOWHEIGHT/6)
	draw_center_text('But hey you got ' + str(score) + '.', font, window_surface, WINDOWHEIGHT/6 + 130)
	draw_center_text('Press ENTER to play again ...', font, window_surface, WINDOWHEIGHT/6 + 130 + 40)
	pygame.display.update()
	wait_for_key_press([K_RETURN])	

	# Reset the game
	score = 0
	bullets = []
	enemies = []
	player.x = 400 # TODO: don't hardcode this

# Display the name and the controls
window_surface.blit(world_image, (0, 0))
big_font = pygame.font.SysFont(None, 120)
draw_center_text('MYCOPHOBIA', big_font, window_surface, 40)
draw_center_text('arrow keys -> move the player', font, window_surface, 40 + 120)
draw_center_text('space -> shoot', font, window_surface, 40 + 120 + 40)
draw_center_text('escape -> pause game', font, window_surface, 40 + 120 + 40*2)
draw_center_text('q -> quit game', font, window_surface, 40 + 120 + 40*3)
draw_center_text('Press ENTER to play ...', font, window_surface, 40 + 120 + 40*4)
pygame.display.update()
wait_for_key_press([K_RETURN])


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
	if enemy_counter > ENEMYNUMBER:
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
			terminate()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				bullets.append(pygame.Rect(player.left + (PLAYERWIDTH - BULLETWIDTH) / 2,
					player.top - BULLETHEIGHT,
					BULLETWIDTH, BULLETHEIGHT))
			if event.key == K_ESCAPE:
				pause_game()
			if event.key == K_q:
				terminate()

	# Draw the white background onto the surface
	window_surface.blit(world_image, (0, 0))

	# Draw the enemies
	for enemy in enemies:
		pygame.draw.rect(window_surface, RED, enemy)

	# Draw the bullets
	for bullet in bullets:
		window_surface.blit(bullet_image, bullet)

	# Draw the player
	pygame.draw.rect(window_surface, BLUE, player)

	# Draw the score
	text_offset = 10
	text = font.render('Score: ' + str(score), 1, BLACK)
	text_rect = text.get_rect()
	text_rect.topleft = (WINDOWWIDTH - text_rect.width - text_offset, text_offset)
	window_surface.blit(text, text_rect)

	# Check for gameover
	for enemy in enemies:
		if enemy.bottom > WORLDBOTTOM:
			gameover()

	# Draw the window to the screen
	#print ("fps:", mainClock.get_fps())
	pygame.display.update()
	main_clock.tick(60)
