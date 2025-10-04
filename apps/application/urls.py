from django.urls import path
from .api_endpoints import (
    ApplicationList, 
    ApplicationCreate, 
    ApplicationForm, 
    ApplicationDetail,
    LocationListView,
    SpecializationListView,
    RequiredSpecialistsView,
    RequiredEquipmentsView)

urlpatterns = [
    path("applications/", ApplicationList.as_view(), name="application-list"),
    path("applications/create/", ApplicationCreate.as_view(), name="application-create"),
    path("applications/<int:pk>/send/", ApplicationForm.as_view(), name="application-send"),
    path("applications/<int:pk>/", ApplicationDetail.as_view(), name="application-detail"),
]


urlpatterns += [
    path("locations/", LocationListView.as_view(), name="locations-list"),
    path("specializations/", SpecializationListView.as_view(), name="specializations-list"),
    path("specializations/<int:id>/required-specialists/", RequiredSpecialistsView.as_view(), name="required-specialists"),
    path("specializations/<int:id>/required-equipments/", RequiredEquipmentsView.as_view(), name="required-equipments"),
]
