from django.contrib.auth.models import User
from djangotcha.models import Person


def stats(request):
    total = User.objects.count()
    killed = Person.objects.filter(is_killed=True).count()
    alive = total - killed

    stats = {
        'total': total,
        'killed': killed,
        'alive': alive,
        'killed_percent': round(killed/total)*100,
        'alive_percent': round(alive/total)*100,
    }

    return {
        'stats': stats
    }

