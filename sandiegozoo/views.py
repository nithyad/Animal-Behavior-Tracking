from django.template.loader import get_template
from django.http import HttpResponse
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from django.shortcuts import render


def index(request): 
	context = {}
	return render(request, 'list.html', context)

def zebra(request):
	context = animal_breakdown("Zebra")
	# Render according template
	if (context == {}): # context is empty, no data or error searching
		return render(request, 'noDataDisplay.html', context)
	return render(request, 'dataDisplay.html', context)

def penguin(request):
	context = animal_breakdown("Penguin")
	# Render according template
	if (context == {}): # context is empty, no data or error searching
		return render(request, 'noDataDisplay.html', context)
	return render(request, 'dataDisplay.html', context)

def lion(request):
	context = animal_breakdown("Lion")
	# Render according template
	if (context == {}): # context is empty, no data or error searching
		return render(request, 'noDataDisplay.html', context)
	return render(request, 'dataDisplay.html', context)

def animal_breakdown(targetAnimal):
	# Get activity data from csv file
	output = []
	with open('sandiegozoo/static/animal_activity_data.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter='\t')
		for row in reader:
			for items in dict(row).values():
				first = True
				for item in items.split(","):
					if first:
						first = False
						if item != targetAnimal:
							break
					output.append(item)

	# get animal information from csv file
	animalInfo = []
	with open('sandiegozoo/static/animal_information.csv') as csvfile:
		reader = csv.DictReader(csvfile, delimiter='\t')
		for row in reader:
			for items in dict(row).values():
				first = True
				for item in items.split(","):
					if first:
						first = False
						if item != targetAnimal:
							break
					animalInfo.append(item)

	# Fill in context to pass to 
	context = {'animal': targetAnimal,
			   'active': output[1],
			   'nonActive': output[2],
			   'imageURL': animalInfo[1],
			   'fun_fact_1': animalInfo[2],
			   'fun_fact_2': animalInfo[3],
			   'fun_fact_3': animalInfo[4]}

	return context
