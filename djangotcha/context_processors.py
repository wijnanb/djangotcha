from django.contrib.auth.models import User
from djangotcha.models import Person


def stats(request):
    total = User.objects.filter(is_superuser=False).count()
    killed = Person.objects.filter(is_killed=True).count()
    alive = total - killed

    stats = {
        'total': total,
        'killed': killed,
        'alive': alive,
        'killed_percent': 0 if total==0 else round(float(killed)/float(total)*100),
        'alive_percent': 0 if total==0 else round(float(alive)/float(total)*100),
    }

    return {
        'stats': stats
    }

