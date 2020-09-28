from django.contrib import admin

# Register your models here.
from outdoorx.forms import LocationForm
from outdoorx.models import Query, Location, Faction,Image, Comment

admin.site.register(Location)
admin.site.register(Faction)
admin.site.register(Image)
admin.site.register(Query)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'body', 'location', 'date_added', 'active')
    list_filter = ('active', 'date_added')
    search_fields = ('owner', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)