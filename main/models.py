from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def str(self):
        return f"{self.username} ({self.role})"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)  # Short title for the ticket
    description = models.TextField()  # Detailed description of the issue
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')  # Ticket status
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_tickets',
        on_delete=models.CASCADE
    )  # User who created the ticket
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tickets',
        blank=True
    )  # Users assigned to the ticket
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-add timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update timestamp for changes

    def __str__(self):
        return f"{self.title} ({self.status})"