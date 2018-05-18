# from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from datetime import datetime
from django.template.loader import get_template
from django.shortcuts import redirect


# Create your views here.


def homepage(request):
    template = get_template('index.html')
    posts = Post.objects.all()
    now = datetime.now()
    html = template.render(locals())

    return HttpResponse(html)

    # post_lists = list()
    # for count, post in enumerate(posts):
    #     post_lists.append("No.{}:".format(str(count)) + str(post.title) + "<br>")
    #     post_lists.append("<small>" + str(post.body) + "</small><br><br>")
    # return HttpResponse(post_lists)


def showPost(request, slug):
    template = get_template('post.html')
    try:
        post = Post.objects.get(slug=slug)
        if post != None:
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return redirect('/')
