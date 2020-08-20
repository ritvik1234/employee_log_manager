from django.shortcuts import render
from django.http import HttpResponse
from .forms import Registeration, Register
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect
import requests

### Global Variables
access = 1
user = 1
employee_code = 1
check_in = 1
checkout = 1
date = 1
month = 1
year = 1
brea_k = 1
staff = 0
ide = 1
username = 1
password = 1
user_name = 1
use_r = 0
once = 1


def logout_view(request):
    global use_r
    use_r = 0
    global once
    once = 1
    logout(request)
    return render(request,"logout.html")


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def home(request):
    if use_r:
        return render(request,"afterlogin.html", {'logout': 1, 'staff': staff})
    else:
        return render(request,"index.html", {'status': ''})

def log(request):
    global username
    username = request.POST['username']
    global password
    password = request.POST['password']
    global use_r
    use_r = 1
    print(use_r)
    payload = {'username': username, 'password': password}
    r = requests.post('http://127.0.0.1:8000/api/token/', data = payload)
    r_dict = r.json()
    print(r_dict)
    if len(r_dict) == 1:
        return render(request, "index.html", {'status': r_dict["detail"]})
    else:
        request.session['session_var_name'] = r_dict["access"]
        print(request.session)
        payload = {'username': username}
        req = requests.get('http://127.0.0.1:8000/api/employee/user/', auth = BearerAuth(request.session['session_var_name']), params = payload)
        req_dict = req.json()
        for dic in req_dict:
            diction = dic
        global user
        user = diction["id"]
        global staff
        staff = diction["is_staff"]
        payload = {'username': user}
        req = requests.get('http://127.0.0.1:8000/api/employee/employee/', auth = BearerAuth(request.session['session_var_name']), params = payload)
        r_dict = req.json()
        diction = r_dict[0]
        global employee_code
        employee_code = diction["employee_code"]
        print(employee_code)
        return render(request,"afterlogin.html", {'status_1':'', 'status_2':'', 'status_3':'', 'staff': staff, 'logout': 1})


def checkin(request):
    if use_r:
        global once
        once = 0
        return render(request,'checkin.html', {'logout': 1})
    else:
        return render(request,"index.html", {'status': ''})



def aftercheckin(request):
    global check_in
    check_in = request.POST['checkin']
    check_in = float(check_in)
    d = request.POST['date']
    d = d.split('-')
    global date
    date = int(d[2])
    global month
    month = int(d[1])
    global year
    year = int(d[0])
    if year >= 1999:
        status = f"You have successfully checked-in at {check_in}"
        return render(request, 'afterlogin.html', {'status_1':status, 'status_2':'', 'status_3':'', 'logout': 1})
    else:
        return render(request, 'checkin.html', {'status': 'Enter a valid year'})

def afterbreak(request):
    global brea_k
    brea_k = request.POST['brea_k']
    status = f"You have taken a break of {brea_k} hrs"
    return render(request, 'afterlogin.html', {'status_1':'', 'status_2':status, 'status_3':'', 'logout': 1})

def aftercheckout(request):
    checkout = request.POST['checkout']
    checkout = float(checkout)
    if checkout > check_in:
        payload = {'check_in': check_in, 'brea_k': brea_k, 'check_out': checkout, 'date': date, 'month': month, 'year': year, 'employee_code': employee_code}
        req = requests.post('http://127.0.0.1:8000/api/employee/entry/create', auth = BearerAuth(request.session['session_var_name']), data = payload)
        r_dict = req.json()
        duration = r_dict["duration"]
        status = f"You have successfully checked-out at {checkout}. You worked today for {duration} hours"
        return render(request, 'afterlogin.html', {'status_1':'', 'status_2':'', 'status_3':status, 'logout': 1})
    else:
        return render(request, 'afterlogin.html', {'status_3': 'Checkout should be greater than checkin'})

def checkout(request):
    global once
    once = 0
    return render(request,'checkout.html', {'logout': 1})

def breakk(request):
    global once
    once = 0
    return render(request,'break.html', {'logout': 1})

def salary(request):
    global once
    once = 0
    if staff:
        req = requests.get('http://127.0.0.1:8000/api/employee/salary/', auth = BearerAuth(request.session['session_var_name']))
    else:
        req = requests.get('http://127.0.0.1:8000/api/employee/salary/', auth = BearerAuth(request.session['session_var_name']), params = {'employee_code': employee_code})
    req_dict = req.json()
    return render(request,'salary.html', {'salary_log': req_dict, 'staff': staff, 'logout': 1})

def time(request):
    global once
    once = 0
    if staff:
        req = requests.get('http://127.0.0.1:8000/api/employee/entry/', auth = BearerAuth(request.session['session_var_name']))
    else:
        req = requests.get('http://127.0.0.1:8000/api/employee/entry/', auth = BearerAuth(request.session['session_var_name']), params = {'employee_code': employee_code})
    req_dict = req.json()
    return render(request,'time.html', {'time_log': req_dict, 'staff': staff, 'logout': 1})

def register(request):
        return render(request,'register.html', {'status': '', 'logout': 1})

def create_user(request):
    global user_name
    user_name = request.POST["username"]
    password = request.POST["password"]
    re = request.POST["re-password"]
    if re != password:
        return render(request, 'register.html', {'status': 'Passwords not matching', 'logout': 1})
    else:
        payload = {'username': user_name, 'password': password}
        r = requests.post('http://127.0.0.1:8000/api/employee/user/create', data = payload)
        print(r.status_code)
        r_dict = r.json()
        if r.status_code == 400:
            return render(request, 'register.html', {'status': r_dict, 'logout': 1})
        else:
            payload = {'username': user_name}
            req = requests.get('http://127.0.0.1:8000/api/employee/user/', params = payload)
            req_dict = req.json()
            for dic in req_dict:
                diction = dic
            user = diction["id"]
            payload = {'username': user}
            req = requests.get('http://127.0.0.1:8000/api/employee/employee/', params = payload)
            r_dict = req.json()
            diction = r_dict[0]
            ide = diction["id"]
            print(ide)
            return render(request, 'personal.html', {'logout': 1})

def admin_update(request):
    username = request.POST.get('username')
    return render(request, 'admin_update.html', {'logout': 1})

def admin_delete(request):
    return render(request, 'admin_delete.html', {'logout': 1})

def delete(request):
    user_name = request.POST['username']
    payload = {'username': user_name}
    req = requests.get('http://127.0.0.1:8000/api/employee/user/', params = payload)
    req_dict = req.json()
    if len(req_dict) == 0:
        return render(request, 'admin_delete.html', {'status': 'The username doesnt exist', 'logout': 1})
    else:
        req_dict = req_dict[0]
        ide = req_dict["id"]
        req = requests.delete(f'http://127.0.0.1:8000/api/employee/user/{ide}/delete')
        print(req)
    return render(request, 'afterlogin.html', {'status': 'Successfully deleted user', 'staff': staff, 'logout': 1})

def update_details(request):
    global user_name
    print(user_name)
    user_name = request.POST["username"]
    payload = {'username': user_name}
    req = requests.get('http://127.0.0.1:8000/api/employee/user/', params = payload)
    req_dict = req.json()
    if len(req_dict) == 0:
        return render(request, 'admin_update.html', {'status': 'The username doesnt exist', 'logout': 1})
    else:
        req_dict = req_dict[0]
        user = req_dict["id"]
        payload = {'username': user}
        req = requests.get('http://127.0.0.1:8000/api/employee/employee/', params = payload)
        r_dict = req.json()
        diction = r_dict[0]
        ide = diction["id"]
        print(ide)
        return render(request, 'personal.html', {'logout': 1, 'name': diction["name"], 'email': diction["email"], 'hourly_rate': diction["hourly_rate"]})

def admin_create(request):
    name = request.POST["name"]
    hour = request.POST["hour"]
    email = request.POST["email"]
    payload = {'username': user_name}
    req = requests.get('http://127.0.0.1:8000/api/employee/user/', params = payload)
    req_dict = req.json()
    for dic in req_dict:
        diction = dic
    user = diction["id"]
    payload = {'username': user}
    req = requests.get('http://127.0.0.1:8000/api/employee/employee/', params = payload)
    r_dict = req.json()
    diction = r_dict[0]
    ide = diction["id"]
    print(ide)
    payload = {'name': name, 'hourly_rate': hour, 'email': email}
    req = requests.put(f'http://127.0.0.1:8000/api/employee/employee/{ide}/update', data = payload)
    r_dict = req.json()
    print(r_dict)
    if req.status_code == 400:
        return render(request, 'personal.html',{'status': r_dict, 'logout': 1})
    else:
        return render(request, 'afterlogin.html', {'status': 'The account has been successfully updated/created', 'staff': staff, 'logout': 1} )

def update_success(request):
    name = request.POST["name"]
    hour = request.POST["hour"]
    email = request.POST["email"]
    payload = {'username': user}
    req = requests.get('http://127.0.0.1:8000/api/employee/employee/', auth = BearerAuth(request.session['session_var_name']), params = payload)
    r_dict = req.json()
    diction = r_dict[0]
    global ide
    ide = diction["id"]
    print(ide)
    payload = {'name': name, 'hourly_rate': hour, 'email': email}
    req = requests.put(f'http://127.0.0.1:8000/api/employee/employee/{ide}/update', auth = BearerAuth(request.session['session_var_name']), data = payload)
    r_dict = req.json()
    print(r_dict)
    if req.status_code == 400:
        return render(request, 'update.html',{'status': r_dict, 'logout': 1})
    else:
        return render(request, 'afterlogin.html', {'status': 'Your account has been successfully updated', 'logout': 1})

def update(request):
    print(employee_code)
    req = requests.get('http://127.0.0.1:8000/api/employee/employee/', auth = BearerAuth(request.session['session_var_name']), params = {'employee_code': employee_code})
    req_dict = req.json()
    req_dict = req_dict[0]
    return render(request, 'update.html', {'name': req_dict["name"], 'email': req_dict["email"], 'hourly_rate': req_dict["hourly_rate"], 'logout': 1})

def manpower(request):
    global once
    once = 0
    req = requests.get('http://127.0.0.1:8000/api/employee/manpower/', auth = BearerAuth(request.session['session_var_name']))
    req_dict = req.json()
    return render(request,'manpower.html', {'manpower_log': req_dict, 'logout': 1})

def employees(request):
    global once
    once = 0
    req = requests.get('http://127.0.0.1:8000/api/employee/employee/', auth = BearerAuth(request.session['session_var_name']))
    req_dict = req.json()
    return render(request,'employees.html',{'employee_log': req_dict, 'logout': 1})

