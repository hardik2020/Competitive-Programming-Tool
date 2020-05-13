import operator
from solved_problems.models import Solved_Probelms
from django.shortcuts import render

from bs4 import BeautifulSoup
import requests
from .models import Problems
# from PIL import Image

dict_url = {}
counter = 1

# Initial Problemset page
def problemset(request):
    print("User is",request.user)
    return render(request, 'problemset.html',{"user":request.user})

# Problemset page after applying rating tags
def tags(request):
    global dict_url
    global counter
    counter = 1
    dict_url = {}
    # extracting out the rating from url(GET method)
    range1 = str(request.GET['range1'])
    range2 = str(request.GET['range2'])


    if range1 != "" and range2 != "":
        range1 = int(range1)
        range2 = int(range2)
    else:
        # default ratings in case of empty form submission
        range1 = 800
        range2 = 3500

    # filtering database according to range queries
    obj = Problems.objects.filter(rating__lte=range2).exclude(rating__lt=range1)

    # Inserting each problem in dictionary and passing it to html file to render
    for probs in obj:
        print(probs.name.strip())
        dict_url[counter] = [str(probs.name).strip(),probs.url,probs.rating]
        counter+=1
    #print(dict_url)
    obj = Solved_Probelms.objects.filter(username=request.user)

    attempted = []
    for ques in obj:
        #print(ques.name)
        attempted.append(ques.name.strip())
    print(attempted)
    return render(request, 'tags.html', {'list_url': dict_url.items(),'attempted':attempted,"user":request.user})


