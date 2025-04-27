from . import BaseTestClass


class BlogClientTestCase(BaseTestClass):

    def test_indexStatusCode(self) -> None:
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)

    def test_indexWithoutPosts(self) -> None:
        response = self.client.get("/")
        self.assertIn(b"No hay entradas", response.data)
