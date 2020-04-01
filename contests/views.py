from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# from PIL import Image

dict_url = {}
dict_contests = {}
dict_contests_cc = {}
counter = 1


def home(request):
    return render(request, 'home.html')


def contests(request):
    req = requests.get('https://codeforces.com' + '/contests')
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", {"class": "datatable"})
    result = results.find("table")
    links = results.findAll("tr")
    count = 0
    counter1 = 1
    for item in links:
        item_text = item.findAll("td")
        if item_text is not None:
            count = 0
            name = ""
            time = ""
            length =0

            for contest_info in item_text:
                if count == 0:
                    name = contest_info.text
                    #print(name)
                    count += 1
                    continue
                if count == 1:
                    # time_info = contest_info.find("a")
                    # if time_info is not None:
                    #     time = time_info.text

                    count += 1
                    continue
                if count == 2:
                    time_info = contest_info.find("a")
                    time = time_info.text
                    #print(time)
                    count += 1
                    continue
                if count == 3:
                    length = contest_info.text
                    #print(length)
                    count += 1
                    continue
            link_contests = "https://codeforces.com/contests"
            if name is not None and time is not None and length!=0:
                tuple = [name, time, length, link_contests]
                dict_contests[counter1] = tuple
                counter1 += 1


    dict_contests_cc = codechef_contests(request)

    return render(request, 'contests.html', {'list_url': dict_contests.items(),'list_url_cc':dict_contests_cc.items()})

def codechef_contests(request):
    req = requests.get('https://www.codechef.com/contests')
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.findAll("table", {"class": "dataTable"})
    # future contests only
    count = 0
    counter2 = 1
    for table_data in results:
        if count == 0:
            count += 1
            continue
        if count == 1:
            name = ""
            url1 = ""
            start_time = ""
            end_time = ""
            table_columns = table_data.findAll("tr")
            for all_tr in table_columns:

                table_col_td = all_tr.findAll("td")
                for table_content in table_col_td:
                    link_url = table_content.find("a")
                    if link_url is not None:
                        url1 = link_url.attrs["href"]
                        name = link_url.text
                        print("here",name)
                        break


                time = all_tr.find("td", {"class": "start_date"})
                if time is not None:
                    start_time = time.text
                else:
                    start_time = None
                print(start_time)
                time = all_tr.find("td", {"class": "end_date"})
                if time is not None:
                    end_time = time.text
                else:
                    end_time = None
                print(end_time)
                if name is not None and start_time is not None and end_time is not None :
                    tuple = [name, url1, start_time, end_time]
                    print(tuple)
                    dict_contests_cc[counter2] = tuple
                    counter2 +=1
                    count +=1
                       
    return dict_contests_cc



