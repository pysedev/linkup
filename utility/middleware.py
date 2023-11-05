from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ObjectDoesNotExist
from post.models import Post
from comment.models import Comment
from tag.models import Tag


class IsObjectExistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        destinations = ['/post', '/tag', '/comment']
        if any([request.path.startswith(path) for path in destinations]) and request.path.count('/') == 3:
            destination = request.path.split("/")[1]
            pk = int(request.path.split("/")[-2])
            try:
                if destination == 'post':
                    obj = Post.custom_objects.get(id=pk)

                if destination == 'tag':
                    obj = Tag.objects.get(id=pk)

                if destination == 'comment':
                    obj = Comment.objects.get(id=pk)

                my_request = request.GET.copy()
                my_request['object'] = obj
                request.GET = my_request
                response = self.get_response(request)
                return response
            except ObjectDoesNotExist:
                response = Response(
                    data={"errors": "Object does not exist"},
                    status=status.HTTP_403_FORBIDDEN
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
        response = self.get_response(request)
        return response
