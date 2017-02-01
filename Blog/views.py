from django.shortcuts import render
from django.shortcuts import *
from Blog.models import *
from django.template.defaultfilters import slugify
from django.template import Context
# Create your views here.


def index(request):
    blogs = Blog.objects.all().order_by('-id')
    for blog in blogs:
        blog.slugify = slugify(blog.title)
    return render(request, "Tenants/blog.html", {"blogs": blogs})


def view_blogpost(request, blog_id, slug):
    try:
        blog = Blog.objects.get(id=blog_id)
        blog.tag_list = blog.tags.split(',')
        return render(request, "Tenants/blog_post.html", {"blog": blog})
    except:
        return render(request, "Tenants/blog_post.html", {"error": "Blog niet gevonden"})
