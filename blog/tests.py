from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        self.post = Post.objects.create(
            title="Test post",
            content="Test content",
            author=self.user
        )

    def test_post_list_status_code(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_status_code(self):
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)