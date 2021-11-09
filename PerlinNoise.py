import random
import numpy as np
from Vector_Operations import *

def round_up(value):
	return int(value)+(value%1>0)

def smoothstep(x):
	if x<=0:
		return 0
	elif x>=1:
		return 1
	else:
		return (3*(x**2) - 2*(x**3))

def interpolate1D(x,a0,a1):
	return (a0+smoothstep(x)*(a1-a0))

def interpolate2D(point,vertices):
	x,y = point[0],point[1]
	tl,tr,bl,br = vertices[0],vertices[1],vertices[2],vertices[3]
	top = interpolate1D(x,tl,tr)
	bottom = interpolate1D(x,bl,br)
	final = interpolate1D(y,top,bottom)
	return final

def create_grad_vectors(width,height,cell_width,cell_height):
	num_rows = round_up(height/cell_height)
	num_cols = round_up(width/cell_width)
	grid = np.empty((num_rows+1,num_cols+1),dtype=list)	
	for r in range(num_rows+1):
		for c in range(num_cols+1):
			grad_vector = get_unit_vector([random.uniform(-1,1),random.uniform(-1,1)])
			grid[r,c] = grad_vector
	return grid

def get_dot_products(point,grid_points,grid):
	x,y = point[0],point[1]
	vertices = [[0,0],[1,0],[0,1],[1,1]]
	grad_vectors = [grid[grid_points[0][0],grid_points[0][1]],grid[grid_points[1][0],grid_points[1][1]],grid[grid_points[2][0],grid_points[2][1]],grid[grid_points[3][0],grid_points[3][1]]]
	dot_products = []
	for i in range(4):
		vertex_pos = vertices[i]
		offset_vector = get_vector(vertex_pos,point)
		dot_product = dot(grad_vectors[i],offset_vector)
		dot_products.append(dot_product)
	return dot_products

def perlin_array(width,height,cell_width,cell_height,scale=1):
	max_height = 0
	min_height = 0
	grid = create_grad_vectors(width,height,cell_width,cell_height)
	noise_array = np.zeros((height,width))
	for y in range(height):
		for x in range(width):
			rel_x = (x-(x//cell_width)*cell_width)/cell_width
			rel_y = (y-(y//cell_height)*cell_height)/cell_height
			grid_points = ([y//cell_height,x//cell_width],[y//cell_height,x//cell_width+1],[y//cell_height+1,x//cell_width],[y//cell_height+1,x//cell_width+1])
			dot_products = get_dot_products([rel_x,rel_y],grid_points,grid)
			value = interpolate2D([rel_x,rel_y],dot_products)*2/1.4143
			value *= scale

			if value>max_height:
				max_height = value
			elif value<min_height:
				min_height = value

			noise_array[y,x] = value

	return noise_array,min_height,max_height

def perlin_coord(x,y,grid,cell_width,cell_height,scale=1):
	rel_x = (x-(x//cell_width)*cell_width)/cell_width
	rel_y = (y-(y//cell_height)*cell_height)/cell_height
	grid_points = ([y//cell_height,x//cell_width],[y//cell_height,x//cell_width+1],[y//cell_height+1,x//cell_width],[y//cell_height+1,x//cell_width+1])
	dot_products = get_dot_products([rel_x,rel_y],grid_points,grid)
	value = interpolate2D([rel_x,rel_y],dot_products)*2/1.4143
	value *= scale
	return value

if __name__=="__main__":
	print(perlin_array(50,50,10))