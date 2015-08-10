from django.contrib import admin

# Register your models here.
from tohdoh.models import TodoList, TodoItem

admin.site.register(TodoList)
admin.site.register(TodoItem)
