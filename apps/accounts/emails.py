from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import timedelta
import random, threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_email(email):
    if settings.DEBUG:
        EmailMessage(email).start()
    else:
        email.send()


class Util:
    async def send_activation_otp(user):
        subject = "Verify your email"
        code = random.randint(100000, 999999)
        message = render_to_string(
            "email-activation.html",
            {
                "name": user.full_name,
                "otp": code,
            },
        )
        user.otp = code
        user.otpExp = timezone.now() + timedelta(
            seconds=settings.EMAIL_OTP_EXPIRE_SECONDS
        )
        await user.asave()

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        send_email(email_message)

    async def send_password_change_otp(user):
        subject = "Your account password reset email"
        code = random.randint(100000, 999999)
        message = render_to_string(
            "password-reset.html",
            {
                "name": user.full_name,
                "otp": code,
            },
        )
        user.otp = code
        user.otpExp = timezone.now() + timedelta(
            seconds=settings.EMAIL_OTP_EXPIRE_SECONDS
        )
        await user.asave()

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        send_email(email_message)

    def password_reset_confirmation(user):
        subject = "Password Reset Successful!"
        message = render_to_string(
            "password-reset-success.html",
            {
                "name": user.full_name,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        send_email(email_message)

    @staticmethod
    def welcome_email(user):
        subject = "Account verified!"
        message = render_to_string(
            "welcome.html",
            {
                "name": user.full_name,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        send_email(email_message)
