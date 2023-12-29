from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

class TextAmountManager(models.Manager):
    def remove_old_objects(self, limit):
        # excess objects amount
        excess_count = self.count() - limit
        if excess_count > 0:
            oldest_object_pks = self.order_by('created_at')[:excess_count].values_list('pk', flat=True)           
            self.filter(pk__in=oldest_object_pks).delete()

class TextModel(models.Model):
    # Old texts get deleted when the amount exceeds the limit
    username = models.CharField(max_length=50)
    text_data = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TextAmountManager()

    def save(self, *args, **kwargs):
        # message limit after which deletion occurs
        limit = 10
        if TextModel.objects.count() >= limit:
            TextModel.objects.remove_old_objects(limit)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.text_data
    
class MessageModel(models.Model):
    message_text = models.CharField(max_length=255)
    message_sender = models.CharField(max_length=25)
    message_target = models.CharField(max_length=25)
    def __str__(self):
        return self.message_sender + ": " + self.message_text  + " -> " + self.message_target
    
class PwChangeModel(models.Model):
    password = models.CharField(max_length=255)
    new_password = models.CharField(max_length=255)

class MessageGetModel(models.Model):
    sender = models.CharField(max_length=50)

class PersonalInfoModel(models.Model):
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)

class MessageLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_message_time = models.DateTimeField(null=True, blank=True)
    message_count = models.IntegerField(default=0)

    def can_send_message(self, max_messages_per_minute=3):
        if self.last_message_time is not None:
            time_difference = timezone.now() - self.last_message_time
            if time_difference.total_seconds() > 60:
                self.message_count = 0

        if self.message_count >= max_messages_per_minute:
            return False

        if self.last_message_time is not None:
            time_difference = timezone.now() - self.last_message_time
            if time_difference.total_seconds() > 5:
                return True

        return True
    def update_message_count(self):
        self.message_count += 1
        self.last_message_time = timezone.now()
        self.save()

class TextLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_text_time = models.DateTimeField(null=True, blank=True)
    text_count = models.IntegerField(default=0)

    def can_send_text(self, max_messages_per_minute=3):
        if self.last_text_time is not None:
            time_difference = timezone.now() - self.last_text_time
            if time_difference.total_seconds() > 60:
                self.text_count = 0

        if self.text_count >= max_messages_per_minute:
            return False
        
        if self.last_text_time is not None:
            time_difference = timezone.now() - self.last_text_time
            if time_difference.total_seconds() > 5:
                return True

        return True

    def update_text_count(self):
        self.text_count += 1
        self.last_text_time = timezone.now()
        self.save()