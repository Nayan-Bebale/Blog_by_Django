from django.shortcuts import render
from .form import ContactForm

from blog.models import BlogPost

def home_page(request):
    qs = BlogPost.objects.all()[:5]
    context = {"title": "Welcome to django.", 'blog_list':qs}
    return render(request, "index.html", context)


def about_page(request):
    title = "WE ARE NOT SAME."
    return render(request, "about.html", {"title": title})

def contect_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form = ContactForm()
    context = {
        "title": "Contact Us",
        "form": form
    }
    return render(request,"form.html", context)

def example_page(request):
    template_name = "about.html"
    title = "Example Is The best Way to Look something"
    return render(request, template_name, {"title": title})