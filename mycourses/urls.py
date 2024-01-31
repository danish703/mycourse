"""
URL configuration for mycourses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import (home,chapterList,saveTopics,
                    addChapter,post,subHeadingSaving,
                    contentSaving,codeSaving,imageSaving,
                    updateSubheading,updateContent,imageUpdateSaving,remove,signin
                    )
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',home,name='home'),
    path('login/',signin,name='login'),
    path('chapters/<int:course_id>',chapterList,name='chapterList'),
    path('add-topics/',saveTopics,name='saveTopics'),
    path('topic/<int:topic_id>',post,name='post'),
    path('add-chapters/',addChapter,name='addChapter'),
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    #saving
    path('subheading/',subHeadingSaving,name='subheading'),
    path('content/',contentSaving,name='contentSaving'),
    path('code/',codeSaving,name='codeSaving'),
    path('image/',imageSaving,name='imageSaving'),
    #update
    path('update-subheading/',updateSubheading,name='updateSubheading'),
    path('update-content/',updateContent,name='updateContent'),
    path('image-updating/',imageUpdateSaving,name='imageUpdating'),
    path('remove/<int:id>/<str:c>',remove,name='remove'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
