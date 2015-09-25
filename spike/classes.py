class DataPoint():
	
	def __init__(self, filed_date = None, drug_name = None, count = None):
		self.filed_date = filed_date
		self.drug_name = drug_name
		self.count = count
	
	def __str__(self):
		return "Filed on {}: {} = {}".format(self.filed_date, self.drug_name, self.count)