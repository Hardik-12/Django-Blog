from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Comment,Author,Tag
from .forms import CommentForm,CreateUserForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def SignUpPage(request):
    if(request.user.is_authenticated):
        return redirect('index')
    else:
        form = CreateUserForm()
        if(request.method == 'POST'):
            form = CreateUserForm(request.POST)
           
            if(form.is_valid()):
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Your Account was Successfully created")
                return redirect('login')
            else:
                return render(request, "app/signup.html",{
                    "form": form
                })


        return render(request, "app/signup.html",{
            "form": form
        })
            
def LoginPage(request):
    if(request.user.is_authenticated):
        return redirect('index')
    else:
        if(request.method == 'POST'):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, "Username or Password is incorrect")

        return render(request, "app/login.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')


def Index(request):
    latest_posts = Post.objects.order_by("-date")
    return render(request, "app/index.html",{
        "latest_posts": latest_posts
    })



def AllPosts(request):
    AllPosts = Post.objects.all()
    return render(request, "app/all_posts.html",{
        "all_posts_show": AllPosts
    })



def PostDetail(request, slug):
    post_render = Post.objects.get(slug = slug)
    count_comments = post_render.comments.all().count()
    stored_posts = request.session.get('stored_posts')
    
    if stored_posts is not None:
        is_saved_for_later = post_render.id in stored_posts
    else:
        is_saved_for_later = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.post = post_render
            comment.save()
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))

        else:
            
            return render(request, "app/post-detail.html",{
                "comment_form": comment_form,
                "post": post_render,
                "count": count_comments,
                "saved_for_later": is_saved_for_later
            })


    
    return render(request, "app/post-detail.html", {
        "comment_form": CommentForm(),
        "post": post_render,
        "count": count_comments,
        "saved_for_later": is_saved_for_later
    })

def AllComments(request, slug):
    part_post = Post.objects.get(slug = slug)
    post_comments = part_post.comments.all()
    return render(request, "app/all_comments.html",{
        "all_comments": post_comments
    })

def ReadLater(request):
    # We have to maintain a lists of posts which we store in session.
    
    if(request.method == 'POST'):
        # If there are no stored posts then we initialize an empty list
        stored_posts = request.session.get("stored_posts")
        if(stored_posts is None):
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
    
    else:
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in = stored_posts)
            context['posts'] = posts
            context['has_posts'] = True
    return render(request, "app/stored_posts.html", context)





