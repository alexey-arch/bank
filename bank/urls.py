from rest_framework import routers

from .views import UserViewSet, AccountView

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'account', AccountView, basename='users')

urlpatterns = router.urls
