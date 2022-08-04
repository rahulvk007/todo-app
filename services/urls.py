from django.urls import path,include
from tomlkit import document
from . import views


urlpatterns = [
    path("profile/<slug:slug>",views.display_profile, name="profile"),
    path("home/",views.home,name = "portal"),
    path("create/work/",views.WorkCreateView.as_view(),name = "create_work"),
    path("view/<slug:slug>/work/<int:pk>/member/",views.WorkDetailView.as_view(),name = "view_work"),
    path("manage/works/all/",views.ManageWorksView.as_view(),name = "manage_works"),
    path("manage/work/<int:pk>/update/<slug:slug>/",views.ManageWorksView.as_view(),name = "manage_works"),
    path("manage/progress/update/<int:pk>/member/",views.update_progress_by_member,name = "update_progress"),
]