from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, redirect
from session_manager.models import Session
from django.contrib.auth.decorators import login_required
# import the login module as auth_login, since I already have a login view and the names would conflict
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login

# Python decorator requiring using accessing view to be logged in
# If used is not logged in they get redirected to /login/
@login_required(login_url='/login/')
def home(request):
    # Give the user only their sessions, not anyone elses'
    objs = Session.objects.filter(owner=request.user)
    return render_to_response('splash.html', {'objs': objs}, context_instance=RequestContext(request))

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pw")
        print "Auth attempt: " + username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Login the user with the credentials provided and redirect to their home page
                auth_login(request, user)
                return redirect('home')
            else:
                return redirect('login')
        else:
            return redirect('login')
    return render_to_response('login.html', context_instance=RequestContext(request))
    
def logout(request):
    logout_then_login(request,"login")
    return redirect('login')
    
def register(request):
	if request.method == "POST":
		name = request.POST.get("name")
		email = request.POST.get("email")
		password = request.POST.get("password")
		print name + " " + email + " " + password
		# Create the account and then save it to the database
		user = User.objects.create_user(name, email, password)
		user.save()
	return render_to_response('login.html', context_instance=RequestContext(request))
