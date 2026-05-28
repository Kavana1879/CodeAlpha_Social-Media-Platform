from django.contrib.auth.models import User
from users.models import UserProfile
from .models import Notification

def notifications(request):
    """
    Context processor to make notifications counts and suggested students
    globally available across all templates on StudySphere.
    """
    if request.user.is_authenticated:
        # Count unread notifications
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
        
        try:
            # Users the current student already follows
            user_profile = request.user.profile
            following_profiles = user_profile.following.all()
            following_user_ids = [p.user.id for p in following_profiles]
            
            # Suggest students who:
            # 1. Are not the current user
            # 2. Are not already followed by the current user
            suggested = UserProfile.objects.exclude(user=request.user).exclude(user__id__in=following_user_ids).order_by('?')[:4]
        except Exception:
            suggested = []
            
        return {
            'unread_notifications_count': unread_count,
            'suggested_students': suggested,
        }
        
    return {
        'unread_notifications_count': 0,
        'suggested_students': [],
    }
