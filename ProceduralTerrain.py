import pygame
import numpy as np
import datetime
import PerlinNoise
from PerlinNoise import round_up

display_width = 500
display_height = 300
cell_width = 50
cell_height = 50
num_rows = round_up(display_height/cell_height)
num_cols = round_up(display_width/cell_width)

# Colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (58, 169, 234)
green = (0,255,0)

def colourmap(value,cmap):
	if cmap == "blue_pink":
		
		if value<-1:
			return(100,160,255)
		elif value<=0:
			R = 100 + (value+1)*155
			G = 160 + (value+1)*95
			B = 255
			return (R,G,B)
		elif value<=1:
			R = 240 + (1-value)*15
			G = 130 + (1-value)*125
			B = 255
			return (R,G,B)
		else:
			return (240,130,255)

	elif cmap == "greyscale":

		if value<-1:
			return (0,0,0)
		elif value<=1:
			C = (value+1)*255/2
			return (C,C,C)
		else:
			return (255,255,255)
	
	elif cmap == "terrain":
		
		if value<-1:
			return (0,20,50)
		elif value<=0:
			R = 0
			G = 20 + (value+1)*40
			B = 50 + (value+1)*100
			return (R,G,B)
		elif value<0.05:
			return (230,170,60)
		elif value<0.75:
			R = 30 + ((value-0.05)/0.7)*35
			G = 65 - ((value-0.05)/0.7)*15
			B = 0
			return (R,G,B)
		elif value<=1:
			C = 100 + ((value-0.75)/0.25)*155
			return (C,C,C)
		else:
			return (255,255,255)

def generate_terrain_1(width,height,initial_cell_width,initial_cell_height,iterations):
	noise_array_composite = np.zeros((height,width))
	min_height = 0
	max_height = 0

	loading_bar_width = display_width*0.7
	loading_bar_height = display_height*0.1
	loaded_percent = 0

	for i in range(iterations):
		cell_width = int(initial_cell_width/(2**i))
		cell_height = int(initial_cell_height/(2**i))
		scale = 1/(2**i)
		grid = PerlinNoise.create_grad_vectors(width,height,cell_width,cell_height)
		for y in range(height):
			for x in range(width):
				value = PerlinNoise.perlin_coord(x,y,grid,cell_width,cell_height,scale)
				value += noise_array_composite[y,x]
				noise_array_composite[y,x] = value
				if value<min_height:
					min_height = value
				elif value>max_height:
					max_height = value
				colour = colourmap(value,"terrain")
				noise_surf.set_at([x,y],colour)
				noise_surf.set_colorkey((0,0,0))

			# if y%3==0 or y==display_height:
			# 	gameDisplay.blit(noise_surf,(0,0))
			# 	pygame.display.update()
			loaded_percent += 1/(height*iterations)
			pygame.draw.rect(gameDisplay,green,((display_width-loading_bar_width)/2,(display_height-loading_bar_height)/2,loaded_percent*loading_bar_width,loading_bar_height))
			pygame.display.update()

	return noise_array_composite,min_height,max_height

def generate_terrain_2(width,height,initial_cell_width,initial_cell_height,iterations):
	noise_array_composite = np.zeros((height,width))
	min_height = 0
	max_height = 0
	
	loading_bar_width = display_width*0.7
	loading_bar_height = display_height*0.1
	loaded_percent = 0

	for i in range(iterations):
		cell_width = int(initial_cell_width/(2**i))
		cell_height = int(initial_cell_height/(2**i))
		scale = 1/(2**i)
		noise_array,min_i,max_i = PerlinNoise.perlin_array(width,height,cell_width,cell_height,scale)
		noise_array_composite = noise_array_composite+noise_array
		
		for y in range(height):
			for x in range(width):
				value = noise_array_composite[y,x]
				if value<min_height:
					min_height = value
				elif value>max_height:
					max_height = value
				colour = colourmap(value,"terrain")
				noise_surf.set_at([x,y],colour)
				noise_surf.set_colorkey((0,0,0))
			# if y%5==0 or y==display_height:
			# 	gameDisplay.blit(noise_surf,(0,0))
			# 	pygame.display.update()
			loaded_percent += 1/(height*iterations)
			pygame.draw.rect(gameDisplay,green,((display_width-loading_bar_width)/2,(display_height-loading_bar_height)/2,loaded_percent*loading_bar_width,loading_bar_height))
			pygame.display.update()

	return noise_array_composite,min_height,max_height

def draw_screen(noise_surf,gridlines):
	gameDisplay.blit(noise_surf,(0,0))
	if gridlines:
		for r in range(num_rows):
			for c in range(num_cols):
				pos = [c*cell_width,r*cell_height]
				pygame.draw.rect(gameDisplay,black,(pos[0],pos[1],cell_width,cell_height),width=2)

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
noise_surf = pygame.Surface((display_width,display_height))
pygame.display.set_caption("Terrain")
clock = pygame.time.Clock()
crashed = False
gridlines = False

if __name__=="__main__":

	noise_array,min_height,max_height = generate_terrain_1(display_width,display_height,cell_width,cell_height,3)
	
	while not crashed:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				crashed = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					crashed = True		

				if event.key == pygame.K_g:
					gridlines = not gridlines

				if event.key == pygame.K_s:
					now = str(datetime.datetime.now())[:19]
					now = '_'.join(now.split(' '))
					now = '.'.join(now.split(':'))
					pygame.image.save(gameDisplay,"Saved/"+str(now)+".png")

		draw_screen(noise_surf,gridlines)
		pygame.display.update()
		clock.tick(60)

	pygame.quit()
	quit()