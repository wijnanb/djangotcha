from django.contrib import admin
from models import Person, Assassination


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'github_user_id', 'is_killed', 'secret_word')
admin.site.register(Person, PersonAdmin)


class AssassinationAdmin(admin.ModelAdmin):
    list_display = ('assassin', 'victim')
admin.site.register(Assassination, AssassinationAdmin)
