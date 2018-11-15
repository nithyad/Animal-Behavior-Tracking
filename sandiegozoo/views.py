from django.template.loader import get_template
from django.http import HttpResponse
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from django.shortcuts import render


def index(request):
	# # Get data from csv file
	# # TODO(amysorto): Clean up reading from csv file and fillin in context
	# output = []
	# with open('sandiegozoo/static/animalActivityData.csv') as csvfile:
	# 	reader = csv.DictReader(csvfile, delimiter='\t')
	# 	for row in reader:
	# 		for items in dict(row).values():
	# 			for item in items.split(","):
	# 				output.append(item)

	# # Fill in context to pass to 
	# context = {'animal': output[0],
	# 		   'active': output[1],
	# 		   'nonActive': output[2]}

	# # Render according template
	# if (context == {}): # context is empty, no data
	# 	return render(request, 'noDataDisplay.html', context)
	# return render(request, 'dataDisplay.html', context)

	context = {}
	return render(request, 'list.html', context)

