from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile, Badge
from posts.models import Post
from posts.utils import generate_ai_summary

class StudySphereCoreTests(TestCase):
    """
    Test suite covering StudySphere profile signal bindings, AI notes summary,
    and post structures.
    """

    def setUp(self):
        # Create initial test user
        self.user = User.objects.create_user(username="teststudent", email="test@college.edu", password="securepassword")

    def test_user_profile_signal_creation(self):
        """
        Verify that a UserProfile is automatically created when a User is saved.
        """
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.user, self.user)
        self.assertEqual(self.user.profile.branch, "")

    def test_ai_summary_engine(self):
        """
        Verify that the AI notes summarizer extracts the first 1-2 sentences correctly.
        """
        # Long note containing multiple sentences
        long_note = "Large Language Models operate through complex transformers. They process tokens using multi-headed self-attention. emergent abilities unlock when scaling parameter bounds."
        summary = generate_ai_summary(long_note)
        
        # Should extract first two sentences
        self.assertIn("Large Language Models operate through complex transformers.", summary)
        self.assertIn("They process tokens using multi-headed self-attention.", summary)
        self.assertNotIn("emergent abilities unlock when scaling parameter bounds.", summary)
        
        # Test short note
        short_note = "Single sentence note."
        self.assertEqual(generate_ai_summary(short_note).strip(), "Single sentence note.")

    def test_post_creation_and_likes(self):
        """
        Verify post category boundaries and liking interactions.
        """
        post = Post.objects.create(
            user=self.user,
            caption="Let's study sorting algorithms tonight!",
            category="Coding"
        )
        self.assertEqual(post.total_likes, 0)
        self.assertEqual(post.category, "Coding")
        
        # User likes the post
        post.likes.add(self.user)
        self.assertEqual(post.total_likes, 1)
        self.assertTrue(post.likes.filter(id=self.user.id).exists())
