from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

import datetime

class Tag(models.Model):
    name = models.CharField(verbose_name=('Name'), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=('Slug'), unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        pass

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            # Now try to find existing slugs with similar names
            slugs = set(
                self.__class__._default_manager
                .filter(slug__startswith=self.slug)
                .values_list('slug', flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    return super(Tag, self).save(*args, **kwargs)
                i += 1
        else:
            return super(Tag, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('Tag_detail')

    def slugify(self, tag, i=None):
        slug = slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug
    
class Task(models.Model):
    title = models.CharField(max_length=140)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateField(auto_now=True)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=None)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='task_created_by')
    note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField()

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the Task's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Task_detail')

    # Auto-set the Task creation / completed date
    def save(self):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    class Meta:
        ordering = ["priority"]


# class Comment(models.Model):
#     """
#     Not using Django's built-in comments because we want to be able to save
#     a comment and change task details at the same time. Rolling our own since it's easy.
#     """
#     author = models.ForeignKey(User)
#     task = models.ForeignKey(Task)
#     date = models.DateTimeField(default=datetime.datetime.now)
#     body = models.TextField(blank=True)
# 
# #     def snippet(self):
#         # Define here rather than in __str__ so we can use it in the admin list_display
# #         return "{task} - {snippet}...".format(task=self.task, snippet=self.body[:35])
# 
#     def __str__(self):
#         return "{task} - {comment}...".format(task=str(self.task), comment=str(self.body[:30]))
#     
#     class Meta:
#         ordering = ["date"]