# Not so useful code was useful at just initial stage to insert all problems in database
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Problems
# from PIL import Image

dict_url = {}
counter = 1
def problemset(request):
    return render(request, 'problemset.html')


def tags(request):
    global dict_url
    global counter
    counter = 1
    dict_url = {}
    range1 = str(request.GET['range1'])
    range2 = str(request.GET['range2'])
    #print("ranges are",range1, range2)
    if range1 != "" and range2 != "":
        range1 = int(range1)
        range2 = int(range2)
    else:
        range1 = 800
        range2 = 3500
    tags_str = str(range1) + "-" + str(range2)
    #print(tags_str)

    problemset_codeforces(request, tags_str)
    problemset_codechef(request, range1, range2)
    return render(request, 'tags.html', {'list_url': dict_url.items()})


def problemset_codeforces(request, tags_str):
    global dict_url
    global counter
    cf = 'https://codeforces.com'
    params = {'tags': tags_str}
    req = requests.get(cf + '/problemset',params=params )
    print(req.url)
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", {"class": "pagination"})
    print(results)
    if results!=None:
        result = results.findAll("a")
        total = result[-2].text
    else:
        total =1
    total = int(total)
    print(total)
    #total = 1
    x = 1
    save = ""

    while (x <= total):

        page = 'https://codeforces.com/problemset/page/' + str(x)
        params = {'tags': tags_str}
        req = requests.get(page, params=params)
        # print(req.url)
        soup = BeautifulSoup(req.text, "html.parser")
        # print(soup.prettify())
        results = soup.find("table", {"class": "problems"})
        links = results.findAll("tr")
        for item in links:
            item_text = item.findAll("td")
            name = ""
            new_url = ""
            rating = 0

            for td in item_text:
                find_div = td.find("div")
                find_span = td.find('span', {"class": "ProblemRating"})
                if find_div is not None:
                    url = find_div.find("a")
                    url1 = url.attrs["href"]
                    name = url.text

                    new_url = cf + url1
                if find_span is not None:
                    rating = find_span.text

            if name is not None and new_url is not None and rating is not None and rating != 0:
                r = requests.get(new_url)
                new_url = r.url
                tuple = [name, new_url, rating]
                Problems.objects.create(name=name,url=new_url,rating=rating)
                dict_url[counter] = tuple
                counter += 1

        x = x + 1

    # return render(request,'contest.html',{'list_url': dict_url.items()})


def problemset_codechef(request, range1, range2):
    #print("here")
    range1 = int(range1)
    range2 = int(range2)
    global dict_url
    cc = 'https://codechef.com'
    global counter
    start = ""
    end = ""
    start_index = 0
    end_index = 0
    ranges = [[800,1300],[1301,1600],[1601,2200],[2201,3500]]
    if range1 >= 800 and range1 <= 1300:
        start = "school"
        start_index = 1
    elif range1 > 1300 and range1 <= 1600:
        start = "easy"
        start_index = 2
    elif range1 > 1600 and range1 <= 2200:
        start = "medium"
        start_index = 3
    else:
        start = "hard"
        start_index = 4
    if range2 >= 800 and range2 <= 1300:
        end = "school"
        end_index = 1
    elif range2 > 1300 and range2 <= 1600:
        end = "easy"
        end_index = 2
    elif range2 > 1600 and range2 <= 2200:
        end = "medium"
        end_index = 3
    else:
        end = "hard"
        end_index = 4

    while start_index <= end_index:
        #print("inside loop")
        page = 'https://codechef.com/problems/' + start
        #print(page)
        req = requests.get(page)
        # print("here")
        # print(req.url)
        soup = BeautifulSoup(req.text, "html.parser")
        # print(soup.prettify())
        results = soup.find("table", {"class": "dataTable"})
        #print(results)
        links = results.findAll("tr")
        for item in links:

            item_text = item.findAll("td")
            name = ""
            new_url = ""
            rating = 0
            itr = 0
            for td in item_text:

                itr += 1
                find_div = td.find("div", {"class": "problemname"})
                find_a = td.find('a')
                if find_div is not None:
                    url = find_div.find("a")
                    # print(url)
                    url1 = url.attrs["href"]
                    name = url.text

                    new_url = cc + url1

                    # print(url1,text_url,1500)
                    # print(new_url)

                    # dict_url [counter] =str1

                    # list_url.append(c)
                    # print()
                if itr == 4:

                    accuracy = find_a.text
                    accuracy = 100 - float(accuracy)
                    rating = ranges[start_index-1][0] + ((ranges[start_index-1][1] - ranges[start_index-1][0]) * accuracy) / 100
                    rating = int(rating)
                    #print(rating)

            if rating >= range1 and rating <= range2:
                #print("in")
                r = requests.get(new_url)
                new_url = r.url
                tuple = [name, new_url, rating]
                # print(new_url)
                Problems.objects.create(name=name, url=new_url, rating=rating)
                dict_url[counter] = tuple
                counter += 1


        if start == 'school':
            start = 'easy'
        elif start == 'easy':
            start = 'medium'
        elif start == 'medium':
            start = 'hard'
        start_index += 1