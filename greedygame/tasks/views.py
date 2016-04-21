from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Task, Tag
from .services import get_query
from django.views.generic.list import ListView
from django.shortcuts import render_to_response
from django.template import RequestContext

class TaskCreate(CreateView):
    model = Task
    fields = ['title','tags','due_date','completed','completed_date','created_by','note','priority']

class TaskUpdate(UpdateView):
    model = Task
    fields = ['title','tags','due_date','completed','completed_date','created_by','note','priority']
    template_name_suffix = '_update'

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('Task_detail')
    
class TaskList(ListView):
    model = Task
    
#     def get_context_data(self, **kwargs):
#         objects = Task.objects.filter(created_by=self.request.user)
#         return objects
    
class TagCreate(CreateView):
    model = Tag
    fields = ['name']

class TagUpdate(UpdateView):
    model = Tag
    fields = ['name']
    template_name_suffix = '_update'

class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('Tag_detail')
    
class TagList(ListView):
    model = Tag
        
def search(request):
    query_string = ''
    task_entries = None
    tag_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        task_query = get_query(query_string, ['title', 'note', 'tags__name'])
        tag_query = get_query(query_string, ['name'])
        
        task_entries = Task.objects.filter(task_query)
        tag_entries = Tag.objects.filter(tag_query)
        

    return render_to_response('tasks/search_result.html',
                              { 'query_string': query_string, 'task_entries': task_entries, 'tag_entries': tag_entries },
                              context_instance=RequestContext(request))