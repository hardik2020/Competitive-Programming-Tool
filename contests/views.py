from django.contrib.auth import logout,authenticate,login
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.models import User


dict_url = {}
dict_contests = {}
dict_contests_cc = {}
counter = 1
message = ""


def registration(request):
    global message
    message = ""
    print(message)
    context = {
        "message": message
    }
    return render(request,'register.html',context)

def register(request):
    print("here")
    global message
    message = ""
    name = request.POST["username"]
    password = request.POST["pass"]
    confirm = request.POST["confirm"]
    context = {
        "message": message
    }

    if password != confirm:
        context["message"] = "Invalid password confirmation"
        message = "Invalid password confirmation"
        print(message)
        return render(request,'register.html',context)

    else:
        user = User.objects.create_user(username=name,password=password)
        if user is None:
            context["message"] = "Invalid Password"
            message = "Invalid Password"
            print(message)
            return render(request, 'register.html', context)
        user.is_staff = False
        user.save()
        #login(request,user)
        context["message"] = ""
        message = ""
        return render(request,'home.html',context)


def login_view(request):
    global message
    print(request.user)
    name = request.POST["username"]
    password = request.POST["pass"]
    user = authenticate(username=name, password=password)
    if user is not None and user.is_active:

        login(request, user)
        message = ""

        return render(request, 'problemset.html')

    else:
        message = "Invalid credentials"
        return HttpResponseRedirect(reverse('home'))

def logout_view(request):
    global message
    message = ""
    print(message)
    context = {
        "message": message
    }
    logout(request)
    return render(request, 'home.html', context)
def home(request):
    #logout(request)
    global message
    print(message)
    context = {
        "message" : message
    }
    return render(request, 'home.html',context)

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
                print(time)
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



