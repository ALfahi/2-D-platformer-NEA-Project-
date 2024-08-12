import pygame
import os
import csv
#inititialising pygame
pygame.init()
#defining constants
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 900
LOWER_MARGIN = 100
SIDE_MARGIN = 600
FPS = 60

#creating a constant for the levels
global level
level = 0# the base level

#creating the internal clock
clock = pygame.time.Clock()
#Creating the screen
screen = pygame.display.set_mode((SCREEN_HEIGHT+ SIDE_MARGIN, SCREEN_WIDTH + LOWER_MARGIN))
#creating a button class for the tiles
class tile_button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()# width is the image's width.
		height = image.get_height()#height is the image's height
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))# tranforms the images by the height and width
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):# draws the buttons onto the scree.
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

#loading in the images for the background
sky_img = pygame.image.load("C:game_background_3\layers\sky.png").convert_alpha()#loads the sky
sky_img_1 = pygame.transform.scale(sky_img,(int(sky_img.get_width()*0.98181818), int(sky_img.get_height()* 1)))
cloud_1 = pygame.image.load("C:game_background_3\layers\clouds_1.png").convert_alpha()#loads the first set of clouds
clouds_2 =  pygame.image.load("C:game_background_3\layers\clouds_2.png").convert_alpha()#loads in the second set of clouds
ground_1 =  pygame.image.load("C:game_background_3\layers\ground_1.png").convert_alpha()#loads in the first set of gorund
ground_2 =  pygame.image.load("C:game_background_3\layers\ground_2.png").convert_alpha()#loads in the second set of ground
ground_3 =  pygame.image.load("C:game_background_3\layers\ground_3.png").convert_alpha()#loadsin in the third set of ground
rock = pygame.image.load("rocks2.png")#loads in the rocks 

#creating varibales for the grid system:
ROWS = 32
MAX_COLUMNS = 350
tile_size = SCREEN_HEIGHT// ROWS
TILE_TYPES = 11# how many different types of images is in my folder

# storing the tile images on the list:
tile_list = []
for x in range(TILE_TYPES):# iterates through my file and loads each of the images.
#    img = pygame.image.load(f"C:tiles/{x}.png") uncomment this when running code at home and comment out the other one.
    img = pygame.image.load(f"C:tiles/{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    tile_list.append(img)
# loading in the imagtes for the buttons
save_btn = pygame.image.load("C:\Al Faysal\python\save_btn.png")
load_btn = pygame.image.load("C:\Al Faysal\python\load_btn.png")

#creating the actual buttons
save = tile_button(SCREEN_HEIGHT//2 - 200, SCREEN_WIDTH + LOWER_MARGIN - 150,save_btn, 3)
load = tile_button(SCREEN_HEIGHT//2 + 500, SCREEN_WIDTH + LOWER_MARGIN - 150,load_btn, 3)


#define font
font = pygame.font.SysFont('Futura', 30)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
#creating buttons and a button list:
button_list = []
button_col = 0
button_row = 0
for i in range(len(tile_list)):
    tile_buttons = tile_button(SCREEN_WIDTH + (75 * button_col) + 50, 75* button_row + 50, tile_list[i], 1)
    button_list.append(tile_buttons)
    button_col +=1
    if button_col == 6:# how many buttons will be displayed in one row
        button_row +=1# goes to the next row
        button_col = 0# restarts the process until all buttons are displayed.

#creating empty list for the levels
level_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLUMNS# "-1" is for tiles which are meant to be empty.
    level_data.append(r)

    #creating ground
for tile in range(0, MAX_COLUMNS):
    level_data[ROWS - 1][tile] = 0# makes the  very bottom of the list be replaced with the ground image

    


#creating variables to scroll the screen
scroll_left = False# scrolls level to the  left
scroll_right = False# scrolls level to the right
scroll = 0
scroll_speed = 2# speed of which level is scrolling


#creating a function to display background
def background():
    screen.fill((255, 255, 224))# fills screen with yellow
    width = sky_img.get_width()
    for x in range(5):# loops the images 5 times; this means that when I scroll right;
                      # the yellow won't shown until I've passed the same image 5 times.
        screen.blit(sky_img, ((x* width) -scroll * 0.5, 0))
        screen.blit(cloud_1, ((x* width) -scroll* 0.6, 0))
        screen.blit(rock, ((x* width) -scroll* 0.65, 0))
        screen.blit(clouds_2, ((x* width) -scroll * 0.9, 0))
        screen.blit(ground_1, ((x* width) -scroll* 0.85, 0))
        screen.blit(ground_2 , ((x* width) -scroll* 0.75, 0))
        screen.blit(ground_3, ((x* width)-scroll, 0))


#drawing the grid lines
def grid():
    #creating the vertical lines
    for c in range(MAX_COLUMNS + 1):
        pygame.draw.line(screen, (255, 255, 255), (c* tile_size -scroll, 0), (c*tile_size -scroll, SCREEN_HEIGHT))# grid lines are white; "tile_size -scroll" moves the grid lines as the background scrolls.
 #drawing the horizontal lines
    for r in range(ROWS + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, r* tile_size), (SCREEN_WIDTH, r*tile_size))

#drawing the tiles
def draw_level():
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile >= 0:# only draws the tiles(and not the empty space)
                screen.blit(tile_list[tile], (x * tile_size -scroll, y * tile_size))


#defining global contants for the tile system to work
global current_tile
global button_count
button_count = 0
current_tile = button_count


#main loop
run = True
while run:
    clock.tick(FPS)
    background()# putting the background function in the main game loop.
    grid()# drawing the grid lines onto the screen.
    draw_level()
    draw_text(f'Level: {level}', font,(255, 255, 255), 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font,( 255, 255, 255), 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    #drawing the savge and load buttons onto the screen
    if save.draw(screen):
            #saving the level data
            with open(f"level.no{level}.csv", "w", newline = "") as csvfile:
                    editor = csv.writer(csvfile, delimiter = ",")# creating an object which can chnage the values in the csv file.
                    for row in level_data:# csv file has 32 rows as there is exactly 32 rows in the actual level editor.
                            editor.writerow(row)
    if load.draw(screen):
            scroll = 0# resets the scroll area back ot the start
            with open(f"level.no{level}.csv", newline = "") as csvfile:
                    viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                    for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                            for y, tile in enumerate(row):
                                    level_data[x][y] = int(tile)
    #drawing the tile panel and the tiles
    pygame.draw.rect(screen,(255, 255, 224), (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    button_count = 0
    
    for button_count, i in enumerate(button_list):# iterates through the utton list which assigns them to the varibale "i" and also keeps track of which button it's on.
        if i.draw(screen):
            current_tile = button_count
            print(current_tile)

        pygame.draw.rect(screen,(255, 0, 0), button_list[current_tile].rect, 3)




    # scrolls the map
    if scroll_left == True and scroll > 0:# makes it so that you can't scroll left when you start.
        scroll -= 5 * scroll_speed
    if scroll_right == True:
        scroll += 5 * scroll_speed
        #adding new tiles to the screen
        #getting the mouse postition.
    pos = pygame.mouse.get_pos()# gets theb postion of the mouse
    x = (pos[0] + scroll)//tile_size
    y = pos[1]//tile_size
    #checking cordinates is within the tile area.
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:# makes sure that the postion is within the tile area.
            #uptades the tile variable
            if pygame.mouse.get_pressed()[0] == 1:
                    if level_data[y][x] != current_tile:# if the tile is not the same as the tile selected.
                            level_data[y][x] = current_tile# replaces the tile with the selected tile.

            if pygame.mouse.get_pressed()[2] == 1:# if the mouse is right clicked.
                    level_data[y][x] = -1# deletes the current tile.
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:#checks if user presses on the left key
                scroll_left = True
            if event.key == pygame.K_RIGHT:#checks if user presses on the right key
                scroll_right = True
            if event.key == pygame.K_UP:# checks if the user presses the up key
                    level += 1
            if event.key == pygame.K_DOWN and level > 0:#checks if user presses the down key and also stops from going down levels infinetly
                    level -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:# checks if user has let go of the left key
                scroll_left = False
            if event.key == pygame.K_RIGHT:# checks if user has let go of the right key
                scroll_right = False
            

    pygame.display.update()

pygame.quit()
#credit for background is craftpix.net
