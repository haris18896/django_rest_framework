# Now that we've got some users to work with, we'd better add representations of those users to our API
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset = Snippet.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = User
        fields = ['id', 'username','owner', 'snippets']     # Because 'snippets' is a reverse relationship on the User model, it will not be included by default when using the ModelSerializer class, so we needed to add an explicit field for it
        

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
        