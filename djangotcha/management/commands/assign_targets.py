import os
import random
from django.core.management.base import BaseCommand
from djangotcha.models import Person, Assassination
from django.conf import settings


class Command(BaseCommand):
    args = ''
    help = 'Assign random targets to everyone'

    def handle(self, *args, **options):
        Assassination.objects.all().delete()

        persons = Person.objects.filter(user__is_superuser=False).order_by('?')

        secret_words = read()
        random.shuffle(secret_words)

        i = 0
        for p in persons:
            if i == 0:
                target = persons[len(persons)-1]
            else:
                target = persons[i-1]

            self.stdout.write('assigned: %s #\'== ~> %s' % (p,target))

            p.target = target
            p.secret_word = secret_words[i]
            p.is_killed = False
            p.date_killed = None
            p.save()
            i += 1

        self.stdout.write('Successfully assigned targets')


def read():
    current = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current, 'words')
    fh = open(path, 'r')

    words = [line.strip() for line in fh]
    return words

