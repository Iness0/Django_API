import logging

import requests
from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
# from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
# from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


logger = logging.getLogger(__name__)


class HelloView(APIView):
    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.or_g/delay/2')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('Httpbin offline')
        return render(request, {'name': data})
