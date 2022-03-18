from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from .forms import SearchBar, LoginForm, RegisterForm
from newsProject import const
import requests
from django.contrib.auth import logout
# Create your views here.


#  general function for calling apis
def apiCall(type=const.POST, url=None, reqData=None, headers=None):
    print(const.BASE_URL+url)
    if type == const.POST:
        responseData = requests.post(const.BASE_URL+url, data=reqData)
        return responseData
    elif type == const.GET:
        print("@@@@@@@@@@@@@@@@@@@@@@@@")
        print(reqData)
        
        responseData = requests.get(const.BASE_URL+url+reqData, headers=headers)
        return responseData


# call login view
def loginView(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            reqData = {'username':username, 'password':password}
            responseData = apiCall(const.POST, 'users/login/', reqData)
            print("************")
            print(responseData.status_code)
            if responseData.status_code == 200:
                responseJson = responseData.json()
                request.session['jwt_access_token'] = responseJson['access']
                request.session['jwt_refresh_token'] = responseJson['refresh']
                return redirect('../news')
            elif  responseData.status_code == 401:
                context = {'error':"Invalid user", 'form': form}
                return render(request, 'login.html', context)

    return render(request, 'login.html', {'form': form})



# call register view
def registerView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            checkpassword = form.cleaned_data["checkpassword"]

            # request data for registration
            reqData = {'username':username, 'password':password, 'checkpassword':checkpassword, 'email':email}

            # api call for registration
            responseData = apiCall(const.POST, 'users/register/', reqData)
        
            if responseData.status_code == 201:
                responseJson = responseData.json()
                request.session['jwt_access_token'] = responseJson['token']
                
                return redirect('../news')
            else:
                context = {'error':"Invalid Data", 'form': form}
                return render(request, 'login.html', context)

    return render(request, 'register.html', {'form': form})


# news view page for logged in users
def NewsPage(request):
    if 'jwt_access_token' not in request.session: ##Check if a token is present or not. Redirect if not
        return redirect('../login')
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    if request.method == 'POST':
        form = SearchBar(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"].split(' ', 1)[0] #if user enters two words then take first one

            reqData = {"keyword":keyword}
            headers = {"Authorization" : "Bearer "+request.session['jwt_access_token']}
            responseData = apiCall(const.GET, 'news/', keyword, headers)

            context = {'form': form, "newslst":responseData.json()}
            return render(request, 'newspage.html', context)
    else:
        form = SearchBar()
    
    return render(request, 'newspage.html', {'form': form})


# logout view
def logoutPage(request):
    logout(request)
 
    return redirect('../login')
