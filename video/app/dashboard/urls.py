# coding:utf-8
from django.urls import path
from .views.base import Base
from .views.auth import Login, AdminManger, LogoutUser, UpdateAdminStatus
from .views.video import ExternaVideo, VideoSubView, VideoStarView, StarDeleteView

urlpatterns = [
    path('', Base.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='login'),
    path('manager', AdminManger.as_view(), name='admin_manager'),
    path('logout', LogoutUser.as_view(), name='logout'),
    path('admin_manager', UpdateAdminStatus.as_view(), name='admin_update_status'),
    path('video/externa', ExternaVideo.as_view(), name='externa_video'),
    path('video/videosub/<int:video_id>', VideoSubView.as_view(), name='videosub'),
    path('video/star', VideoStarView.as_view(), name='video_star'),
    path('video/star/delete/<int:star_id>/<int:video_id>',StarDeleteView.as_view(), name='star_delete')
]
