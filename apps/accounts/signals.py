from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, TravelerProfile, ProviderProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'provider':
            ProviderProfile.objects.get_or_create(
                user=instance,
                defaults={'business_name': f"{instance.username.title()} Travel Services"}
            )
        else:
            TravelerProfile.objects.get_or_create(user=instance)
