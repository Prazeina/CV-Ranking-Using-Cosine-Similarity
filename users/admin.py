from .models import Profile
from django.contrib import admin
from .models import User


class UsersAdmin(admin.ModelAdmin):

    list_display = [
        'username',
        'email',
    ]

    class Meta:
        model = User


admin.site.register(Profile)
admin.site.register(User, UsersAdmin)
