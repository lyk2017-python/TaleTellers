from storyboard.models import Post


def post_processor(request):
    return {"post": Post.objects.all()}
