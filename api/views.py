from rest_framework import generics
from courses.models import Course,Chapter,Topic,Post
from api.serializer import CourseSerializer,ChapterSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
class CourseView(generics.ListAPIView):

    def get_queryset(self):
        return Course.objects.all()
    def get(self,request,format=None):
        serializer = CourseSerializer(self.get_queryset(),many=True)
        return Response(serializer.data)

class CourseDetailsView(generics.RetrieveAPIView):
    def get_object(self,pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Http404

    def get(self, request,pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)


@api_view(['GET',])
def chapterList(request,course_id):
    return Response(ChapterSerializer(Chapter.objects.filter(course_id=course_id),many=True).data)

def post(id):
    posts = Post.objects.filter(topic_id=id)
    data = list()
    for p in posts:
        if p.content_object.type()=='image':
            mypost['image'] = p.content_object.image.url
        else:
            mypost = model_to_dict(p.content_object)
        mypost['type'] = p.content_object.type()
        data.append(mypost)
    return data



def topics(id):
    topics = Topic.objects.filter(chapter_id=id)
    topics_list = list()
    for t in topics:
        mydict = dict()
        mydict["id"] = t.ide
        mydict["title"] = t.title
        if t.logo:
            mydict["logo"] = t.logo.url
        else:
            mydict["logo"] = ""
        mydict["chapter"] = t.chapter_id
        mydict["posts"] = post(t.id)
        topics_list.append(mydict)
    return topics_list
def chapterDict(id):
    chapters = Chapter.objects.filter(course_id = id)
    data = list()
    for chapter in chapters:
        data.append({'id': chapter.pk, 'title': chapter.title,'content':topics(chapter.id)})
    return data

def api(request,id):
    result = {}
    c = Course.objects.get(pk=id)
    result["id"] = c.id
    result["course"] = c.course_name
    result["createdAt"] = c.createdAt
    result["chapters"]  = chapterDict(id)
    return JsonResponse(result,safe=False)


