# Now that we've got some users to work with, we'd better add representations of those users to our API
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    class Meta:
        model = Snippet
        fields = ['url','id','highlight', 'owner' ,'title', 'code', 'linenos', 'language', 'style']
        
        
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedIdentityField(many=True, view_name='snippet-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']     # Because 'snippets' is a reverse relationship on the User model, it will not be included by default when using the ModelSerializer class, so we needed to add an explicit field for it
        