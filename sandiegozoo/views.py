# from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
# from django.template import Template, Context
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def index(request):
	# # plot active v. non active data on a pie chart
	# df = pd.DataFrame(3 * np.random.rand(2), index=[100, 600])
	# df.plot.pie(subplots=True)
	# plt.savefig('foo.png')

  	t = get_template('sandiegozoo/index.html')
  	html = t.render({})
  	return HttpResponse(html)