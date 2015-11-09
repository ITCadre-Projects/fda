from django.shortcuts import render
from .models import DataPoint
from .services import baseline_10_years
from .services import searcb_by_product
from django.http import HttpResponse

def index(request):
	data_points = DataPoint.objects.order_by('filed_date')
	context = {'data_points': data_points}
	return render(request, 'spike/index.html', context)
	
def fda(request):
	data_points = baseline_10_years()
	context = {'data_points': data_points}
	return render(request, 'spike/index.html', context)

def search_form(request):
	return render(request, 'spike/search.html')

def search(request):
	if 'drug_name' in request.GET and request.GET['drug_name']:
		drug_name = request.GET['drug_name']
		start_date = request.GET['start_date']
		end_date = request.GET['end_date']
		#print(drug_name)
		data_points = searcb_by_product(drug_name, start_date,end_date)

		print("--------------")
		print(data_points)
		if(data_points):
			context = {'data_points': data_points}
			return render(request, 'spike/index.html', context)
		else:
			return render(request, 'spike/search.html', {'error': True})
	else:
		return render(request, 'spike/search.html', {'error': True})