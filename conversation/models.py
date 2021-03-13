from django.db import models
from userprofile.models import Profile
# Create your models here.


class Conversation(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='conversations')
    user_with = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Conversation between {owner.user.full_name} and {user_with.user.full_name} '


class Message(models.Model):
    user_from = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sent_messages")
    user_to = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="messages")
    sent = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    read = models.BooleanField(default=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Message from {self.user_from.user.full_name}'

    class Meta:
        ordering = ['-sent']
