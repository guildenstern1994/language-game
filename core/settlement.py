



class Settlement(Object):
	'''
	Represents cities, towns, etc
	'''

	def __init__(self, society, location=location, name=name, size=size, pops=pops, languages=languages, trades=trades, json=json):

		if json is not None:
			self.import_from_json(json)
		else:
			self.society = society
			self.location = self.create_location(location)
			self.size = self.create_size(size)
			self.trades = self.create_trades(trades)
			self.languages = self.generate_languuages(languages)
			self.pops = self.generate_pops(pops)
			self.name = self.generate_name(name)
			

	def create_location(self, override_value):
		#TODO
		pass

	def create_size(self, override_value):
		#TODO
		pass

	def create_trades(self, override_value):
		#TODO
		pass

	def generate_languages(self, override_value):
		#TODO
		pass

	def generate_pops(self, override_value):
		#TODO
		pass

	def generate_name(self, override_value):
		#TODO
		pass