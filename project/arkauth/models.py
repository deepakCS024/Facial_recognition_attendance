from django.db import models

# Create your models here.
class Subjects(models.Model):
    subject_name=models.CharField(max_length=500)
    def __str__(self):
        return self.subject_name

class Register(models.Model):
    sno=models.AutoField(primary_key=True)
    usn=models.CharField(max_length=100)
    gender=models.CharField(max_length=150)
    sem=models.EmailField()
    ia=models.CharField(max_length=55)
    marks=models.CharField(max_length=55)
    subject=models.CharField(max_length=100)
    def __str__(self):
        return self.subject