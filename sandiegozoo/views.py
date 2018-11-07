from django.template.loader import get_template
from django.http import HttpResponse
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def index(request):
	if (os.path.isfile('sandiegozoo/static/images/activityPieChart.png')):
		t = get_template('dataDisplay.html')
	else:
		t = get_template('noDataDisplay.html') # no found data to display
	html = t.render()
	return HttpResponse(html)
