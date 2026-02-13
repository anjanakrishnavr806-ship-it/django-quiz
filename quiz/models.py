from django.db import models
from django.contrib.auth.models import User

# Profile for distinguishing student and teacher
class Profile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

# Quiz category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title

# Questions
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

# Choices
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# Student answers
class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
