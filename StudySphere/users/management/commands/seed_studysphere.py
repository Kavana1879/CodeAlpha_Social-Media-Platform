import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Badge, UserProfile
from posts.models import Post
from posts.utils import generate_ai_summary
from interactions.models import Comment, Notification

class Command(BaseCommand):
    help = 'Seeds StudySphere database with initial glowing skill badges, mock academic students, rich posts, and comments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting StudySphere DB seeding operations..."))
        
        # 1. Clear Existing Data
        self.stdout.write("Purging old records...")
        Comment.objects.all().delete()
        Notification.objects.all().delete()
        Post.objects.all().delete()
        Badge.objects.all().delete()
        
        # Delete non-superuser accounts
        User.objects.filter(is_superuser=False).delete()
        
        # 2. Create Glowing Achievement & Skill Badges
        self.stdout.write("Generating neon achievement badges...")
        badges_data = [
            {
                "name": "Python Beginner",
                "description": "Knows fundamentals of python variables, control flow, loops, and lists.",
                "icon_class": "fa-brands fa-python",
                "glow_color": "purple"
            },
            {
                "name": "Java Developer",
                "description": "Knows OOP classes, interfaces, inheritances, and multithreading.",
                "icon_class": "fa-brands fa-java",
                "glow_color": "blue"
            },
            {
                "name": "AI Explorer",
                "description": "Understands neural networks, deep learning summaries, and generative models.",
                "icon_class": "fa-solid fa-brain",
                "glow_color": "pink"
            },
            {
                "name": "UI/UX Designer",
                "description": "Master of glassmorphism UI cards, glowing elements, and responsive designs.",
                "icon_class": "fa-solid fa-palette",
                "glow_color": "pink"
            },
            {
                "name": "Hackathon Champion",
                "description": "Successfully designed and launched a fully functioning prototype within 24 hours.",
                "icon_class": "fa-solid fa-code-fork",
                "glow_color": "green"
            },
            {
                "name": "DSA Learner",
                "description": "Mastered sorting, lists, stacks, trees, and space-time complexity analysis.",
                "icon_class": "fa-solid fa-diagram-project",
                "glow_color": "green"
            }
        ]
        
        badges = {}
        for b in badges_data:
            badge = Badge.objects.create(
                name=b["name"],
                description=b["description"],
                icon_class=b["icon_class"],
                glow_color=b["glow_color"]
            )
            badges[badge.name] = badge
            
        # 3. Create Multiple Mock Academic Users
        self.stdout.write("Initializing student profiles across branches...")
        students_data = [
            {
                "username": "ananya",
                "email": "ananya@college.edu",
                "password": "Password123",
                "branch": "Computer Science",
                "bio": "Third-year CSE undergrad. Fascinated by data structures, algorithmic puzzles, and scalable backends. Always up for a cup of coffee and standard pair-programming sessions!",
                "skills": "Python, Java, Django, DSA, PostgreSQL",
                "badges": ["Python Beginner", "DSA Learner", "Hackathon Champion"]
            },
            {
                "username": "rohan",
                "email": "rohan@college.edu",
                "password": "Password123",
                "branch": "AI / ML",
                "bio": "AI engineering student exploring Neural Networks, LLMs, and computer vision. Working on training custom embeddings for automated study bots.",
                "skills": "Python, PyTorch, AI/ML, NLP, Scikit-Learn",
                "badges": ["Python Beginner", "AI Explorer"]
            },
            {
                "username": "isha",
                "email": "isha@college.edu",
                "password": "Password123",
                "branch": "Data Science",
                "bio": "Mastering dashboard designs, mathematical statistics, and big data analysis. Let's make study notes clean and structured!",
                "skills": "Python, UI/UX, Big Data, SQL, Figma",
                "badges": ["UI/UX Designer", "Python Beginner"]
            },
            {
                "username": "kaviraj",
                "email": "kaviraj@college.edu",
                "password": "Password123",
                "branch": "Information Technology",
                "bio": "Passionate about full-stack web architectures. Building modern tools for student collaborations. Hackathons are my playground.",
                "skills": "JavaScript, React, Node.js, WebDev, Git",
                "badges": ["Hackathon Champion", "UI/UX Designer"]
            }
        ]
        
        users = {}
        for s in students_data:
            user = User.objects.create_user(
                username=s["username"],
                email=s["email"],
                password=s["password"]
            )
            
            # Access auto-created profile
            profile = user.profile
            profile.branch = s["branch"]
            profile.bio = s["bio"]
            profile.skills = s["skills"]
            
            # Assign fallback avatar if exists
            avatar_path = "profile_images/default_avatar.png"
            profile.profile_image = avatar_path
            profile.save()
            
            # Assign badges
            for badge_name in s["badges"]:
                profile.badges.add(badges[badge_name])
                
            users[user.username] = user
            
        # 4. Link Followers Network (to populate counts immediately!)
        self.stdout.write("Linking student follower networks...")
        # ananya is followed by rohan, isha, and kaviraj
        users["ananya"].profile.followers.add(users["rohan"].profile)
        users["ananya"].profile.followers.add(users["isha"].profile)
        users["ananya"].profile.followers.add(users["kaviraj"].profile)
        
        # rohan is followed by ananya and isha
        users["rohan"].profile.followers.add(users["ananya"].profile)
        users["rohan"].profile.followers.add(users["isha"].profile)
        
        # isha is followed by kaviraj and ananya
        users["isha"].profile.followers.add(users["kaviraj"].profile)
        users["isha"].profile.followers.add(users["ananya"].profile)

        # 5. Populate Timelines with Rich Note Posts
        self.stdout.write("Publishing academic study notes and syncing AI summaries...")
        posts_data = [
            {
                "username": "ananya",
                "category": "Coding",
                "caption": "Python Decorators are incredibly clean. They allow you to wrap another function in order to extend the behavior of the wrapped function, without permanently modifying it. This is highly useful in logging, authentication checks, and timing function executions.\n\nHere is a simple blueprint:\ndef log_execution(func):\n    def wrapper(*args, **kwargs):\n        print(f'Starting {func.__name__}')\n        result = func(*args, **kwargs)\n        print(f'Finished {func.__name__}')\n        return result\n    return wrapper"
            },
            {
                "username": "rohan",
                "category": "AI/ML",
                "caption": "Large Language Models (LLMs) operate through complex transformer mechanisms. They process tokens using multi-headed self-attention parameters to understand semantics. By mapping inputs to dense vectors, neural weights predict the most probable next token in sequence.\n\nIt is fascinating how scaling up parameters from millions to billions unlocks emergent cognitive-like problem-solving behaviors!"
            },
            {
                "username": "isha",
                "category": "Notes",
                "caption": "Database Normalization (1NF to 3NF) is vital for standard relational architectures. The primary goal of normalization is to minimize data redundancy and prevent insertion, update, and deletion anomalies. By decomposing tables and establishing foreign key constraints, we guarantee data consistency and speed up analytical queries."
            },
            {
                "username": "kaviraj",
                "category": "Projects",
                "caption": "StudySphere UI Design Sprint completed today. I designed semi-transparent dark surfaces with subtle white/neon borders, backed by a backdrop-filter blur of 16px and soft neon box-shadows. The layout feels responsive and fully alive.\n\nMoving on to hook up the Django backend views and AJAX controllers next!"
            }
        ]
        
        created_posts = []
        for p in posts_data:
            post = Post(
                user=users[p["username"]],
                category=p["category"],
                caption=p["caption"]
            )
            # Run AI summary engine
            post.ai_summary = generate_ai_summary(p["caption"])
            post.save()
            created_posts.append(post)
            
        # 6. Generate Social Interactions (Likes & Comments)
        self.stdout.write("Simulating user likes, comments, and notifications...")
        # Post 1 (ananya's Coding post) gets likes and comments
        post1 = created_posts[0]
        post1.likes.add(users["rohan"], users["isha"], users["kaviraj"])
        Comment.objects.create(
            user=users["rohan"],
            post=post1,
            text="This is an awesome explanation of python wrappers! Helped me clean up my data processing scripts."
        )
        Comment.objects.create(
            user=users["kaviraj"],
            post=post1,
            text="Agreed! Very clean and beginner-friendly snippet. I will use this in our final semester web app."
        )
        
        # Trigger mock notifications for post1
        Notification.objects.create(
            sender=users["rohan"],
            receiver=users["ananya"],
            notification_type='like',
            post=post1
        )
        Notification.objects.create(
            sender=users["rohan"],
            receiver=users["ananya"],
            notification_type='comment',
            post=post1
        )
        
        # Post 2 (rohan's AI/ML post) gets likes and comments
        post2 = created_posts[1]
        post2.likes.add(users["ananya"], users["isha"])
        Comment.objects.create(
            user=users["ananya"],
            post=post2,
            text="Emergent abilities are truly mind-blowing. Have you looked into lightweight local parameter fine-tuning yet?"
        )
        Notification.objects.create(
            sender=users["ananya"],
            receiver=users["rohan"],
            notification_type='like',
            post=post2
        )
        
        # Post 3 (isha's normalization post) gets liked
        post3 = created_posts[2]
        post3.likes.add(users["ananya"])
        
        self.stdout.write(self.style.SUCCESS("Database seeded successfully! StudySphere is ready for student interaction."))
