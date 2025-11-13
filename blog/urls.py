"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index),
    path("post/list/", views.PostList),
    path("post/create/", views.PostCreate),
    path("post/update/<int:pk>/", views.PostUpdate),
    path("post/detail/<int:pk>/", views.PostDetail),
    path("post/delete/<int:pk>/", views.PostDelete),
    path("post/activate/<int:pk>/", views.PostActivate),
    path("post/deactivate/<int:pk>/", views.PostDeactivate),
    path("post/reaction/<int:post_id>/", views.ReactionToggle),
    path("category/list/", views.CategoryList),
    path("category/create/", views.CategoryCreate),
    path("category/update/<int:pk>/", views.CategoryUpdate),
    path("category/delete/<int:pk>/", views.CategoryDelete),
    path("comment/create/<int:post_pk>/", views.CommentCreate),
    path("login/", views.Login),
    path("register/", views.Register),
    path("logout/", views.Logout),
    path("change_password/", views.ChangePassword),
    path("notifications/", views.NotificationList),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
