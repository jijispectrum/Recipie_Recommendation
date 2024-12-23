# from django.http import HttpResponse
# from django.template import loader
# from django.shortcuts import render,redirect
# from django.contrib.auth import authenticate,login,logout
# from django.contrib import messages
# from .forms import LoginFortm, Signupform
# from .models import UserProfile
# from django.contrib.auth.models import user
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request,'index.html')
def about(request):
    template=loader.get_template('about.html')
    return HttpResponse(template.render())

def contact(request):
    template=loader.get_template('contact.html')
    return HttpResponse(template.render())
def login(request):
    template=loader.get_template('login.html')
    return HttpResponse(template.render())
def register(request):
    template=loader.get_template('register.html')
    return HttpResponse(template.render())



from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Create a new user with a hashed password
        user = User.objects.create(username=username, email=email, password=make_password(password))
        return redirect('login_page')  # Redirect to the login page

    return render(request, 'register.html')
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import redirect

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect
            login(request, user)
            return redirect('home')  # Replace 'home' with your target view name
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    # Log the user out
    logout(request)
    
    # Display a success message
    messages.success(request, "You have successfully logged out.")
    
    # Redirect to the login page or home page
    return redirect('login_page')  # You can change 'login_page' to any other URL name you prefer


# recommendations/views.py
# recommendations/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils import load_data, preprocess_data, get_recipe_vectors, calculate_similarity
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity









# Load data and preprocess it
data = load_data('app7/ml_models/dataset.zip')
  # Update path to your dataset

data = preprocess_data(data)
cv, vectors = get_recipe_vectors(data)
similarity = calculate_similarity(vectors)

@login_required 
def recommend_recipes(request):
    input_ingredients = request.GET.get('ingredients', '')
    
    recommended_recipes = []

    if input_ingredients:
        # Preprocess the input ingredients
        input_data = preprocess_data(pd.DataFrame([input_ingredients], columns=["Ingredients"]))
        input_vector = cv.transform(input_data["Cleaned_Ingredients"]).toarray()

        # Calculate the similarity with the existing recipes
        input_similarity = cosine_similarity(input_vector, vectors)
        recommendations = sorted(list(enumerate(input_similarity[0])), reverse=True, key=lambda x: x[1])[1:6]

        # Collect recommended recipes
        for i in recommendations:
            recipe = data.iloc[i[0]]
            recommended_recipes.append({
                'title': recipe['Title'],
                'ingredients': recipe['Ingredients'],
                'instructions': recipe['Instructions'],
                'image_name': recipe['Image_Name']
            })
    
    return render(request, 'recommend.html', {'recommended_recipes': recommended_recipes})
from django.shortcuts import render

# def login_redirect(request):
#     messages.info(request, "You need to log in to view recipes.")
#     return redirect('login_page')
