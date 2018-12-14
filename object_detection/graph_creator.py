import numpy as np
import matplotlib.pyplot as plt
import csv
import math


def creategraphs(csv1, csv2):
	# getting information from distances csv
	coordinates = []
	with open(csv1, mode='r') as csv_file:	
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			xcoordinate = row["x-coords"]
			ycoordinate = row["y-coords"]
			coordinates.append([float(xcoordinate), float(ycoordinate)])

	#getting the time information from frames csv
	times = []
	with open(csv2, mode='r') as csv_file:	
		csv_reader = csv.DictReader(csv_file)
		counter = 0
		for row in csv_reader:
			if counter != 0:
				frame = row["file_name"]
				time = row["millis"]
				time = time + str(counter)
				times.append(time)
			counter += 1

	times[:-1]

	distance = []
	for values in range(len(coordinates) - 1):
		x_distance = (coordinates[values][0] - coordinates[values+1][0]) ** 2
		y_distance = (coordinates[values][1] - coordinates[values+1][1]) ** 2
		euclid_distance = math.sqrt(x_distance + y_distance)
		distance.append(euclid_distance)

	plt.plot(times, distance, color='g')
	plt.xlabel('Millisecond')
	plt.ylabel('Movement Distance')
	plt.title('Active Time Frame')
	plt.savefig("graph.png")