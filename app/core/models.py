from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        # test for a non value/no email is passed
        if not email:
            raise ValueError('Users must have email addresses')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # normalize_email() function comes with BaseUserManager
        user.set_password(password)
        """helps with managing multiple db"""
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        # as we will be creating superuser using commandline we don't need the
        # extra_fields
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # the is_superuser field is included with permissionsmixin
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """assign user manage to objects attribute"""
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    """Category of a painting """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(  # foreign key of the user object which could be
        # done by refereing to the user
        settings.AUTH_USER_MODEL,  # used from the settings imported on top
        on_delete=models.CASCADE,  # if the user is deleted the category will
        # be deleted as well
    )

    def __str__(self):  # retrun the string representation
        return self.name


class Supply(models.Model):
    """Supply to be used in a painting"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Painting(models.Model):
    """Painting object"""
    user = models.ForeignKey(  # one painting can belong to only one user
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # every field will be a column in the data table
    title = models.CharField(max_length=255)
    painting_create_date = models.DateField()
    # price = models.DecimalField(max_digits=5, decimal_places=2)
    link_to_instragram = models.CharField(max_length=255, blank=True)
    # link field is optional, in a char field user can enter a null value,
    # thus blank= ture will set the link as a blank string
    category = models.ManyToManyField('Category')
    supply = models.ManyToManyField('Supply')
    # the models are passed as strings , not by class because in that case
    # the classes has to be in order which will not be handy when we have
    # many classes
    # many-to-many represets the many-to-many replationship in between models

    def __str__(self):
        return self.title
# Create your models here.
