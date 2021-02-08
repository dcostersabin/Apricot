from django.test import TestCase
from users.models import User

__USERNAME__ = "test123"
__PASSWORD_1__ = "testing123"
__EMAIL__ = "test@test.com"


# Create your tests here.
class TestUserCreation(TestCase):
    def test_insert_valid_user(self):
        # test user with valid inputs
        new_user = User()
        new_user.email = __EMAIL__
        new_user.password = __PASSWORD_1__
        new_user.username = __USERNAME__
        new_user.save()
        get_last_user = User.objects.last()
        self.assertEqual(new_user, get_last_user)

    def test_insert_user_without_email(self):
        # test user without email. That should raise value error
        new_user = User()
        new_user.password = __PASSWORD_1__
        new_user.username = __USERNAME__
        new_user.save()
        count = User.objects.count()
        self.assertEqual(count, 1)

    def test_insert_user_without_username(self):
        # test user without username. That should raise value error
        new_user = User()
        new_user.email = __EMAIL__
        new_user.password = __PASSWORD_1__
        new_user.save()
        count = User.objects.count()
        self.assertEqual(count, 1)

    def test_insert_user_without_password(self):
        # test user without password. That should raise value error
        new_user = User()
        new_user.email = __EMAIL__
        new_user.username = __USERNAME__
        new_user.save()
        count = User.objects.count()
        self.assertEqual(count, 1)

    def test_insert_user_with_no_parameters(self):
        # test user without any input. That should also raise value error
        new_user = User()
        new_user.save()
        count = User.objects.count()
        self.assertEqual(count, 1)


if __name__ == '__main__':
    TestUserCreation.main()
