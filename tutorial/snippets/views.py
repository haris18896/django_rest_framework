# Generic Class Based View
from snippets.permissions import IsOwnerOrReadOnly
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions    
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import renderers, viewsets
from rest_framework.reverse import reverse
# Viewsets class based view
"""In the snippets/urls.py file we bind our ViewSet classes into a set of concrete views."""
# Replacing the Userlist and UserDetail with single UserViewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # This viewset automatically provide 'list' and 'retrieve' actions
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# Next we're going to replace the SnippetList, SnippetDetail and SnippetHighlight view classes. We can remove the three views, and again replace them with a single class.
class SnippetViewSet(viewsets.ModelViewSet):
    # This viewset automatically provides `list`, `create`, `retrieve`,`update` and `destroy` actions.
    # Additionally we also provide an extra `highlight` action.
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
@api_view(['GET'])
# Two things should be noticed here.
# First, we're using REST framework's reverse function in order to return fully-qualified URLs;
# second, URL patterns are identified by convenience names that we will declare later on in our snippets/urls.py.
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
    
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def perform_create(self, serializer):   # The create() method of our serializer will now be passed an additional 'owner' field, along with the validated data from the request.
#         serializer.save(owner=self.request.user)
    
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]



    
    
# We'll also add a couple of views to views.py. We'd like to just use read-only views for the user representations, so we'll use the ListAPIView and RetrieveAPIView generic class-based views.
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer