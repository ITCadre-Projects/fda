import urllib.request
from urllib.parse import urlparse
from .classes import DataPoint
import json

def get_json(url, username = None, password = None):
	if(username and password):
		url_parts = urlparse(url)
		url_base = "{}://{}/".format(url_parts.scheme, url_parts.netloc)
		password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		password_manager.add_password(None, url_base, username, password)
		auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
		opener = urllib.request.build_opener(auth_handler)
		urllib.request.install_opener(opener)
	with urllib.request.urlopen(url) as response:
		raw = response.read().decode('utf-8')
		data = json.loads(raw)
		return data

def baseline_10_years():
	base = "https://api.fda.gov/drug/event.json"
	search = "receivedate:[20050101+TO+20150101]"
	count = "receivedate"
	url = "{}?search={}&count={}".format(base, search, count)
	data = get_json(url)
	points = []
	for result in data["results"]:
		point = DataPoint(filed_date=result["time"], drug_name="All", count=result["count"])
		points.append(point)
	return points
