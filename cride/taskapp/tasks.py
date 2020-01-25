""" Celery tasks. """

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

# Celery
from celery.decorators import task, periodic_task

# Model
from cride.users.models import User
from cride.rides.models import Ride

# Utilities
from datetime import timedelta
import jwt


def gen_verification_token(user):
    """ Create JWT token that the user can usen to very its account. """
    exp_date = timezone.now() + timedelta(3)
    paylod = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation',
    }
    token = jwt.encode(paylod, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """ Send account verification link to given a user. """
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = f'Welcome @{user}! Verify your account to start using Comparte Ride'
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {
            'token': verification_token,
            'user': user,
        }
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


# @periodic_task(name='disable_finished_ride', run_every=timedelta(seconds=5))
# def disable_finished_ride():
#     """ Disable finished rides. """
#     now = timezone.now()
#     offset = now + timedelta(minutes=5)

#     # Udate rides that have already finished
#     rides= Ride.objects.filter(
#         arrival_date__gte=now,
#         arrival_date__lte=offset,
#         is_active=True
#     )
#     rides.update(is_active=False)
