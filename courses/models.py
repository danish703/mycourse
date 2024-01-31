from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete,pre_delete

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100,unique=True)
    courseIcon = models.ImageField(upload_to='courseImages')
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


class Chapter(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course,on_delete=models.RESTRICT)
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='topics/',null=True,blank=True)
    chapter = models.ForeignKey(Chapter,models.RESTRICT)

    def __str__(self):
        return self.title


class Heading(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,default=0)
    def __str__(self):
        return self.title

    def type(self):
        return "Heading"
@receiver(post_save,sender=Topic)
def create_heading(instance,created,**kwargs):
    if created:
        Heading.objects.create(title=instance.title,topic=instance)


class SubHeading(models.Model):
    sub_title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic,models.CASCADE,default=0)
    def __str__(self):
        return self.sub_title

    def type(self):
        return "subheading"


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,default=0)

    def __str__(self):
        return str(self.image)

    def type(self):
        return "image"


class Content(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.content

    def type(self):
        return "content"


class Code(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.content

    def type(self):
        return "code"


class Post(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    topic = models.ForeignKey(Topic,models.RESTRICT,default=None)

    def __str__(self):
        return str(self.content_type)+" | "+str(self.content_object)


@receiver(post_save,sender=Heading)
@receiver(post_save,sender=SubHeading)
@receiver(post_save,sender=Image)
@receiver(post_save,sender=Content)
@receiver(post_save,sender=Code)
def post_create(instance,created,**kwargs):
    if created:
        a = Post(content_object=instance,topic=instance.topic)
        a.save()

@receiver(pre_delete,sender=Heading)
@receiver(pre_delete,sender=SubHeading)
@receiver(pre_delete,sender=Image)
@receiver(pre_delete,sender=Content)
@receiver(pre_delete,sender=Code)
def post_delete(sender,instance,**kwargs):
    try:
        content_type = ContentType.objects.get_for_model(instance.__class__)
        Post.objects.get(content_type=content_type,object_id=instance.id).delete()
    except:
        pass

