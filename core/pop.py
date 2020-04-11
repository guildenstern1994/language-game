


class Pop(object):
	'''
	Basic population unit
	'''

	def __init__(self, location, home, name=None, age=None, cohort=None, languages=None, profession=None, socialclass=None, ethnicity=None, religion=None, json=None):
		if json is not None:
			self.import_from_json(json)
		else:
			self.location = location
			self.home = home
			self.name = self.generate_name(name)
			self.age = self.generate_age(age)
			self.cohort = self.generate_cohort(cohort)
			self.languages = self.generate_languages(languages)
			self.socialclass = self.generate_socialclass(socialclass)
			self.profession = self.generate_profession(profession)
			self.ethnicity = self.generate_ethnicity(ethnicity)
			self.religion = self.generate_religion(religion)


	def generate_name(self, name):
		'''
		TODO
		'''
		pass

	def generate_age(self, age):
		'''
		TODO
		'''
		pass

	def generate_cohort(self, cohort):
		'''
		TODO
		'''
		pass

	def generate_languages(self, languages):
		'''
		TODO
		'''
		pass

	def generate_socialclass(self, socialclass):
		'''
		TODO
		'''
		pass

	def generate_profession(self, profession):
		'''
		TODO
		'''
		pass


	def generate_ethnicity(self, ethnicity):
		'''
		TODO
		'''
		pass

	def generate_religion(self, religion):
		'''
		TODO
		'''
		pass

	def import_from_json(self, json):
		'''
		Import from file
		TODO
		'''
		pass