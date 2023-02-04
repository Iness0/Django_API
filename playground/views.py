from django.shortcuts import render
# from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
# from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('Hello')
    return render(request)
