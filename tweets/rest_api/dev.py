from rest_framework import authentication
from django.contrib.auth.models import User

class DevAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        qs = User.objects.filter(id=1)
        user = qs.order_by("?").first()
        return (user, None)