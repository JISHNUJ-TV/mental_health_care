from django.db import models

class register(models.Model):
 
    name=models.CharField(max_length=150)
    phone=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)

class doctor(models.Model):
 
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)

class chats(models.Model):
 
    user_id=models.CharField(max_length=150)
    d_chat=models.CharField(max_length=150)
    u_chat=models.CharField(max_length=150)
    datetme=models.CharField(max_length=150)