from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.
from newsfeed.models import Post, Comment

def create_post(request):
    if request.method == "POST":
        
        content = request.POST.get('content')
        post_img = request.FILES.get('post_img')
        print(content)
        print(post_img)

        Post.objects.create(
            content=content,
            post_img=post_img,
            user=request.user
        )
        
        print(Post.objects.all()[0])

    return redirect('newsfeed:newsfeed')
    

@login_required
def toggle_post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)  # Unlike
    else:
        post.likes.add(user)  # Like

   # Redirect to 'next' page if provided, else profile
    next_url = request.POST.get('next', '/')
    return redirect(next_url)




@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    next_url = request.POST.get('next', '/')
    return redirect(next_url)


@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=parent_comment.post,
                user=request.user,
                content=content,
                parent=parent_comment,
                is_reply=True
            )
    next_url = request.POST.get('next', '/')
    return redirect(next_url)




def news_feed(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
       
        if hasattr(post.user, 'profile') and post.user.profile.profile_picture:
            post.user_profile_picture = post.user.profile.profile_picture.url
        else:
            post.user_profile_picture = None  
     
    return render(request,'newsfeed/feed.html',{"posts": posts})





@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    edited = True
    # Check if the logged-in user is the owner of the post
    if request.user != post.user:
        return redirect('newsfeed:newsfeed')  # Redirect to home or another page if not the owner
    
    if request.method == 'POST':
        content = request.POST.get('content')
        post_img = request.FILES.get('post_img')
        
        # Update post content
        if content:
            post.content = content
        
        # If a new image is uploaded, update the image
        if post_img:
            post.post_img = post_img
        
        post.save()
        edited = False  # Set flag to indicate that the post was edited
        
        # Redirect back to the post page or the profile page
        return redirect('newsfeed:newsfeed')

    
    return render(request, 'newsfeed/feed.html', {'post': post,'edited':edited})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('newsfeed:newsfeed')  # Adjust redirect as needed



def search_post(request):
    posts = Post.objects.all()

    # 🔍 Keyword Search
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(content__icontains=query))

    # 🗂️ Filter by Date
    date_order = request.GET.get('date_order')
    if date_order == 'newest':
        posts = posts.order_by('-created_at')
    elif date_order == 'oldest':
        posts = posts.order_by('created_at')

    # 🖼️ Filter by Media Type
    media_type = request.GET.get('media_type')
    if media_type == 'text':
        posts = posts.filter(image__isnull=True)
    elif media_type == 'image':
        posts = posts.filter(image__isnull=False)

    # 👤 Filter by Author
    author = request.GET.get('author')
    if author:
        posts = posts.filter(user__username__icontains=author)

    # 🔗 Attach Profile Picture
    for post in posts:
        post.user_profile_picture = (
            post.user.profile.profile_picture.url if hasattr(post.user, 'profile') and post.user.profile.profile_picture else None
        )

    return render(request, 'newsfeed/searched_feed.html', {"posts": posts})


