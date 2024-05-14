from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from smtplib import SMTPException
from django.conf import settings
from django.conf import settings
import logging

logger = logging.getLogger(__name__)



def notify_daard_user(receiver=[], template='', instance='', title=''):

    if settings.EMAIL_ENABLE is False:
        logger.info("EMAIL_ENABLE is false. Returning")
        return

    #msg_html = render_to_string('./email/admin_notice_created.txt', {'instance': instance.pk})
    msg_plain = render_to_string(template, {'instance': instance})

    try:
        send_mail(
            title,
            msg_plain,
            settings.DEFAULT_FROM_EMAIL,
            receiver
        )
    except BadHeaderError:  # If mail's Subject is not properly formatted.
        logger.error('Invalid header found.')
    except SMTPException as e:  # It will catch other errors related to SMTP.
        logger.error('There was an error sending an email.' + e)
    except:  # It will catch All other possible errors.
        logger.error("Mail Sending Failed!")
