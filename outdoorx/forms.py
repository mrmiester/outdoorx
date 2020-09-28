from django import forms
from .models import Location, Image, Comment, Query

class QueryForm(forms.ModelForm):
	class Meta:
		model = Query
		fields = ['name', 'email', 'message']
		labels = {'name':'z',
				'email': 'z',
				'message': 'z'}
		widgets = {
          'message': forms.Textarea(attrs={'rows':6}),
        }

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields = ['body']
		labels = {'body':''}
		widgets = {'body': forms.TextInput(attrs={'style': 'width: 40%'})}
		
		
class LocationForm(forms.ModelForm):
	latitude = forms.DecimalField(label= 'Latitude',
                           widget= forms.HiddenInput
                           (attrs={'id':'latbox'}))
	longitude = forms.DecimalField(label='Longitude',
                           widget= forms.HiddenInput
                           (attrs={'id':'lngbox'}))
	"""multiimage = forms.ImageField(label='multiimage',widget=forms.ClearableFileInput(attrs={'multiple': True}))"""

	class Meta:
		model = Location
		comment = forms.CharField()
		your_name = forms.CharField(label='Your name', max_length=100)
		fields = ['title','description','type_of_excercise','type_of_location','latitude','longitude', 'tags',]
		labels = {
		# 'latitude': 'Latitude',
		# 'longitude': 'Longitude'
		'type_of_location': 'Type of Location',
		'type_of_excercise': ' Type of Activity',
		'equipment':'Is There Any Equipment?',
		}
		widgets = {
			'title' :forms.HiddenInput(attrs={'id': 'geotitle4'}),
			'description': forms.TextInput(attrs={'cols': 10}),
			}

class ImageForm(forms.ModelForm):
	model=Image
	label = 'image'
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': 
True, 'label': 'Images: up to 9'}))