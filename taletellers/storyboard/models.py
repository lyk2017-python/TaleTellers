from django.db import models


class Post(models.Model):
    """This class arranges user posts. A post might contain a title or content but it can't contain
    both. If a post has a title, that post must be parent of other posts. Content posts must be
    child of title posts."""
    title = models.CharField(max_length=100, blank=True, null=True)     # unique=True might be added
    content = models.CharField(max_length=140)
    creation_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")

    def __str__(self):
        # returns the id and the title of the Post class's objects when it's requested on manage.py's shell
        return "#{0} {1}".format(self.id, self.title)

    def get_parents(self, exclude_self=False):
        story = self
        story_list = []
        while story.parent is not None:
            story_list.append(story)
            story = story.parent
        else:
            story_list.append(story)
        story_list.reverse()
        if exclude_self:
            story_list.pop(-1)
        return story_list

    class Meta:
        get_latest_by = "creation_time"
        unique_together = ("content", "parent")