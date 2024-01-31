from django.contrib import admin
from .models import Course,Chapter,Topic,Heading,SubHeading,Code,Image,Post,Content
# Register your models here.
admin.site.register([Course,Chapter,Topic,Heading,SubHeading,Code,Image,Post,Content])