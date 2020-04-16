import uuid

from core.language import Language


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
		TODO more dynamic mechanics
		'''
		if override_value is not None: return override_value
		cohort = self.languages[0].name + '00'
		return cohort

	def generate_languages(self, override_value):
		'''
		Populate language field, or generate a new language
		TODO: propagate new language up to game state
		'''
		if override_value is not None: return override_value
		return [Language(None)]

	def generate_socialclass(self, override_value):
		'''
		Should not be called without an override value
		'''
		if override_value is not None: return override_value
		return "worker"

	def generate_profession(self, override_value):
		'''
		Should not be called without an override_value
		'''
		if override_value is not None: return override_value
		return "unemployed"


	def generate_ethnicity(self, override_value):
		'''
		Should not be called without an override valuue
		'''
		if override_value is not None: return override_value
		return "Defaultian"

	def generate_religion(self, override_value):
		'''
		Should not be called without an override value
		'''
		if override_value is not None: return override_value
		return "Agnostic"

	def import_from_json(self, json):
		'''
		Import from file
		
		'''
		self.location = json['location']
		self.home = json['home']
		self.age = json['age']
		self.languages = json['languages']
		self.cohort = json['cohort']
		self.uuid = json['uuuid']
		self.socialclass = json['socialclass']
		self.profession = json['profession']
		self.ethnicity = json['ethnicity']
		self.religion = json['religion']

	def serialize_to_json(self):
		'''
		Export to json for writing to file
		TODO: evaluate what should be an object and what should be a reference
		'''
		json = {}
		json['location'] = self.location
		json['home'] = self.home
		json['age'] = self.age
		json['languages'] = self.languages
		json['cohort'] = self.cohort
		json['uuid'] = self.uuid
		json['socialclass'] = self.socialclass
		json['profession'] = self.profession
		json['ethnicity'] = self.ethnicity
		json['religion'] = self.religion


	def reproduce(self):
		'''
		TODO
		Creates a new Pop simulating generational shift
		'''