from django.core.management.base import BaseCommand, CommandError
from djangotcha.models import Person
from django.conf import settings
import random


class Command(BaseCommand):
    args = ''
    help = 'Assign random targets to everyone'

    def handle(self, *args, **options):
        persons = Person.objects.filter(user__is_superuser=False).order_by('?')

        secret_words = settings.SECRET_WORDS
        random.shuffle(secret_words)

        i = 0
        for p in persons:
            if i == 0:
                target = persons[len(persons)-1]
            else:
                target = persons[i-1]

            secret_word = secret_words[ i % len(secret_words) ]

            self.stdout.write('assigned: %s #\'== ~> %s' % (p,target))

            p.target = target
            p.secret_word = secret_word
            p.is_killed = False
            p.date_killed = None
            p.save()
            i += 1

        self.stdout.write('Successfully assigned targets')