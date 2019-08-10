from django.urls import path
from django.conf.urls import url
# from django.views.static import serve
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    download_cv)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #tyo key vako wala post lai chai update garna milney
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),

    # path('upload/', views.upload, name='cv-upload'),
    path('cvs/<int:pk>/', views.upload_cv_list, name='cv-upload-list'),
    # path('cvs/<int:pk>/<path>/', views.download_cv, name='cv-download'),
    path('cvs/upload/<int:pk>/', views.upload_cv, name='cv-up'),
    path('cvs/<int:pk>/', views.delete_cv, name='cv-delete'),
    url(r'^cvs/download/(?P<filename>.*)$', download_cv, name="download-cv"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
