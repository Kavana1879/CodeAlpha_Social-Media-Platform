from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    """
    Model representing achievements or skill badges earned by students.
    E.g., 'Python Beginner', 'AI Explorer', 'UI/UX Designer'.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(
        max_length=100, 
        default="fa-solid fa-graduation-cap", 
        help_text="Font Awesome class for the icon (e.g. 'fa-brands fa-python')"
    )
    glow_color = models.CharField(
        max_length=50, 
        default="purple", 
        choices=[
            ("purple", "Neon Purple"),
            ("blue", "Neon Blue"),
            ("pink", "Neon Pink"),
            ("green", "Neon Green"),
        ],
        help_text="Color class used for neon shadow and background animations"
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    Extends the default Django User model with student-centric attributes
    including bio, branch, comma-separated skills, badges, and followers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True, help_text="Short bio about the student")
    branch = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Department or engineering branch (e.g., Computer Science, Data Science)"
    )
    skills = models.TextField(
        blank=True, 
        help_text="Comma-separated list of interests/skills (e.g., Python, UI/UX, DSA)"
    )
    profile_image = models.ImageField(
        upload_to="profile_images/", 
        default="profile_images/default_avatar.png"
    )
    badges = models.ManyToManyField(Badge, blank=True, related_name="profiles")
    followers = models.ManyToManyField(
        "self", 
        symmetrical=False, 
        related_name="following", 
        blank=True
    )
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def skills_list(self):
        """Helper to return skills as an actual list in templates."""
        if self.skills:
            return [s.strip() for s in self.skills.split(",") if s.strip()]
        return []
