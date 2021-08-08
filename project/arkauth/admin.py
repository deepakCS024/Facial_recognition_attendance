from django.contrib import admin

# Register your models here.
from arkauth.models import Subjects,Register

admin.site.register(Subjects)


class RegisterDataAdmin(admin.ModelAdmin):
    list_display = ('sno','usn','gender','sem','ia','marks','subject')
    search_fields = ('usn','subject')

    list_per_page = 50
    list_filter=['subject','gender','sem','marks']
    
admin.site.register(Register,RegisterDataAdmin)