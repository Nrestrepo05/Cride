# Generated by Django 2.2.9 on 2020-01-14 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='remaining_invitation',
            new_name='remaining_invitations',
        ),
    ]
