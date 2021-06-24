from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password./home/vikram/Desktop/DJANGO FLAIR TECH/gmailproject
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Registration(models.Model):
    myuser = models.OneToOneField(MyUser, related_name='myuser', on_delete=models.CASCADE)
    make_spam=models.BooleanField(default=False)

    def __str__(self):
        return self.myuser.email



class Gmail(models.Model):
    """ models for email """
    sender = models.ForeignKey(MyUser, related_name='sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(MyUser, related_name='reciever', on_delete=models.CASCADE)
    body = models.TextField()
    subject = models.CharField(max_length=10000)
    is_spam = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    is_trash= models.BooleanField(default=False)




# Create your models here.
