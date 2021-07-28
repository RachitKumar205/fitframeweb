from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pose/<int:pose_id>/", views.pose, name="pose"),
    path("accounts/register/", views.signup, name="signup")
]
