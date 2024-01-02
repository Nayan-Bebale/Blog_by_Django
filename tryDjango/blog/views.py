from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views import View
# from django.utils import timezone
# Create your views here.

from .form import BlogPostModelForm, SignupForm, LoginForm
from blog.models import BlogPost


def user_has_permission(user):
    return user.is_staff or user.has_perm('blog.add_blogpost')  # Adjust 'your_app.add_blogpost' to the actual permission


def blog_post_detail_page(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog_post_details.html"
    context = {"object":obj}
    return render(request, template_name, context)



# this checks if the user is already logged in and returns its username
def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username = request.user.username
    else:
        username = None
    return username

# Create logged out
def logged_view(request):
    username = UserLoggedIn(request)
    if username != None:
        logout(request)
        return redirect("blog_post_list_view")

# Signup page

def signup_view(request): 
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blog_post_list_view")
    else:
        form = SignupForm()

    template_name = 'signup.html'
    context = {'form': form}
    return render(request, template_name, context)

# User's post
class UserPostView(View):
    template_name = "user_posts.html"

    def get(self, request):
        # Retrieve the blog posts for the currently logged-in user
        user_post = BlogPost.objects.user_posts(request.user)

        # Pass the user_post to the template
        context = {'user_posts': user_post}
        print(context)
        return render(request, self.template_name, context)



# login page
@csrf_protect
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog_post_list_view")
    else:
        form = LoginForm()
        
    template_name= "login.html"
    context = {'form': form}
    return render(request, template_name, context)
# Create Retrive Update Delete

def blog_post_list_view(request):
    # list out objects
    # could be search
    # now = timezone.now()
    qs = BlogPost.objects.all().published()
    # qs = BlogPost.objects.filter(publish_date__lte=now)
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = "blog_post_list.html"
    context = {'object_list': qs}
    return render(request, template_name, context)



def blog_post_create_view(request):
    # Create objects
    # ? use a form 
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to the login page

    if not user_has_permission(request.user):
        return redirect('permission_denied')  # Redirect users without permission to a custom permission_denied page

    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = BlogPostModelForm()
    template_name = "form.html"
    context = {'form': form}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog_post_retrive.html"
    context = {'object': obj}
    return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = "form.html"
    context = {'form':form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog_post_delete.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {'object': obj}
    return render(request, template_name, context)
