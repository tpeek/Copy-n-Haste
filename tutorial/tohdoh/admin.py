from django.contrib import admin

# Register your models here.
from django.contrib import admin
from todo.models import TodoList, TodoItem

admin.site.register(TodoList)
admin.site.register(TodoItem)
