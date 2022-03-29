"""voteapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from votes import views

urlpatterns = [
    path('', views.view_all_polls),

    path('polls/', views.view_all_polls, name='view_all_polls'),           # 전체 투표 주제
    path('polls/create/', views.create_poll, name='create_poll'),       # 투표주제 생성하기
    path('polls/<int:id>/', views.view_poll_by_id, name='view_poll_by_id'),     # 특정 투표주제 결과보기
    path('polls/<int:id>/vote/', views.vote_poll, name='vote_poll'),       # 투표하기
    path('polls/<int:id>/update/', views.update_poll, name='update_poll'),     # 투표주제 수정하기
    path('polls/<int:id>/delete', views.delete_poll, name='delete_poll')       # 투표주제 삭제하기
]
