from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # This makes the gold and user visible in a table list
    list_display = ('user', 'gold')
    # This allows you to edit the gold directly from the list
    list_editable = ('gold',)