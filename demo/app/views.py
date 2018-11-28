from rest_framework.decorators import api_view, renderer_classes, APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


@api_view(['get'])
@renderer_classes([JSONRenderer])
def hello(request):
    return Response("Hello World")


class HealthCheck(APIView):
    authentication_classes = []
    versioning_class = None

    def get(self, _):
        return Response({'success': True})