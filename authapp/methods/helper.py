from django.core.mail import send_mail
from blog import settings

def sent_to_mail(request, address, message):
    message = f"Hello {address}. \n\n{message}"
    subject = 'Confirmation Code'
    address = address
    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])