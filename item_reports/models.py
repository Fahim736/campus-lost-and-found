from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):

    TYPE_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(max_length=200)

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    category = models.CharField(max_length=100)

    description = models.TextField()

    location = models.CharField(max_length=200)

    date = models.DateField()

    contact = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='reports/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.item_name



class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology_used = models.CharField(max_length=200)
    github_link = models.URLField(max_length=500)
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title