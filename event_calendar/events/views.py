from django.shortcuts import render
from django.http import JsonResponse
from .models import AppUser, Event
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#home screen view
def index(request):
    # checking to see if user is logged in
    if request.user.is_authenticated:
        #if they are, I am grabbing their event objects to display on their home screen
        events = Event.objects.filter(owner=request.user.id).values()
        # creating a data package with their full name and their objects
        full_name = f"{request.user.first_name} {request.user.last_name}"
        data = {'full_name': full_name, 'events': events}
        #rendering the home page with their data so they get a greeting in navbar and their events are
        #displayed on home screen
        return render(request, 'pages/index.html', data)
    else:
        #if not logged in I am rendering home page with no data
        return render(request, 'pages/index.html')

#signup view
def sign_up(request):
    #if post request I grab the values out of the request so I can create user
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        try:
            #creating new user
            AppUser.objects.create_user(first_name=first_name, last_name=last_name,  username=username, email=email, password=password)
            
        except Exception as e:
            print('oops!')
            print(str(e))
        #since the user just signed up successfully I am logging them in so they are logged in when
        # re-directed to home page    
        user = authenticate(email=email, password=password)
        login(request, user)
        #returning friendly message to be alerted to user
        return JsonResponse({'status': 'Account created successfully!'})
    #if get request rendering the initial signup page
    return render(request, 'pages/signup.html')

#log in view
def log_in(request):
    #if post, grabbing values
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        #grabbing the user
        user = authenticate(email=email, password=password)

        #logging them in if they exist and are active user
        if user is not None:
            if user.is_active:
                try:
                    login(request, user)
                except Exception as e:
                    print('oops!')
                    print(str(e))
        #friendly messages depending on outcome to be displayed to user in an alert
                return JsonResponse({'status': 'Successfully logged in!'})
            else:
                return JsonResponse({'status': 'User not active!'})
        else:
            return JsonResponse({'status': 'No user!'})

    #if a get request rendering the initial login page
    return render(request, 'pages/login.html')

#logout view, pretty self explanatory
def log_out(request):
    logout(request)
    return render(request, 'pages/index.html')

#add item view
def add_item(request):
    #if post,grabbing values and creating a new event and saving it
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        start = request.POST['start']
        end = request.POST['end']
        new_event = Event(name=name, description=description, starts_at=start, ends_at=end, owner=request.user)
        new_event.save()
        #returning friendly response to be alerted to user
        return JsonResponse({'status': 'Event Added!'})
    #if get request, rendering initial add item page
    return render(request, 'pages/add_item.html')

#update item view
def update_item(request, id):
    #if post grabbing needed values
    if request.method == 'POST':
        id = request.POST['id']
        #in order to use same update page to delete, put this conditional in to catch
        #deletion cases and treat appropriately
        if request.POST['type'] == "delete":
            item = Event.objects.get(id=id)
            item.delete()
            #friedly response
            return JsonResponse({'status': 'Event Deleted!'})
        else:
            #if not a deletion
            name = request.POST['name']
            description = request.POST['description']
            start = request.POST['start']
            end = request.POST['end']

            #after getting the values from the post request
            #querying for the item and setting the new values and saving
            item = Event.objects.get(id=id)
            item.name = name
            item.description = description
            item.starts_at = start
            item.ends_at = end
            item.save()
            #returning friedly response
            return JsonResponse({'status': 'Event Updated!'})
    #if get request, querying to grab them event from db to push to update page to populate form 
    #with existing values for the selected event
    event = Event.objects.filter(id=id).values()[0]

    data = {"event": event}
    #build data package and render page with data
    return render(request, 'pages/update_item.html', data)