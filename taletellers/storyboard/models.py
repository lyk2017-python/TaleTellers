from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)         # unique=True might be added
    content = models.CharField(max_length=140, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")

    def __str__(self):
        # returns the id and the title of the Post class's objects when it's requested on manage.py's shell
        return "#{0} {1}".format(self.id, self.title)
