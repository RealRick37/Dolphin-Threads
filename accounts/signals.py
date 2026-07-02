from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@receiver(post_save, sender=CustomUser)
                  #CustomUser, user, new record boolean created=True, etc data
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):

    if created and instance.email:

        html_content = render_to_string("emails/welcome.html", {"user": instance})

        email = EmailMultiAlternatives(subject="خوش اومدی :)", body="خوش اومدی به فروشگاه ما", to=[instance.email])

        email.attach_alternative(html_content, "text/html")

        email.send()