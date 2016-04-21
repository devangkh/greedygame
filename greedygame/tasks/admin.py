from django.contrib import admin
from tasks.models import Tag, Task

# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    search_fields = ['title', 'note', 'priority']
    list_filter = ['priority']
    pass

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(Task, TasksAdmin)
