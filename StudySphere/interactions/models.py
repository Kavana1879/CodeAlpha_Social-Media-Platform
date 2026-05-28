from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Comment(models.Model):
    """
    Model representing user comments under posts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class Notification(models.Model):
    """
    Model representing student alerts on StudySphere.
    Fires on follow, new post likes, or comments, with customized neon templates.
    """
    TYPE_CHOICES = [
        ('like', 'New Like ❤️'),
        ('comment', 'New Comment 💬'),
        ('follow', 'New Follower 👤'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.receiver.username} from {self.sender.username} ({self.notification_type})"
