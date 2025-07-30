from django.shortcuts import render, redirect
from .models import Recipe
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Creating recipes page
@login_required(login_url='/login/')
def recipes(request):
    """
    Handle displaying and creating recipes

    - GET: Retrieves all recipes and filters by 'day' if a search parameter is present.
    - POST: Creates a new Recipe object from form data.

    Context passed to the template:
        recipes (Queryset): All or filtered Recipe objects.
    """
    if request.method == 'POST':
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')
        Recipe.objects.create(
            day = day,
            name = name,
            description = description,
        )
        return redirect('/')
    
    queryset = Recipe.object.all()
    if request.GET.get('search'):
        queryset = queryset.filter(day__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'recipe.html', context)

# Update the recipes data
@login_required(login_url='/login/')
def update_recipe(request, id):
    """
    Update an existing recipe by ID.

    POST: Update the recipe with form data.
    GET: Render form pre-filled with the recipe data.
    """
    recipe = Recipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        recipe.day = data.get('day')
        recipe.name = data.get('name')
        recipe.description = data.get('description')
        recipe.save()
        return redirect('/')
    
    context = {'recipe': recipe}
    return render(request, 'update_recipe.html', context)


@login_required(login_url='/login/')
def delete_recipe(request, id):
    """
    Delete an existing recipe by ID and redirect to home.
    """
    recipe = Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('/')


def login_page(request):
    """
    Handle user login.

    POST: Authenticate and log in user if credentials are valid.
    GET: Render login page.
    """
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username not found")
                return redirect('/login/')
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('recipes')
            
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        
        except Exception:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
        
    return render(request, "login.html")
    

def register_page(request):
    """
    Handle user registration.

    POST: Create new user if username is not taken.
    GET: Render registration page.
    """
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            messages.success(request, "Account create")
            return redirect('/login/')
        except Exception:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
        
    return render(request, "register.html")


def custom_logout(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def pdf(request):
    """
    Generate PDF view with recipes.

    POST: Add new recipe.
    GET: Display all recipes or filter by search query.
    """
    if request.method == 'POST':
        data = request.POST
        Recipe.objects.create(
            day=data.get('day'),
            name=data.get('name'),
            description=data.get('description'),
        )
        return redirect('pdf')
    
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(day__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'pdf.html', context)