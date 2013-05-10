from django.core.management.base import BaseCommand, CommandError
from djangotcha.models import Person
import random

class Command(BaseCommand):
    args = ''
    help = 'Assign random targets to everyone'

    def handle(self, *args, **options):
        persons = Person.objects.all()

        indices = range(len(persons))
        random.shuffle(indices)

        # you cannot target yourself
        # first make sure last one is not himself
        last = len(persons)-1
        while indices[last] == last:
            self.stdout.write('last one is himself')
            random.shuffle(indices)

        for i in range(len(persons)):
            t = indices[i]

            if t == i:  # auto-target discovered, switch with next person
                self.stdout.write('auto-target discovered, switch with next person')
                indices[i] = indices[i+1]
                indices[i+1] = t


        # save to database
        i = 0
        for p in persons:
            index = indices[i]
            target = persons[index]

            self.stdout.write('assigned: %s #\'== ~> %s' % (p,target))

            p.target = target
            p.save()
            i += 1

        self.stdout.write('Successfully assigned targets')