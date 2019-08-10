from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .models import Post, CV
from .forms import CVForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .algo import Rank
from django.contrib import messages
import os
from django.conf import settings
from django.http import HttpResponse, Http404

#context is dictionary and key is called posts and  values are the posts we've created at top
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# Job Posting Ko Lagie
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    # This view is for list of job posts
    model = Post
    template_name = "blog/user_post.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    # in order to modify query set that list view gives and change querry set from there
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(View):
    template = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, author=request.user)
        # print(kwargs)
        # post = Post.objects.filter(author=request.user)
        return render(request, self.template, {
            'object': post,
        })


class PostCreateView(LoginRequiredMixin, CreateView): #login navai add garna mildaina if so it will direct to login page
    model = Post
    fields = ['title', 'skill', 'education',
              'experience', 'required', 'salary'] #kun kun rakhera create garney

    #form valid method login garekai le post gareko ho ki nai
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #login navai add garna mildaina if so it will direct to login page also usermixin allwos post gareko user le matra change garna milney
    model = Post
    fields = ['title', 'skill', 'education',
              'experience', 'required', 'salary'] #kun kun rakhera create garney

    #form valid method login garekai le post gareko ho ki nai
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): #tei user le matra updaee garna milcha
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' #homepage

    def test_func(self):  # tei user le matra updaee garna milcha
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#uploading CV's


# def upload(request):
#     # context = {
#     #     'name': name
#     # }
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         fs.save(uploaded_file.name, uploaded_file)
#         # context['url'] = fs.url(name)
#     return render(request, 'blog/upload.html')


def upload_cv_list(request, *args, **kwargs):
    post = get_object_or_404(Post, id=kwargs.get('pk'))
    # logging.warning(post)
    qs = CV.objects.filter(post=post)
    # logging.warning(qs)
    filtered_cv_qs = Rank(qs, post)
    print('filtered_cv: ', filtered_cv_qs)
    return render(request, 'blog/cv_upload_list.html', {'cvs': filtered_cv_qs})


def upload_cv(request, *args, **kwargs):
    template = 'blog/cv_upload.html'
    form = CVForm(request.POST or None)
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        post = get_object_or_404(Post, id=kwargs.get('pk'))
        instance = form.save(commit=False)
        instance.user = request.user
        instance.post = post
        instance.save()
        messages.success(request, f'Your CV has been uploaded. Upload CV in other vacancies too.')
        return redirect(reverse_lazy('blog-home'))
    return render(request, template, {'form': form})


def delete_cv(request, pk):
    if request.method == 'POST':
        cv = CV.objects.get(pk=pk)
        cv.delete()
    return redirect('cv-upload-list')


# def download_cv(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/pdf")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404

def download_cv(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, "cvs", filename)
    print('filename:', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        raise Http404



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})





