from . import BaseTestClass

from app.public.models import Post


class PostModelTestCase(BaseTestClass):

    def test_titleSlug(self) -> None:
        with self.app.app_context():
            post = Post(title="Test Post", content="Content", user_id=self.admin_id)
            post.save()

            self.assertEqual(first="test-post", second=post.slug_title, msg="Slug title must be 'test-post'.")
