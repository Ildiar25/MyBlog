from . import BaseTestClass

from app.public.models import Post


class PostModelTestCase(BaseTestClass):

    def test_titleSlug(self) -> None:
        with self.app.app_context():
            post = Post(title="Test Post", content="Content", user_id=self.admin_id)
            post.save()

            self.assertEqual(first="test-post", second=post.slug_title, msg="Slug title must be 'test-post'.")

    def test_repeatedTitleSlug(self) -> None:
        with self.app.app_context():
            post = Post(title="Test Post", content="Content", user_id=self.admin_id)
            post.save()

            post_duplicated = Post(title="Test Post", content="Content", user_id=self.admin_id)
            post_duplicated.save()

            self.assertEqual(
                first="test-post-1", second=post_duplicated.slug_title, msg="Slug title must be 'test-post-1'."
            )
