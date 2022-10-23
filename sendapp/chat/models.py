from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    username = models.CharField(max_length = 10, unique = True, primary_key=True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 20)

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

class Message(models.Model):
    description = models.TextField()
    sender_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    timestamp = models.TimeField(auto_now_add=True)

class PublicKey(models.Model):
    owner = models.TextField()
    value = models.TextField()