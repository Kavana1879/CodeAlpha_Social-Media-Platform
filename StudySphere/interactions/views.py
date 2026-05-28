from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Notification
from users.models import UserProfile

@login_required
def notifications(request):
    """
    Renders notifications list and auto-marks them as read.
    """
    notifs = request.user.notifications.all()
    
    # Render view
    context = {
        'notifications': notifs,
    }
    
    # Mark them all as read once the user visits the page
    Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'interactions/notifications.html', context)


@login_required
@require_POST
def mark_all_read(request):
    """
    POST view to explicitly mark all notifications as read.
    """
    Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications')


@login_required
@require_POST
def toggle_follow(request, user_id):
    """
    AJAX view toggling follow state between students.
    Returns follower counts and updates follower networks.
    """
    target_user = get_object_or_404(User, id=user_id)
    target_profile = target_user.profile
    request_profile = request.user.profile
    
    if target_user == request.user:
        return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)
        
    # Check if currently following
    if request_profile in target_profile.followers.all():
        # Unfollow
        target_profile.followers.remove(request_profile)
        following = False
        
        # Delete follow notification if exists
        Notification.objects.filter(
            sender=request.user,
            receiver=target_user,
            notification_type='follow'
        ).delete()
    else:
        # Follow
        target_profile.followers.add(request_profile)
        following = True
        
        # Create follow notification alert
        Notification.objects.get_or_create(
            sender=request.user,
            receiver=target_user,
            notification_type='follow'
        )
        
    return JsonResponse({
        'following': following,
        'followers_count': target_profile.followers.count(),
        'following_count': target_profile.following.count(),
        'request_following_count': request_profile.following.count()
    })
