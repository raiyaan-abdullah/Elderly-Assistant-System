from rest_framework import routers
from .api import LeadViewSet

router = routers.DefaultRouter()
router.register('api/medicine-history', LeadViewSet, 'medicine_history')

urlpatterns = router.urls