from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Введите пожалуйста ваш email!")

        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,  password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have status is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have status is_superuser=True')
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=40, blank=True)
    objects = UserManager()
    username = models.CharField(max_length=255)
    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception('code is invalid')
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])



