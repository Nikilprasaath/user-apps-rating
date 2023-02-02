from django.db import models
from django.contrib.auth.models import User

class app(models.Model):
    app_name = models.CharField(max_length=20)
    app_link = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    subcategory = models.CharField(max_length=20)
    points = models.IntegerField()

    def __str__(self):
        return self.app_name

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apps = models.ManyToManyField(app)
    points = models.IntegerField(null= True)

    def __str__(self):
        return self.user.first_name

class tasks(models.Model):
    status_choices = (
        ('pending','pending'),
        ('approved','approved'),
        ('rejected','rejected'),
    )
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    app = models.ForeignKey(app, on_delete= models.CASCADE)
    screenshot = models.ImageField(upload_to='scrn')
    status = models.CharField(max_length=20, choices= status_choices, default='pending', blank=True)

    def __str__(self):
        return "%s | %s" % (self.user, self.app)