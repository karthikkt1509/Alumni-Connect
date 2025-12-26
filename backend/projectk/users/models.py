from django.db import models

# Create your models here.
# users/models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group_name = f"group_{self.username}"
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)
    def __str__(self):
        return self.username
class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
    

from django.db import models
from django.conf import settings
class JobPosting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who posted the job
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    
    
    apply_link = models.URLField(max_length=500, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models

class Question(models.Model):
    source = models.CharField(max_length=255)  # Question Source (Book, Exam, etc.)
    category = models.CharField(max_length=100)  # Subject Name
    question_text = models.TextField()  # Full Question Text
    tags = models.CharField(max_length=255, blank=True)  # Tags
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.question_text[:50]  # Display first 50 chars


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Related Question
    answer_text = models.TextField()  # Answer Content
    upvotes = models.PositiveIntegerField(default=0)  # Upvote Count
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    upvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvoted_answers", blank=True)

    def __str__(self):
        return self.answer_text[:50]
class UserUpvote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')  # Ensure one upvote per answer per user

    def __str__(self):
        return f"{self.user.username} upvoted {self.answer.id}"