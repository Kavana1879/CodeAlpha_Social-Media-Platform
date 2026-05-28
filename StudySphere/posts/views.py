import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.http import require_POST
from .models import Post
from .utils import generate_ai_summary
from interactions.models import Comment, Notification

@login_required
def feed(request):
    """
    Renders the central social study dashboard feed showing all posts,
    associated images, likes, live comments, and AI summaries.
    """
    posts = Post.objects.all().prefetch_related('comments__user__profile', 'likes')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/feed.html', context)


@login_required
def create_post(request):
    """
    Handles rendering the workspace editor and processing form submission.
    Runs the automated AI summary utility before saving.
    """
    if request.method == 'POST':
        caption = request.POST.get('caption', '').strip()
        category = request.POST.get('category', 'Notes')
        image = request.FILES.get('image')
        
        if not caption:
            messages.error(request, "Post notes caption cannot be empty.")
            return render(request, 'posts/create_post.html')
            
        # Create Post instance (without saving immediately to append AI summary)
        post = Post(
            user=request.user,
            caption=caption,
            category=category,
            image=image
        )
        
        # Trigger automated AI notes summary
        post.ai_summary = generate_ai_summary(caption)
        post.save()
        
        messages.success(request, "Notes successfully shared! StudySphere AI has summarized your material.")
        return redirect('feed')
        
    return render(request, 'posts/create_post.html')


@login_required
@require_POST
def like_post(request, post_id):
    """
    AJAX view toggling a post's like status.
    Returns live like stats and triggers follow/like alerts.
    """
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
        # Remove like notification if exists
        Notification.objects.filter(
            sender=user, 
            receiver=post.user, 
            notification_type='like', 
            post=post
        ).delete()
    else:
        post.likes.add(user)
        liked = True
        # Trigger notification alert to author
        if post.user != user:
            Notification.objects.get_or_create(
                sender=user,
                receiver=post.user,
                notification_type='like',
                post=post
            )
            
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })


@login_required
@require_POST
def add_comment(request, post_id):
    """
    AJAX view submitting comments instantly.
    Renders comments list elements immediately on the client browser.
    """
    post = get_object_or_404(Post, id=post_id)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid payload'}, status=400)
        
    if not text:
        return JsonResponse({'error': 'Comment content cannot be empty'}, status=400)
        
    comment = Comment.objects.create(
        user=request.user,
        post=post,
        text=text
    )
    
    # Trigger notification alert to post author
    if post.user != request.user:
        Notification.objects.create(
            sender=request.user,
            receiver=post.user,
            notification_type='comment',
            post=post
        )
        
    # Return serializable parameters for Javascript rendering
    return JsonResponse({
        'id': comment.id,
        'username': comment.user.username,
        'profile_image': comment.user.profile.profile_image.url,
        'text': comment.text,
        'created_at': timesince(comment.created_at) + " ago",
        'total_comments': post.comments.count()
    })


@login_required
@require_POST
def delete_comment(request, comment_id):
    """
    AJAX view allowing authors or comment-owners to safely delete comments.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Authorized checks: either the comment owner OR the post owner can delete
    if comment.user == request.user or post.user == request.user:
        comment.delete()
        return JsonResponse({
            'success': True,
            'total_comments': post.comments.count()
        })
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
