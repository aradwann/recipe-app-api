from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)


class UserManger(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError("users must have an email address")
        user = self.model(email=self.normalize_email(email),
                          **extra_fields)
        # we use this method becuase the password has to be hashed/encrypted
        user.set_password(password)
        # self._db is used for supporting
        # multiple databases (recommended practice)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates and saves a new super user"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = "email"
