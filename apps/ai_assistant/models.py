from django.db import models
from apps.accounts.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ChatSession {self.session_id} ({self.user.username if self.user else 'Guest'})"


class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('assistant', 'AI Travel Assistant'),
    )

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.sender}] {self.content[:40]}..."
