import random
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import timedelta


def send_email(email, code):
    pass


class UserManager(BaseUserManager):
    def save_send_verify_code(self, user):
        verify_code = random.randint(123456, 987654)
        user.verify_code = str(verify_code)
        user.save()
        send_email(user.email, verify_code)

    def is_exist_user(self, email=None, pk=None):
        try:
            if email:
                return self.get(email=email)
            if pk:
                return self.get(id=pk)
        except self.model.DoesNotExist:
            return None

    def check_verify_code(self, email, verify_code, password):
        user = self.is_exist_user(email=email)
        if user:
            if user.verify_code != verify_code:
                return {"error": "verify code is not correct "}
            if user.sent_at + timedelta(minutes=2) < timezone.now():
                return {"error": "time ended "}
            if not user.is_active:
                Profile(user=user).save()
                user.is_active = True
            user.set_password(password)
            user.save()
            return {"success": "user activated"}
        return {"error": "user whit this email not exist"}

    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=self.normalize_email(email), is_admin=True, is_active=True)
        user.set_password(password)
        user.save()
        Profile(user=user).save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    verify_code = models.CharField(max_length=6)
    sent_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return f'{self.first_name}  {self.first_name}'

