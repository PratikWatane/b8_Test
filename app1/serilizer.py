from django.shortcuts import HttpResponse
from rest_framework import serializers
from .models import Employee


def name_start_with_b(value):
    if value[0].lower() != "b":
        return serializers.ValidationError("name should be start with alphabet b ")
    return value


class EmployeeSerilizer(serializers.Serializer):
    # id = serializers.IntegerField()
    name = serializers.CharField(max_length= 100, validators = [name_start_with_b])
    age = serializers.IntegerField()
    sallary = serializers.CharField(max_length=100)
    company = serializers.CharField(max_length=100)
    designation = serializers.CharField(max_length=100)
    # is_active = serializers.BooleanField()



# def create(self, validated_data):
#         # print("in data", validated_data)#  # in data {'name': 'shashank', 'age': 25, 'marks': 45, 'addr': 'pune'}
#                                         # kwargs coz we fetch the dictionary and store into data
#         emp = Employee.objects.create(**validated_data)
#         # name = Student(name=validated_data.get("name"))  # single data store
#         return emp

# def create(self, validated_data):
#       print(validated_data)
#     #   emp = Employee.objects.create(**validated_data)
#     #   return emp
# def create(self,validated_data):
#         return Employee.objects.create(**validated_data)
    
                     

    def create(self, validated_data):
        '''It is used to store data in database and save() call from view '''
        return Employee.objects.create(**validated_data)          # employee.objects.create() : it mapped serilizer data and store into database 
                                                                  # validated data in the form of key- value form
    
    def update(self, instance, validated_data):   # update method has two argument
                                                  # instance : it  is from of complex data
                                                  # validated data : it is user data in the form of key-value arguments
        '''it is used to update the single fields as well as all field
           it excuted when save () call'''
        # return super().update(instance, validated_data)
        # print("in update method")
        # print(instance)# {'_state': <django.db.models.base.ModelState object at 0x000001CB4900BD30>, 'id': 13, 'name': 'prasanna Watane', 'age': 30, 'sallary': '45000', 'company': 'infosys', 'designation': 'tester', 'is_active': True}
        # print(validated_data) # {'name': 'prasanna Watane'}
        # print(instance.name)
        # print(validated_data.get("name"))
        # print(validated_data.get("sallary"))
        instance.name = validated_data.get("name", instance.name)       # get(): it is two value "name": from user and instance.name from database 
        # print(instance.name)
        instance.age = validated_data.get("age", instance.age)
        # print(instance.age)
        instance.sallary = validated_data.get("sallary", instance.sallary)
        # print(instance.sallary)
        instance.company = validated_data.get("company", instance.company)
        # print(instance.company)
        instance.designation = validated_data.get("designation", instance.designation)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        # print(instance.__dict__)
        return instance
        # return HttpResponse("message")
        # field level validation
    def validate_name(self,value):
        '''add validation to name'''
        # print(value)
        if 'a' not in value.lower():
            raise serializers.ValidationError("Name doesn't have alphabet a")
        return value
    def validate_age(self,value):
        '''add validation to age'''
        print(value)
        if value >= 60:
            raise serializers.ValidationError("Age should be below 50")
        return value
    
    # object level validation
    def validate(self, data):
        if (data.get("address")!= "Pune" and (not data.get("name").isalpha())):
            raise serializers.ValidationError("City should be Pune and name should be alphabetical")
        return data