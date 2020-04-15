import uuid


class Pop(object):
	'''
	Basic population unit
	'''

	def __init__(self, location, home, uuid=None, age=None, cohort=None, languages=None, profession=None, socialclass=None, ethnicity=None, religion=None, json=None):
		'''
		Note: should only be called from a Pop or Settlement object
		'''
		if json is not None:
			self.import_from_json(json)
		else:
			self.location = location
			self.home = home
			self.age = self.generate_age(age)
			self.languages = self.generate_languages(languages)
			self.cohort = self.generate_cohort(cohort)
			self.uuid = self.generate_uuid(uuid)
			self.socialclass = self.generate_socialclass(socialclass)
			self.profession = self.generate_profession(profession)
			self.ethnicity = self.generate_ethnicity(ethnicity)
			self.religion = self.generate_religion(religion)


	def generate_uuid(self, override_value):
		'''
		Unique id for this object
		'''
		if override_value is not None: return override_value
		return uuid.uuid4()


	def generate_age(self, override_value):
		'''
		Age in human years
		'''
		if override_value is not None: return override_value
		return 0

	def generate_cohort(self, override_value):
		'''
		TODO
		'''
		if override_value is not None: return override_value
		cohort = self.languages[0].name + '00'
		return cohort

	def generate_languages(self, override_value):
		'''
		TODO
		'''
		pass

	def generate_socialclass(self, override_value):
		'''
		TODO
		'''
		pass

	def generate_profession(self, override_value):
		'''
		TODO
		'''
		pass


	def generate_ethnicity(self, override_value):
		'''
		TODO
		'''
		pass

	def generate_religion(self, override_value):
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

	def reproduce(self):
		'''
		TODO
		Creates a new Pop simulating generational shift
		'''