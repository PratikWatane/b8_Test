import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import Employee
from .serilizer import EmployeeSerilizer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import io
# Create your views here.


def get_single_data(request, id):
    emp_obj = Employee.objects.get(id = id)        # query object
    # print(emp_obj)
    python_data = EmployeeSerilizer(emp_obj)       # query object to python dict
    # print(python_data.data)
    jason_data = JSONRenderer().render(python_data.data)     # python dict to bytes data
    # print(jason_data)
    # jason_data =  json.dumps(python_data)
    # print(jason_data)
    # bytes_data = emp_obj.__dict__.pop("_state")
    # print(bytes_data)
    # data_obj = emp_obj.__dict__.pop("_state")
    # print(data_obj)
    # data = json.dumps(emp_obj.__dict__)
    # return HttpResponse("success")
    # return HttpResponse(data)

    return HttpResponse(jason_data, content_type= "application/json")


def get_all_data(request):
    emp_object = Employee.objects.all()
    # print(emp_object)
    python_dict = EmployeeSerilizer( emp_object, many = True)
    # print(python_dict.data)
    json_data = JSONRenderer().render(python_dict.data)
    return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def create_student(request):
    if request.method == "POST":
        bytes_data = request.body          # data from postman body
        # jason_data = JSONParser().parse(bytes_data)
        # print(jason_data)
        # print(bytes_data) 
        my_json = bytes_data.decode('utf8').replace("'", '"')          # bytes data to string
        # print(type(my_json))
        python_dict = json.loads(my_json)              # string to python to dict
        # print(python_dict)
        ser = EmployeeSerilizer(data=python_dict)
        # print(ser)
        if ser.is_valid():
            # print(ser)
            data = ser.save()   # query set object
            # print(data.__dict__)
            data.__dict__.pop("_state")
            jason_msg = json.dumps(data.__dict__)   # here we convert data dict to bytes data
            # print(jason_msg)
        # msg_dict = {"msg" : "Record store successfuly"}
        # jason_data = json.dumps(msg_dict)
        # return HttpResponse("success")
        return HttpResponse(jason_msg, content_type="application/json", status = status.HTTP_201_CREATED)
    else:
        msg_data = {"msg": "Only post method allowed"}
        json_data = json.dumps(msg_data)
        return HttpResponse(json_data, content_type = "application", status = status.HTTP_405_METHOD_NOT_ALLOWED)
@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])           # we access the decorator @api_view(): pass the list it import rest_framework.decorators
def all_opeartion(requset):
    # print(requset.method)
    if requset.method == "GET":    # it is used to fetch single or all record from data base
        inp_data = requset.body    # client side data that is the form json byte
        stream = io.BytesIO(inp_data)
        py_data = JSONParser().parse(stream)        # json pasrse is used to convert into python dict
        eid = py_data.get("id")                     # we fetch single id from python dict to fetch the data from data base using id
        if eid:
            emp_obj =  Employee.objects.get(id=eid)  # here the provide or client user input id then fetch appropriate data
            emp_dict = EmployeeSerilizer(emp_obj)    # now to dict to serlizer coz complex data stored into data 
            emp_json = JSONRenderer().render(emp_dict.data)
            # return JsonResponse(emp_dict ) 
            return HttpResponse(emp_json, content_type="application/json")

        em_all_data = Employee.objects.all()
        emp_all_dict = EmployeeSerilizer(em_all_data, many = True)  # it convert all data into python dict thats y many = true
        # json_emp_all = JSONRenderer().render(emp_all_dict.data)
        # return HttpResponse(json_emp_all, content_type = "application/json") 
        return JsonResponse(emp_all_dict, safe=False) # it takes the python dict and convert into json

        # print(py_data)
        # print(py_data.id)
        # print(type(py_data))
        # id1 = py_data(id)
        # print(id1)
        # return JsonResponse({"msg" : "Success"})
    elif requset.method == "POST":
        
        inp_data = requset.body
        stream = io.BytesIO(inp_data)
        py_data = JSONParser().parse(stream)
        emp_ser = EmployeeSerilizer(data=py_data)
        if emp_ser.is_valid():   # check validation then raise validation error
            data = emp_ser.save()
            data.__dict__.pop("_state")
            json_msg = json.dumps(data.__dict__)
            return HttpResponse(json_msg, content_type = "application/json")
        else:
            return JsonResponse(emp_ser.errors)   # it used for validation to return error
            # error_msg = {"msg": "Invalid json data"}
            # json_data = json.dumps(error_msg)
            # return HttpResponse(json_data, content_type="application/json")
    
    elif requset.method == "PUT":
        inp_data = requset.body
        stream = io.BytesIO(inp_data)
        py_data = JSONParser().parse(stream)
        
        eid = py_data.get("id")
        emp_data = Employee.objects.get(id = eid)
        ser = EmployeeSerilizer(instance=emp_data,data=py_data)  # here we provide two parameter
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            json_msg = json.dumps(data.__dict__)
            return HttpResponse(json_msg, content_type = "application/json", status = status.HTTP_200_OK)
        else:
            return JsonResponse({"errors" : ser.errors})
        return JsonResponse({"msg" : "Success"})
        
        
        


    elif requset.method == "PATCH":
        inp_data = requset.body
        # print(inp_data)
        stream = io.BytesIO(inp_data)
        # print(stream.name)
        py_dict = JSONParser().parse(stream) 
        '''another way to json to python dict'''
        # my_json = inp_data.decode('utf8').replace("'", '"')
        # py_dict = json.loads(my_json)
        
        eid = py_dict.get("id")
        # print(eid)
        emp_data = Employee.objects.get(id=eid)
        # print(emp_data)
        ser = EmployeeSerilizer(instance=emp_data,data=py_dict, partial = True)
        print(type(ser))
        print(ser)
        if ser.is_valid():
            data = ser.save()   # it called to the update method
            data.__dict__.pop("_state")
            json_data = json.dumps(data.__dict__)
            return HttpResponse(json_data, content_type = "application/json", status= status.HTTP_200_OK)
        else:
            json_msg = {"errors": ser.errors}

    elif requset.method == "DELETE":
        inp_data = requset.body
        stream = io.BytesIO(inp_data)
        py_data = JSONParser().parse(stream)
        # print(py_data)
        eid = py_data.get("id")
        emp = Employee.objects.get(id=eid)
        # print(emp)
        
        # print(eid)
        # print(emp_data)
        emp.delete()
        error_msg = {"msg": "Invalid json data"}
        json_data = json.dumps(error_msg)
        return HttpResponse(json_data,content_type = "application/json",status=status.HTTP_204_NO_CONTENT)
        # return HttpResponse("success")
