""" Invitations tests. """

# Django
from django.test import TestCase

# Models
from cride.circles.models import Invitation, Circle
from cride.users.model import User


class InvitationsManagerTestCase(TestCase):
    """ Invitations manager Test Case. """

    def setUp(self):
        """ Test case setup. """
        self.user = User.objects.create(
            first_name='Nicolas',
            last_name='Restrepo',
            email='me@nrestrepo05.com',
            username='nrestrepo05',
            password='admin12345'
        )
        self.circle = Circle.objects.create(
            name='Platzi Bogotá',
            slug_name='platzi-bogota',
            about='oficina de Platzi en Bogotá',
            verified=True
        )

    def test_code_generation(self):
        """ Random codes should be generated automatically. """
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        print(invitation.code)

