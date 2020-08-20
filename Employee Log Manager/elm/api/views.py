from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models
from api.models import ManpowerInvestment, EntryLog, Employees, Salary
from django.contrib.auth.models import User
from api.serializers import ManpowerSerializer, EntryLogSerializer, EmployeesSerializer, SalarySerializer, EmployeesCreateSerializer, UserSerializer, UserCreateSerializer
from rest_framework import generics
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

class EntryLogFilter(filters.FilterSet):

    class Meta:
        model = EntryLog
        fields = {
        'employee_code' : ['exact']
        }


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
        'username': ['exact'],
        'id': ['exact'],}

class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employees
        fields = {
        'username': ['exact'],
        'employee_code': ['exact'],
        }

class SalaryFilter(filters.FilterSet):

    class Meta:
        model = Salary
        fields = {
        'employee_code': ['exact'],
        }

class ManpowerFilter(filters.FilterSet):

    class Meta:
        model = ManpowerInvestment
        fields = {
        'investment': ['lte', 'gte', 'exact'],
        'month': ['exact', 'lte'],
        'year': ['exact']
        }

class ManpowerListAPIView(ListAPIView):
    queryset = ManpowerInvestment.objects.all()
    serializer_class = ManpowerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ManpowerFilter
    ordering_fields = ('investment', 'month', 'year')
    permission_class = [IsAuthenticated]

class ManpowerRetrieveAPIVIew(RetrieveAPIView):
    queryset = ManpowerInvestment.objects.all()
    serializer_class = ManpowerSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class ManpowerUpdateAPIVIew(UpdateAPIView):
    queryset = ManpowerInvestment.objects.all()
    serializer_class = ManpowerSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class ManpowerDestroyAPIVIew(DestroyAPIView):
    queryset = ManpowerInvestment.objects.all()
    serializer_class = ManpowerSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class ManpowerCreateAPIVIew(CreateAPIView):
    queryset = ManpowerInvestment.objects.all()
    serializer_class = ManpowerSerializer
    permission_class = [IsAuthenticated]

class EntryLogListAPIView(ListAPIView):
    queryset = EntryLog.objects.all()
    serializer_class = EntryLogSerializer
    filterset_class = EntryLogFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('check_in', 'check_out', 'brea_k', 'duration', 'date', 'month', 'year')
    permission_class = [IsAuthenticated]

class EntryLogRetrieveAPIVIew(RetrieveAPIView):
    queryset = EntryLog.objects.all()
    serializer_class = EntryLogSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class EntryLogUpdateAPIVIew(UpdateAPIView):
    queryset = EntryLog.objects.all()
    serializer_class = EntryLogSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class EntryLogDestroyAPIVIew(DestroyAPIView):
    queryset = EntryLog.objects.all()
    serializer_class = EntryLogSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class EntryLogCreateAPIVIew(CreateAPIView):
    queryset = EntryLog.objects.all()
    serializer_class = EntryLogSerializer
    permission_class = [IsAuthenticated]
    def post(self, request):
        request.data._mutable = True
        duration = float(float(request.data.get('check_out')) - float(request.data.get('check_in')) - float(request.data.get('brea_k')))
        dur = duration - int(duration)
        dur = dur - 0.6
        duration = round(duration, 3)
        if dur > 0:
            duration = int(duration) + 1 + dur
            duration = round(duration, 3)
        request.data['duration'] = duration
        emp = Employees.objects.get(employee_code = request.data['employee_code'])
        hourly_rate = emp.hourly_rate
        ans = Salary.objects.filter(employee_code = emp).filter(month = request.data.get('month')).filter(year = request.data.get('year'))
        ans = list(ans)
        print(ans)
        if ans:
            query = Salary.objects.filter(employee_code = emp).filter(month = request.data.get('month')).filter(year = request.data.get('year'))
            num = query.values('id')
            num = list(num)
            num = dict(num[0])
            num = int(num.get("id"))
            t = Salary.objects.get(id = num)
            t.duration = t.duration + duration
            t.duration = round(t.duration, 3)
            duration = t.duration
            t.save()
        if duration <= 192:
            entry = Salary.objects.update_or_create(employee_code = Employees.objects.get(employee_code = request.data['employee_code']), month = request.data.get('month'), year = request.data.get('year'), defaults = dict(
                salary = duration*hourly_rate, duration = duration ))
            investment = duration*hourly_rate
        elif duration > 192 and duration <= 250:
            entry = Salary.objects.update_or_create(employee_code = Employees.objects.get(employee_code = request.data['employee_code']), month = request.data.get('month'), year = request.data.get('year'), defaults = dict(
                salary = 192*hourly_rate + (duration-192)*hourly_rate*1.5, duration = duration))
            investment = 192*hourly_rate + (duration-192)*hourly_rate*1.5
        elif duration > 250:
            entry = Salary.objects.update_or_create(employee_code = Employees.objects.get(employee_code = request.data['employee_code']), month = request.data.get('month'), year = request.data.get('year'), defaults = dict(
                salary = 192*hourly_rate + 58*hourly_rate*1.5 + (duration - 250)*2*hourly_rate, duration = duration))
            investment = 192*hourly_rate + 58*hourly_rate*1.5 + (duration - 250)*2*hourly_rate
        ans = ManpowerInvestment.objects.filter(month = request.data.get('month')).filter(year = request.data.get('year'))
        ans = list(ans)
        print(ans)
        if ans:
            query = ManpowerInvestment.objects.filter(month = request.data.get('month')).filter(year = request.data.get('year'))
            num = query.values('id')
            num = list(num)
            num = dict(num[0])
            num = int(num.get("id"))
            t = ManpowerInvestment.objects.get(id = num)
            t.investment = t.investment + investment
            investment = t.investment
            t.save()
        man = ManpowerInvestment.objects.update_or_create(month = request.data.get('month'), year = request.data.get('year'), defaults = dict(investment = investment))
        return self.create(request)

class EmployeesListAPIView(ListAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    filterset_class = EmployeeFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('username', 'name', 'email', 'hourly_rate')
    permission_class = [IsAuthenticated]

class EmployeesRetrieveAPIVIew(RetrieveAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class EmployeesUpdateAPIVIew(UpdateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class EmployeesDestroyAPIVIew(DestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class EmployeesCreateAPIVIew(CreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesCreateSerializer
    permission_class = [IsAuthenticated]

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_class = [IsAuthenticated]

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('username', 'id')
    permission_class = [IsAuthenticated]

class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class SalaryListAPIView(ListAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    filterset_class = SalaryFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('duration', 'month', 'year', 'salary')
    permission_class = [IsAuthenticated]

class SalaryRetrieveAPIVIew(RetrieveAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class SalaryUpdateAPIVIew(UpdateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class SalaryDestroyAPIVIew(DestroyAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    lookup_field = 'id'
    permission_class = [IsAuthenticated]

class SalaryCreateAPIVIew(CreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_class = [IsAuthenticated]

    def post(self, request):
        ans = ManpowerInvestment.objects.filter(month = request.data.get('month')).filter(year = request.data.get('year'))
        ans = list(ans)
        investment = request.data.get('salary')
        if ans:
            query = ManpowerInvestment.objects.filter(month = request.data.get('month')).filter(year = request.data.get('year'))
            num = query.values('id')
            num = list(num)
            num = dict(num[0])
            num = int(num.get("id"))
            t = ManpowerInvestment.objects.get(id = num)
            t.investment = t.investment + investment
            investment = t.investment
            t.save()
        man = ManpowerInvestment.objects.update_or_create(month = request.data.get('month'), year = request.data.get('year'), defaults = dict(investment = investment))

        return self.create(request)
