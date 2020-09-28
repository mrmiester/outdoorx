from django.db.models import Q
from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.models import User
from .models import Location, Faction,Image
from .forms import QueryForm, LocationForm, ImageForm, CommentForm
from django.forms import modelform_factory,modelformset_factory
from django.http import JsonResponse
from django.views import View



# Create your views here.
def factions(request):
	factions = Faction.objects.order_by('word')
	context = {'factions' : factions, }
	return render(request, 'master/factions.html', context)


def success(request):
	return render(request, 'master/success.html')

def index(request):
	locations = Location.objects.order_by('date_added').reverse()[:9]
	images = Image.objects.all()
	coords = []
	if request.method != 'POST':
		form = QueryForm()
	else:
		form = QueryForm(data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('index'))
 	# for location in Location.latlng coords.append()
	context = {
		'locations' : locations,
		'coords': coords,
		'images': images,
		'form': form,
		}
	return render(request, 'master/index.html', context)


def News(request):
	return HttpResponse("<h1>This is our latest news</h1>")

def Contact(request):
	return HttpResponse("<h1>Contact us here!</h1>")


@login_required
def new_entry(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	images = Image.objects.all()
	if request.method != 'POST':
		form = EntryForm()
		queryform = QueryForm()
	else:
		form = EntryForm(data=request.POST)
		queryform = QueryForm(data=request.POST)
		if queryform.is_valid():
			queryform.save()
		elif form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('topic', args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'master/new_entry.html', context)

@login_required
def location(request, location_id):
	location = Location.objects.get(id=location_id)
	images = Image.objects.all()
	comments = location.comments.filter(active=True)
	new_comment = None
	if request.method != 'POST':
		form = CommentForm()
		queryform = QueryForm()
	else:
		form = CommentForm(data=request.POST)
		queryform = QueryForm(data=request.POST)
		if queryform.is_valid():
			queryform.save()
		elif form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.location = location
			new_comment.owner = request.user
			new_comment.save()
			return HttpResponseRedirect(reverse('location', args=[location_id]))
	context = {
		'location': location, 
		'form': form,
		'images': images,
		'new_comment': new_comment,
		'comments': comments,
	}
	return render(request, 'master/location.html', context)



def locations(request):
	locations =Location.objects.order_by('date_added')
	context = {'locations':locations}
	return render(request, 'master/locations.html', context)

@login_required
def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	if topic.owner!= request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries' : entries}
	return render(request, 'master/topic.html', context)

class LocationView(FormView):
	form_class = LocationForm
	template_name='master/new_location.html'
	success_url = 'index'

	def post(self,request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('images')	
		if form.is_valid():
			form.owner=User.objects.all().first()
			for file in files:
				instance = Image(location=Location.objects.get(), photo=file)
				instance.owner=self.request.user
				instance.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

@login_required
def new_location(request):
	if request.method != 'POST':
		form = LocationForm()
		files = request.FILES.getlist('images')
	else:
		form = LocationForm(data=request.POST)
		files = request.FILES.getlist('images')
		if form.is_valid():
			new_location = form.save(commit=False)
			new_location.owner = request.user
			new_location.save()
			for file in files:
				instance = Image(location=new_location, image=file)
				instance.save()
			form.save_m2m()
		location_id = Location.objects.order_by('-id')[0].id
		return HttpResponseRedirect(reverse('location', args=[location_id]))
	context = {'form': form,'files': files,}
	return render(request, 'master/new_location.html', context)
