from django.template.loader import get_template
from django.http import HttpResponse
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from django.shortcuts import render


def index(request):
	# Fill in context to pass to 
	context = {'animal': 'Zebra',
			   'active': 100,
			   'nonActive': 240}

	# Render according template
	if (context == {}): # context is empty, no data
		return render(request, 'noDataDisplay.html', context)
	return render(request, 'dataDisplay.html', context)

