from rest_framework import status
from rest_framework.decorators import api_view  # The @api_view decorator for working with function based views., and The APIView class for working with class-based views.
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
                                                # request.POST  # Only handles form data.  Only works for 'POST' method.                                                
@api_view(['GET','POST'])
def snippet_list(request, format=None):         # To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints. Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as http://example.com/api/items/4.json. and then add suffixes to snippets/urls.py
    # list all code snippets or create a new snippet
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)    # # Renders to content type as requested by the client.

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)   # request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if you get an error code wrong. REST framework provides more explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST

# We'll also need a view which corresponds to an individual snippet, and can be used to retrieve, update or delete the snippet.
@api_view(['GET','PUT','DELETE'])
def snippet_detail(request, pk, format=None):
    # retrive, update or delete a code snippet
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Notice that we're no longer explicitly tying our requests or responses to a given content type. request.data can handle incoming json requests, but it can also handle other formats. Similarly we're returning response objects with data, but allowing REST framework to render the response into the correct content type for us.
    
    