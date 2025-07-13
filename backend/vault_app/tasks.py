from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from celery import shared_task
from backend.settings import EMAIL_HOST_USER

@shared_task
def send_mail(subject, html_content, text_content, email):
    connection = get_connection()

    email_message = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, {email} ,connection= connection)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    connection.close()
