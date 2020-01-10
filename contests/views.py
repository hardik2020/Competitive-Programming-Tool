from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from PIL import Image

def contest(request):
    cf = 'https://codeforces.com'
    # query = {'q': 'Forest', 'order': 'popular', 'min_width': '800', 'min_height': '600'}
    # params = "writing-first-c-program-hello-world-example"
    counter=1
    dict_url={}
    req = requests.get(cf + '/problemset',)
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", {"class": "pagination"})
    result = results.findAll("a")
    total = result[-2].text
    total = int(total)
    print(total)
    total=2
    x = 1
    save = ""

    while (x <= total):

        page = 'https://codeforces.com/problemset/page/' + str(x)
        params = {'tags':'1500-1600'}
        req = requests.get(page,params=params)
        soup = BeautifulSoup(req.text, "html.parser")
        # print(soup.prettify())
        results = soup.find("table", {"class": "problems"})
        links = results.findAll("tr")
        for item in links:
            flag = False
            item_text = item.findAll("td")
            for td in item_text:
                find_div = td.find("div")
                if find_div is not None:
                    url = find_div.find("a")
                    # print(url)
                    url1 = url.attrs["href"]
                    text_url = url.text
                    str1 = cf + url1

                    # print(url1,text_url,1500)
                    #print(str1)

                    dict_url [counter] =str1
                    counter+=1
                    #list_url.append(c)
                    # print()
                    break

        x = x + 1

    return render(request,'contest.html',{'list_url': dict_url.items()})
