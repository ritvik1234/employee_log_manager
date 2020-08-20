import requests
# payload = {'username': '', 'password': ''}
# payload = {'id' : 2, 'name': 'Ritvik Munjal'}
# r = requests.get('http://127.0.0.1:8000/api/employee/employee/', params = payload)
# dict(r.text)
# payload = {'check_in': '9.00', 'check_out': '17.25', 'brea_k': 1.2, 'date': 3, 'month': 12, 'year': 2021, 'employee_code': '626449f2-3329-417b-be86-941f786db558'}
# r = requests.post('http://127.0.0.1:8000/api/employee/entry/create', data = payload)
# print(r.json())
# r_dict = r.json()
# print(r_dict['employee_code'])
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
payload = {'username': '2017meb1234', 'password': 'sexyboy222'}
r = requests.post('http://127.0.0.1:8000/api/token/', data = payload)
print(r.text)
# print(r.text)
r_dict = r.json()
access = r_dict["access"]
# print(access)

# refresh = r_dict["refresh"]
# headers = {'Authorization': 'Bearer ' + access}

req = requests.get('http://127.0.0.1:8000/api/employee/employee/56', auth = BearerAuth(access))
print(req.text)
# print(req.text)
# r = requests.get('')
# print(r.text)
# print(r_dict["access"])
#HTML PARSER
# r.status_code
# help(r)


#Authentication
# r = request.get(link, auth = ('corey', 'test'))


#Django Variable , Domain Name Rkhega
# Session mei store krao Token. Server side Session
# Request library ke thru, Headers mei pass hoga
# Login : JWT API
# Logout mein manipulate: User Mdo
# Session mei token hataoge

# Password Change: Email
