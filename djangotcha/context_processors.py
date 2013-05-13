from django.contrib.auth.models import User
from djangotcha.models import Person


def stats(request):
    total = User.objects.count()
    killed = Person.objects.filter(is_killed=True).count()
    alive = total - killed

    stats = {
        'total': total,
        'killed': killed,
        'alive': alive
    }

    return {
        'stats': stats
    }

