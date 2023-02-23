from django.db import models

# Create your models here.



class Employee(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sallary = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "Employee"

    def __str__(self):
        # return f"{self.__dict__}"
        return self.name