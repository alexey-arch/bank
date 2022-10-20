from rest_framework import routers

from .views import UserViewSet, AccountView, HistoryView

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'account', AccountView, basename='account')
router.register(r'history', HistoryView, basename='history')

urlpatterns = router.urls
