from django.contrib.auth.models import User
from django.test import Client, TestCase
from Main.models import Image, Project
from Main.tests.helpers import AddFixtures, MoveBaseAbstract


class HomePageTest(AddFixtures, TestCase):
    def setUp(self):
        self.c = Client()
        self.test_proj2.published = True
        self.test_proj2.save()

    def test_home_unauthenticated(self):
        r = self.c.get("/")
        self.assertTrue(
            r.status_code == 200, msg="Home page should return 200 not logged in"
        )
        self.assertTrue(len(r.context["projects"]) == 1)
        self.assertNotIn(
            f'<a class="btn btn-info mr-2 reorderBtn" id="{str(self.test_proj2.id)}-moveUp" role="button">Up</a>',
            r.content.decode("utf-8"),
        )

    def test_home_authenticated(self):
        su = User.objects.create(username="uname")
        su.is_staff = True
        su.is_superuser = True
        su.set_password("paasssqwer123;")
        su.save()
        self.assertTrue(su.is_superuser)

        status = self.c.login(username="uname", password="paasssqwer123;")
        self.assertEqual(status, True)

        r = self.c.get("/")
        self.assertTrue(
            r.status_code == 200, msg="Home page should return 200 logged in"
        )
        # print(r.context['projects'])
        self.assertTrue(len(r.context["projects"]) == 2)
        self.assertInHTML(
            f'<a class="btn btn-info mr-2 reorderBtn" id="{str(self.test_proj2.id)}-moveUp" role="button">Up</a>',
            r.content.decode("utf-8"),
        )
        self.c.logout()


class TestProjectDetail(AddFixtures, TestCase):
    def setUp(self):
        self.c = Client()
        self.test_proj2.published = True
        self.test_proj2.save()
        self.test_proj3 = Project.objects.create(
            title="test3", slug="test-3", published=True, description="Test Description"
        )
        self.test_proj3.images.add(Image.objects.all().first())

    def test_unpublished_unauthenticated(self):
        r = self.c.get(f"/projects/{self.test_proj1.slug}/")
        self.assertEqual(
            r.status_code, 403, "unauthenticated user shouldn't see unpublished"
        )

        r = self.c.get(f"/projects/{self.test_proj2.slug}/")
        self.assertEqual(r.status_code, 200)

    def test_next_link(self):
        r = self.c.get(f"/projects/{self.test_proj2.slug}/")
        self.assertInHTML(
            f'<small><a class="float-end" href={self.test_proj3.get_absolute_url()}>{self.test_proj3.title} <i class="bi bi-chevron-right"></i></a></small>',
            r.content.decode("utf-8"),
        )

    def test_previous_link(self):
        r = self.c.get(f"/projects/{self.test_proj3.slug}/")
        self.assertInHTML(
            f'<small><a class="float-start" href={self.test_proj2.get_absolute_url()}><i class="bi bi-chevron-left"></i> {self.test_proj2.title}</a></small>',
            r.content.decode("utf-8"),
        )


class TestProjectMoveAjax(MoveBaseAbstract, TestCase):
    model_class = Project
    base_url = "/ajax/move-project/"

    def _get_objects(self):
        return (self.test_proj1, self.test_proj2)


class TestImageMoveAjax(MoveBaseAbstract, TestCase):
    model_class = Image
    base_url = "/ajax/move-image/"

    def _get_objects(self):
        return (self.proj1_img1, self.proj1_img2)
