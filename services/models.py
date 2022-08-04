from unittest.util import _MAX_LENGTH
from . choices import *
from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


from django.db.models.signals import post_save,m2m_changed


# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    email = models.EmailField()
    dept = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to = 'profile_pic/',blank = True)
    role = models.CharField(max_length = 200,choices = ROLE_CHOICES,blank = True)
    team = models.CharField(max_length = 200,choices = TEAM_CHOICES,blank = True)
    slug = AutoSlugField(populate_from='user',unique = True)
    Skillset = TaggableManager(blank=True)
    description = models.TextField()
    awards = models.CharField(max_length=500)
    def __str__(self):
        return self.user.email
class Work(models.Model):
    title = models.CharField(max_length = 200)
    description = HTMLField()
    date_of_creation = models.DateTimeField(auto_now_add = True)
    deadline = models.DateField(editable=True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)
    assigned_to = models.ManyToManyField(User,related_name = "assigned")
    slug = AutoSlugField(populate_from='title',unique = True)
    def __str__(self):
        return self.title
class Progress(models.Model):
    assigned_work = models.ForeignKey(Work,on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    progress = models.CharField(max_length = 200,choices = PROGRESS_CHOICES)
    reference = models.URLField(max_length = 300,help_text = "Upload Your Work Via Link",null = True,blank = True)
    def __str__(self):
        return self.assigned_work.title
    class Meta:
        verbose_name = "Progress"
        verbose_name_plural = "Progress"
@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance,role = "Member")
        instance.profile.save()
@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
@receiver(m2m_changed,sender = Work.assigned_to.through)
def create_progress(sender,instance,**kwargs):
    for user in instance.assigned_to.all():
        progress = Progress(user = user,assigned_work = instance,progress = "ASSIGNED")
        progress.save()

    