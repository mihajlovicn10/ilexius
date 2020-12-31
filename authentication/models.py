from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **druga_polja):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(email=self.normalize_email(email), **druga_polja)

        user_obj.set_password(password)
    
        
        
        user_obj.is_admin = False
        user_obj.has_module_perms = True
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email,password, **druga_polja):
        user_obj = self.create_user(email,password, **druga_polja)
        user_obj.is_admin = True
        user_obj.login_count = 0
        user_obj.login_attempt = 0
        user_obj.is_superuser = True
        user_obj.has_module_perms = True
        user_obj.is_staff = True
        user_obj.save(using=self._db)
        return user_obj






class User(AbstractUser):
    login_count = models.IntegerField(null=True)
    login_attempt = models.IntegerField(null=True)
    objects = UserManager()
    REQUIRED_FIELDS = ['password', 'email', 'first_name', 'last_name']
    def __str__(self): 
        return self.username
# Create your models here.
