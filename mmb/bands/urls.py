from django.conf.urls import patterns, url, include
from rest_framework import routers

from bands.views import BandMemberViewset, BandVacancyViewset, \
    BandViewset, BandFollowersViewset, UserBandMemberViewset


router = routers.DefaultRouter()
router.register(r'band', BandViewset)
router.register(r'vacancy', BandVacancyViewset)
router.register(r'follower', BandFollowersViewset)
router.register(r'member', BandMemberViewset)
router.register(r'user', UserBandMemberViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^invite/$', BandMemberViewset.as_view({"get": "invite"})),
]

