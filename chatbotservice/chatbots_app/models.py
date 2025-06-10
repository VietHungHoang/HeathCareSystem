import uuid
from django.db import models

class ChatSession(models.Model):
    BOT_TYPE_CHOICES = [
        ('CONSULTING', 'Consulting'),
        ('DIAGNOSIS', 'Diagnosis'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    bot_type = models.CharField(max_length=50, choices=BOT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} for user {self.user_id}"

    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-created_at']

class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('USER', 'User'),
        ('BOT', 'Bot'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"

    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']