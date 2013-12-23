from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^mygroups/$', view=login_required(GroupListView.as_view()),
        name="group_list"),
    url(r'^$', view=login_required(AllGroupListView.as_view()),
        name="group_list_all"),
    url(r'^(?P<group_pk>[\d]+)/join/$', view=login_required(GroupJoinView.as_view()),
        name="group_join"),
    url(r'^add/$', view=login_required(GroupCreateView.as_view()),
        name="group_add"),
    url(r'^(?P<group_pk>[\d]+)/$',
        view=login_required(GroupDetailView.as_view()),
        name="group_detail"),
    url(r'^(?P<group_pk>[\d]+)/edit/$',
        view=login_required(GroupUpdateView.as_view()),
        name="group_edit"),
    url(r'^(?P<group_pk>[\d]+)/delete/$',
        view=login_required(GroupDeleteView.as_view()),
        name="group_delete"),

    # Group user URLs
    url(r'^(?P<group_pk>[\d]+)/people/$',
        view=login_required(GroupUserListView.as_view()),
        name="group_user_list"),
    url(r'^(?P<group_pk>[\d]+)/people/add/$',
        view=login_required(GroupUserCreateView.as_view()),
        name="group_user_add"),
    url(r'^(?P<group_pk>[\d]+)/people/(?P<user_pk>[\d]+)/$',
        view=login_required(GroupUserDetailView.as_view()),
        name="group_user_detail"),
    url(r'^(?P<group_pk>[\d]+)/people/(?P<user_pk>[\d]+)/edit/$',
        view=login_required(GroupUserUpdateView.as_view()),
        name="group_user_edit"),
    url(r'^(?P<group_pk>[\d]+)/people/(?P<user_pk>[\d]+)/delete/$',
        view=login_required(GroupUserDeleteView.as_view()),
        name="group_user_delete"),
)

