from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apis.models.user_profile import UserProfile
from apis.models.competition import Competition
from apis.models.ticket import Ticket
from django.db import transaction
import itertools
import string

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=Competition)
def store_original_ticket_config(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Competition.objects.get(pk=instance.pk)
        instance._original_ticket_config = {
            'ticket_letter_limit': old_instance.ticket_letter_limit,
            'tickets_per_letter': old_instance.tickets_per_letter
        }
    else:
        instance._original_ticket_config = None
        
@receiver(post_save, sender=Competition)
def generate_or_update_tickets(sender, instance, created, **kwargs):

    should_generate = False

    if created:
        should_generate = True
    else:
        original = getattr(instance, '_original_ticket_config', None)
        if original:
            if (
                instance.ticket_letter_limit != original['ticket_letter_limit']
                or instance.tickets_per_letter != original['tickets_per_letter']
            ):
                should_generate = True

    if should_generate:
        # Delete old tickets
        Ticket.objects.filter(competition=instance).delete()

        letter_limit = instance.ticket_letter_limit
        per_letter = instance.tickets_per_letter

        # Generate allowed letters
        if letter_limit > 1:
            allowed_letters = [''.join(t) for t in itertools.product(string.ascii_uppercase, repeat=letter_limit)]
        else:
            allowed_letters = list(string.ascii_uppercase)

        allowed_letters = allowed_letters[:26**letter_limit]

        number_length = len(str(per_letter - 1))  # for zfill

        for letter in allowed_letters:
            for i in range(per_letter):
                ticket_number = f"{letter}{str(i).zfill(number_length)}"
                Ticket.objects.create(competition=instance, ticket_number=ticket_number)