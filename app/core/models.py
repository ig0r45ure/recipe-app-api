from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user with password as a username"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class OrgUnit(models.Model):
    """Organizational Unit who is owner of processes or does activities"""
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=3, blank=True, default='')
    is_HQUnit = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Process(models.Model):
    """Business process - element of management architecture"""
    name = models.CharField(max_length=255)
    proc_id = models.CharField(max_length=4)
    is_megaprocess = models.BooleanField(default=False)
    type = models.CharField(max_length=255)
    owner = models.ForeignKey(
        'OrgUnit',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'is_megaprocess': True}
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products are input or output of activities"""
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity is a part of a process performed that has defined
        input and products"""
    name = models.CharField(max_length=255)
    input = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
    )
    process = models.ForeignKey(
        'Process',
        on_delete=models.CASCADE,
        limit_choices_to={'is_megaprocess': False}
    )
    performer = models.ForeignKey(
        'OrgUnit',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
