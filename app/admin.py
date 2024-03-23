from django.contrib import admin
from .models import Poll, Voter, Candidate

class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_votes', 'created_at', 'updated_at')

class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'nid', 'image', 'status', 'created_at', 'updated_at')

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user','poll',  'votes', 'created_at', 'updated_at')

admin.site.register(Poll, PollAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Candidate, CandidateAdmin)
