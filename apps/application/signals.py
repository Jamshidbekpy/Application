from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from apps.application.models import Application
from django.conf import settings

@receiver(post_save, sender=Application)
def send_application_notification(sender, instance, created, **kwargs):
    if not created and instance.status == "sent":  # "Yuborildi"
        # Email yuborish
        if instance.email:
            send_mail(
                subject="Arizangiz yuborildi",
                message=f"Assalomu alaykum {instance.full_name}, arizangiz muvaffaqiyatli yuborildi!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        
        # # SMS yuborish (twilio yoki boshqa provider orqali)
        # if instance.phone:
        #     # Masalan Twilio ishlatamiz
        #     from twilio.rest import Client
        #     account_sid = "ACXXXX"   # twilio SID
        #     auth_token = "XXXXXX"    # twilio token
        #     client = Client(account_sid, auth_token)

        #     try:
        #         client.messages.create(
        #             body=f"Assalomu alaykum {instance.full_name}, arizangiz yuborildi!",
        #             from_="+123456789",  # twilio raqam
        #             to=instance.phone
        #         )
        #     except Exception:
        #         pass
