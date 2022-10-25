import json
import geopy.distance

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.forms import TextInput, NumberInput, ModelForm, Textarea
from geopy.geocoders import Nominatim
from .models import User, kitchen, menu_course, dish



class restaurant_create(ModelForm):
    class Meta:
        model = kitchen
        fields = ['restaurant_name', 'phone_number', 'cuisine', 'address', 'city', 'state', 'country', 'description']
        widgets = {
            'restaurant_name': TextInput(attrs={
                'class': 'mb-3',
                'style': 'max-width: 300px;',
                'placeholder': 'name of restaurant',
                'style': 'border: solid 1px black',
            }),
            'phone_number': TextInput(attrs={
                'style': 'border: solid 1px black',
            }),
            'address': Textarea(attrs={
                'class':'mb-3',
                'rows':'2',
                'style': 'border: solid 1px black; width: 300px',
            }),
            'description': Textarea(attrs={
                'class': 'mb-3',
                'style': 'border: solid 1px black; width: 200px',
            }),
            'city': TextInput(attrs={
                'style': 'border: solid 1px black',
            }),
            'state': TextInput(attrs={
                'style': 'border: solid 1px black',
            }),
        }

class dish_submit(ModelForm):
    class Meta:
        model = dish
        fields = ['name', 'course','price', 'image_url', 'description']

def index(request):
    if request.user.is_authenticated:
        if request.method != "GET":
            return JsonResponse({"error" : "GET request required."}, status=400)
        #dish_ratings = UserRating.objects.all().order_by("created")
        collection = []
        #for rating in dish_ratings:
            #rest = dish.objects.get(name = rating.rating)
            #e = {
                #"dish_name" : rating.rating,
                #"restaurant" : rest.recipe_owner,
                #"score" : rating.score,
                #"patron" : rating.user,
            #}
            #collection.append(e)
        kitchen_list = kitchen.objects.all().order_by('-created')
        return render(request, "restaurant/index.html", {"recently_rated": collection, "kitchen_list": kitchen_list})
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "restaurant/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "restaurant/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "restaurant/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "restaurant/register.html", {
                "message": "Name already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "restaurant/register.html")

def profile(request, profile):
    restaurant_list = kitchen.objects.all()
    owners_restaurants = []
    owner_check = False
    for restaurant in restaurant_list:
        if restaurant.owner == request.user:
            owners_restaurants.append(restaurant)
            owner_check = True
    return render(request, "restaurant/profile.html", {"profile": profile, "owner_check" : owner_check, "owners_restaurants" : owners_restaurants})

def about(request):
    return render(request, "restaurant/about.html")

@login_required
def create(request):
    usern = request.user
    geolocator = Nominatim(user_agent="restaurants")
    if request.method == "GET":
        return render(request, "restaurant/create.html", {"owner": usern, "create": restaurant_create()})
    if request.method == "POST":
        form = restaurant_create(request.POST)
        if form.is_valid():
            restaurant_name = form.cleaned_data['restaurant_name']
            address = form.cleaned_data['address']
            description = form.cleaned_data['description']
            state = form.cleaned_data['state']
            cuisine = form.cleaned_data['cuisine']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            phone_number = form.cleaned_data['phone_number']
        else:
            print(form.errors)
            return render(request, "restaurant/create.html", {"create" : restaurant_create()})
        location = geolocator.geocode(address + " " + city)
        coordinates = f"{location.latitude},{location.longitude}"
        new_restaurant = kitchen(owner=usern, phone_number=phone_number, city=city, restaurant_name=restaurant_name, address=address, description=description, state=state, country=country, cuisine=cuisine, geolocation=coordinates)
        new_restaurant.save()
        return HttpResponseRedirect(reverse('eatery', kwargs={'eatery' : new_restaurant.restaurant_name}))

def eatery(request, eatery):
    course_list = menu_course.objects.all()
    restaurant_get = kitchen.objects.get(restaurant_name=eatery)
    dishes = dish.objects.filter(recipe_owner=restaurant_get)
    courses = restaurant_get.courses.all()
    #rating = Rating.objects.all().order_by("-average")
    #top_ratings = []
    #for item in rating:
        #if item.average > 3:
            #for i in dishes:
                #if item.object_id == i.id:
                    #top_ratings.append(i)
    if restaurant_get.owner == request.user:
        owner = True
        if request.method == "GET":
            return render(request, "restaurant/eatery.html", {"eatery": eatery, "restaurant_details": restaurant_get, "owner":owner, "courses":courses, "dishes":dishes, "course_list":course_list})
    else:
        owner = False
        if request.method != "GET":
            return JsonResponse({"error" : "GET request required."}, status=400)
        if request.method == "GET":
            return render(request, "restaurant/eatery.html", {"eatery": eatery, "restaurant_details": restaurant_get, "owner":owner, "courses":courses, "dishes":dishes, "course_list":course_list})

@login_required
def new_dish(request, kitchen_name):
    if request.method == "GET":
        return render(request, "restaurant/newdish.html", {"new_dish" : dish_submit()})
    if request.method == "POST":
        form = dish(request.POST)
        user = request.user
        if form.is_valid():
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            recipe_owner = kitchen_name
            image_url = form.cleaned_data["image_url"]
            course = form.cleaned_data["course"]
            description = form.cleaned_data["description"]
        else:
            print(form.errors)
            return render(request, "restaurant/newdish.html", {"new_dish" : dish_submit()})
        new = dish(name=name, price=price, image_url=image_url, course=course, description=description, recipe_owner=recipe_owner)
        new.save()
        messages.add_message(request, messages.INFO, f"'{name}' successfully added to menu")
        return HttpResponseRedirect(reverse('eatery', kwargs={"eatery": kitchen_name}))

@csrf_exempt
@login_required
def add_course(request, dishData, eatery):
    course_add = menu_course.objects.get(course_list=dishData)
    try:
        current_restaurant = kitchen.objects.get(restaurant_name = eatery)
    except kitchen.DoesNotExist:
        return JsonResponse({"error": "kitchen does not exist."}, status=404)
    if request.method == "POST":
        current_restaurant.courses.add(course_add)
        current_restaurant.save()
        return JsonResponse({"message": "course added"},status=201)
    else:
        return JsonResponse({"error": "GET request required."}, status=400)

@csrf_exempt
@login_required
def add_dish(request, eatery):
    if request.method != "POST":
        return JsonResponse({"error" : "POST request required."}, status=400)
    data = json.loads(request.body)
    user = request.user
    name = data.get("name", "")
    description = data.get("description", "")
    price = data.get("price", "")
    image_url = data.get("image_url", "")
    course = data.get("course", "")
    dish_course = menu_course.objects.get(course_list=course)
    eatery = kitchen.objects.get(restaurant_name=eatery)
    new_dish = dish(
        recipe_owner = eatery,
        name = name,
        description = description,
        price = price,
        image_url = image_url,
        course = dish_course,
    )
    new_dish.save()
    return JsonResponse({"message": "Dish added"}, status=201)

def search(request, position, distance):
    if request.method != "GET":
        return JsonResponse({"error" : "GET request required."}, status=400)
    if distance == "Walk":
        distance_lat = .03
        distance_lon = .04
    if distance == "Bike":
        distance_lat = .075
        distance_lon = .1
    if distance == "Drive":
        distance_lat = .225
        distance_lon = .3
    latitude = position.split(", ")[0]
    latitude = float(latitude)
    longitude = position.split(", ")[1]
    longitude = float(longitude)
    distance_plus_lat = latitude + distance_lat
    distance_minus_lat = latitude - distance_lat
    distance_plus_lon = longitude + distance_lon
    distance_minus_lon = longitude - distance_lon
    kitchen_list = kitchen.objects.all()
    kitchens_nearby = []
    test_dict = []
    for eatery in kitchen_list:
        coordinates = str(eatery.geolocation)
        eatery_latitude = float(coordinates.split(",")[0])
        eatery_longitude = float(coordinates.split(",")[1])
        if distance_plus_lat > eatery_latitude > distance_minus_lat and distance_plus_lon > eatery_longitude > distance_minus_lon:
            between_locations = round(geopy.distance.distance(position, coordinates).miles, 2)
            kitchens_nearby.append(eatery)
            e = {
                "eatery": eatery.cuisine.cuisine,
                "name": eatery.restaurant_name,
                "address": eatery.address,
                "city": eatery.city,
                "state": eatery.state,
                "description": eatery.description,
                "between": between_locations,
                "cuisine": eatery.cuisine.cuisine
            }
            test_dict.append(e)
    return JsonResponse([localKitchen for localKitchen in test_dict], safe=False)

def filter(request, place):
    if request.method != "GET":
        return JsonResponse({"error" : "GET request required."}, status=400)
    location_kitchens = kitchen.objects.filter(city__icontains = place)
    return JsonResponse([localEatery.serialize() for localEatery in location_kitchens], safe=False)

@csrf_exempt
@login_required
def edit_dish(request, dishid):
    try:
        item = dish.objects.get(id = dishid)
    except dish.DoesNotExist:
        return JsonResponse({"error": "dish does not exist."}, status=404)
    if request.method == "GET":
        return JsonResponse(item.serialize())
    if request.method == "POST":
        data = json.loads(request.body)
        description = data.get("description", "")
        name = data.get("name", "")
        price = data.get("price", "")
        image = data.get("image", "")
        item.description = description
        item.name = name
        item.price = price
        item.image_url = image
        item.save()
        return JsonResponse({"message": "post successfully edited!"}, status=201)
    else:
        return JsonResponse({"error": "GET or POST request required."}, status=400)

@csrf_exempt
@login_required
def delete_dish(request, dishid):
    try:
        item = dish.objects.get(id = dishid)
    except dish.DoesNotExist:
        return JsonResponse({"error": "dish does not exist."}, status=404)
    if request.method != "GET":
        return JsonResponse({"error" : "GET request required."}, status=400)
    item.delete()
    return JsonResponse({"message": "dish deleted"}, status=201)

@csrf_exempt
@login_required
def delete_course(request, eatery, course):
    if request.method != "GET":
        return JsonResponse({"error" : "GET request required."}, status=400)
    current_course = menu_course.objects.get(course_list = course)
    current_kitchen = kitchen.objects.get(restaurant_name = eatery, owner = request.user)
    current_kitchen.courses.remove(current_course)
    return JsonResponse({"message": "course deleted"}, status=201)
