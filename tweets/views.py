from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(["GET"])
def tweet_list_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    serializer = TweetSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
# @authentication_classes([SessionAuthentication])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(["GET"])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    obj = Tweet.objects.get(pk=tweet_id) or None
    if not obj:
        return Response({}, status=404)
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    obj = Tweet.objects.get(pk=tweet_id) or None
    if not obj:
        return Response({"Tweet not found!"}, status=404)
    elif request.user != obj.user:
        return Response({"message": "You can't delete this tweet"}, status=401)
    obj.delete()
    return Response({}, status=204)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
        actions are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        obj = Tweet.objects.get(pk=tweet_id) or None
        if not obj:
            return Response({"Tweet not found!"}, status=404)
        if action == "like":
            obj.likes.add(request.user)
        elif action == "unlike":
            obj.likes.remove(request.user)        
        elif action == "retweet":
            pass 
        return Response({"action is succesfully done."}, status=200)












def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html")

def tweet_list_view_pure_django(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweets_list = [qs.serialize() for qs in queryset]
    data = {
        "isUser": False, 
        "response": tweets_list,
    }
    return JsonResponse(data)

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(obj.serialize(), status=201)
    if form.errors:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(form.errors, status=400)
    form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    data = {}
    try: 
        obj = Tweet.objects.get(id= tweet_id)
        data["id"] = obj.id
        data["content"] = obj.content
        status = 200
    except:
        data["message"] = "Tweet Not Found, you probably entered wrong tweet id"
        status = 404
    
    return JsonResponse(data, status= status)