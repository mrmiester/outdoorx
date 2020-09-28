import uuid
from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager


class Location(models.Model):
	"""A location for excercise"""
	title = models.CharField(max_length=200)
	geotitle = models.CharField(max_length=100, default='OutdoorEx Location')
	description = models.CharField(max_length=200, default='A short description about the location')
	comment = models.CharField(max_length=200, null=True)
	latitude = models.DecimalField(max_digits=55, decimal_places=50, null=True, blank=True)
	longitude = models.DecimalField(max_digits=55, decimal_places=50, null=True, blank=True)
	latlng = models.CharField(max_length=50, default='00.0000, 00.0000')
	date_added = models.DateTimeField(auto_now_add=True)
	equipment = models.CharField(max_length=200, default='Unfinished- needs different model')
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	# docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	multiimage = models.ImageField(null=True, blank=True, upload_to = 'location_images/', default = 'location_images/stock.png')
	image = models.ImageField(upload_to='pic_folder', null=True, default = 'stock.png')
	location_image = models.ImageField(null=True, blank=True, upload_to = 'location_images/', default = 'location_images/stock.png')
	file = models.FileField(upload_to='pic_folder')
	tags = TaggableManager()
	CALISTHENICS = 'Calisthenics'
	FREEWEIGHTS = 'Free Weights'
	MECHANISMS = 'Mechanisms'
	TRACKANDFIELD = 'Track & Field'
	SPORTS = 'Popular for Sports'
	EXTREMESPORTS = 'Extreme Sports'
	SELFDEFENCE= 'Self Defence'
	LARPING = 'Larping'
	
	PRACTICALITY_CHOICES = [
	(CALISTHENICS,'Calisthenics'),
	(FREEWEIGHTS, 'Freeweights'),
	(MECHANISMS, 'Mechanisms'),
	(TRACKANDFIELD, 'Track & Field'),
	(SPORTS, 'Popular for Sports'),
	(EXTREMESPORTS, 'Extreme Sports'), 
	(SELFDEFENCE, 'Self Defence'),
	(LARPING, 'Larping (Live Action Role Playing'),
	]
	type_of_excercise = models.CharField(
		max_length=30,
		choices=PRACTICALITY_CHOICES,
		default=CALISTHENICS
		)

	COASTAL = 'Coastal'
	RAISED = 'Raised'
	FOREST = 'Forest'
	PARK = 'Park'
	URBAN = 'Urban'
	INANDOUT = 'Indoor and Outdoor'
	SHADED = 'Shaded'

	TYPE_OF_LOCATION_CHOICES = [
	(COASTAL,'Coastal'),
	(RAISED, 'Raised'),
	(FOREST, 'Forest'),
	(PARK, 'Park'),
	(URBAN, 'Urban'),
	(INANDOUT, 'Indoor and Oudoor'),
	(SHADED, 'Shaded'),
	]
	type_of_location = models.CharField(
		max_length=30,
		choices=TYPE_OF_LOCATION_CHOICES,
		default=PARK
		)

	def __str__(self):
		return self.title


class Faction(models.Model):
	name = models.CharField(max_length = 200)
	desc = models.CharField(max_length = 10000, default = 'A great and noble faction')
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	color = ColorField(default='#FF0000')
	image = models.ImageField(upload_to = 'static/images/', default = 'static/images/no-img.jpg')
	
	def  __str__(self):
		"""Return a string representation of the model."""
		return self.name



def images_directory_path(instance, filename):
    return '/'.join(['images', str(instance.location), str(uuid.uuid4().hex + ".png")])

class Image(models.Model):
	location = models.ForeignKey(Location, default=None, on_delete=models.PROTECT, related_name='images')
	image = models.ImageField(upload_to=images_directory_path, default=None)

class Comment(models.Model):
	location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='comments')
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	body = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)

	class Meta:
		ordering = ['date_added']

	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.owner)

class Query(models.Model):
	email = models.CharField(max_length = 200)
	name = models.CharField(max_length = 200)
	message = models.CharField(max_length = 1000)
	date_added = models.DateTimeField(auto_now_add=True)

