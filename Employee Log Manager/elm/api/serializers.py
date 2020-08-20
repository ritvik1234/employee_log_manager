from rest_framework import serializers
from api.models import ManpowerInvestment, Employees, Salary, EntryLog, User
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
class ManpowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManpowerInvestment
        fields = ['id', 'investment', 'month', 'year']

class EmployeesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username', read_only=True)
    class Meta:
        model = Employees
        fields = ['id', 'employee_code', 'name', 'email', 'username', 'hourly_rate']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style = {'input_type': 'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff']

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return make_password(data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff']

class EmployeesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['employee_code', 'name', 'email', 'username','hourly_rate']

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'employee_code', 'month', 'year', 'salary', 'duration']

class EntryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryLog
        fields = ['id', 'employee_code', 'check_in', 'check_out', 'brea_k', 'duration', 'date', 'month', 'year']
