from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Voter(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter')
    image = models.ImageField(upload_to='', default='avatar.png')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    nid = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Candidate(BaseModel):
    user = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='voter')
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='candidates')
    votes = models.IntegerField(default=0)

    @property
    def image(self):
        return self.user.image

    def __str__(self):
        return self.user.user.username


class Poll(BaseModel):
    title = models.CharField(max_length=100, default='')
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
