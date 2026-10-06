from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
from .serializers import EmployeeSerializer
import json
from rest_framework.decorators import api_view
from rest_framework.response import responses
from rest_framework import status 

# Create your views here.

def build_response(success, message, status, data=None , error=None):
    response_data={
        'success':success,
        'message':message

    }
    if data is not None:
        response_data['data']= data
    if error is not None:
        response_data['error'] = error
    return JsonResponse(data = response_data , status = status)

@csrf_exempt
@api_view(['GET' ,"POST"])
def employee_list_view(request):
    if request.method=='GET':
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(instance=employee , many=True)
        return build_response(True, "Employee Retrived Successfully ", status=200 , data = serializer.data)
    if request.method=="POST":
        
        serializer = EmployeeSerializer(data=request.data )
        if serializer.is_valid():
            serializer.save()
            return build_response(True,'employee created' , status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return build_response(False , "validtion error" ,status=400, error=serializer.errors )
@csrf_exempt
@api_view(['GET' ,"PUT" , 'PATCH', 'DELETE'])
def employee_details_view(request , employee_id):
    try:
        employee = Employee.objects.get(id = employee_id)
    except Employee.DoesNotExist:
        return build_response(False, 'Employee not Found' , status=404)
    if request.method=="GET":
        serializer = EmployeeSerializer(instance=employee)
        
        return build_response(True , 'Employee Found', status=status.HTTP_200_OK , data = serializer.data)
        
    if request.method=='PUT':
        request_data = json.loads(request.body)
        serializer = EmployeeSerializer(insatnce=employee , data =request_data)
        if serializer.is_valid():
            serializer.save()
            return build_response(True , 'Employee replaced successfully', status=status.HTTP_200_OK , data = serializer.data)
        else:return build_response(False , "vaildation erroe" , status=status.HTTP_400_BAD_REQUEST , errors= serializer.errors)
    
    if request.method=='PATCH':
        request_data = json.loads(request.body)
        serializer = EmployeeSerializer(instance=employee , data =request_data ,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return build_response(True , 'Employee updated successfully',status=status.HTTP_200_OK , data = serializer.data)
       
        else:
            return build_response(False , "vaildation error" , status=status.HTTP_400_BAD_REQUEST , error= serializer.errors)
    
    if request.method=="DELETE":
        employee.delete()
        return build_response(True , 'Employee deleted successfully', status=status.HTTP_200_OK )
    return build_response(False , 'only GET , PUT , PACTH , and DELETE methods are allowed')

