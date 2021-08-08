from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Faculty)



class AttendenceDataAdmin(admin.ModelAdmin):
    list_display = ('Faculty_Name','Student_ID','date','time','branch','year','section','period','status')
    search_fields = ('status','section','date')

    list_per_page = 50
    list_filter=['status','section','date','time']

admin.site.register(Attendence,AttendenceDataAdmin)




class StudentDataAdmin(admin.ModelAdmin):
    list_display = ('firstname','lastname','registration_id','branch','year','section','profile_pic')
    search_fields = ('registration_id','firstname')

    list_per_page = 50
    list_filter=['branch','section','year']
    
admin.site.register(Student,StudentDataAdmin)