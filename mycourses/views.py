from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from courses.models import Course,Chapter,Topic,Post,Heading,SubHeading,Content,Code,Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

def signin(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            return redirect('home')
        return redirect('login')

@login_required(login_url='login')
def home(request):
    courses = Course.objects.all()
    return render(request,'home.html',{'courses':courses})


@login_required(login_url='login')
def chapterList(request,course_id):
    chapter = Chapter.objects.filter(course_id=course_id)
    course = Course.objects.get(pk=course_id)
    context = {
        'chapters':chapter,
        'course':course
    }
    return render(request,'chapters.html',context)
@login_required(login_url='login')
def saveTopics(request):
    if request.method=='POST':
        topics = request.POST.get('topic')
        img = request.FILES.get('image')
        chapter = request.POST.get('chapter')
        t = Topic(title=topics,chapter_id=chapter,logo=img)
        t.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def addChapter(request):
    if request.method=='POST':
        chapter = request.POST.get('chapter')
        course = request.POST.get('course')
        position = int(request.POST.get('position'))+1
        newChapter = Chapter(title=chapter,course_id=course,position=position)
        newChapter.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def subHeadingSaving(request):
    if request.method=="POST":
        h = request.POST.get('subheading')
        t = request.POST.get('topic')
        s = SubHeading(sub_title=h,topic_id=t)
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def contentSaving(request):
    if request.method=="POST":
        h = request.POST.get('content')
        t = request.POST.get('topic')
        s = Content(content=h,topic_id=t)
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def codeSaving(request):
    if request.method=="POST":
        h = request.POST.get('code')
        t = request.POST.get('topic')
        s = Code(content=h,topic_id=t)
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def imageSaving(request):
    if request.method=="POST":
        h = request.FILES.get('image')
        t = request.POST.get('topic')
        s = Image(image=h,topic_id=t)
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def post(request,topic_id):
    mypost = Post.objects.filter(topic_id=topic_id)
    content = {
        'posts':mypost,
        'topic':topic_id,
        'title': mypost[0].content_object.title
    }
    return render(request,'topic.html',content)

#update views
@login_required(login_url='login')
def updateSubheading(request):
    if request.method=="POST":
        h = request.POST.get('subheading')
        t = request.POST.get('id')
        s = SubHeading.objects.get(pk=t)
        s.sub_title = h
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def updateContent(request):
    if request.method=="POST":
        h = request.POST.get('content')
        t = request.POST.get('id')
        s = Content.objects.get(pk=t)
        s.content = h
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def imageUpdateSaving(request):
    if request.method=="POST":
        h = request.FILES.get('image')
        t = request.POST.get('id')
        s = Image.objects.get(pk=t)
        s.image = h
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove(request,id,c):
    if c == 'image':
        Image.objects.get(pk=id).delete()
    elif c == 'content':
        Content.objects.get(pk=id).delete()
    elif c == 'code':
        Code.objects.get(pk=id).delete()
    elif c == 'subheading':
        SubHeading.objects.get(pk=id).delete()
    return redirect(request.META.get('HTTP_REFERER'))