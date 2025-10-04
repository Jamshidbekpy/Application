from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.application.models import Branch, Speciality, Specialist, Equipment, ApplicationBranch
from apps.application.api_endpoints.Application.serializers import (
    BranchSerializer, SpecialitySerializer,
    SpecialistSerializer, EquipmentSerializer
)


# 1) GET /api/locations/ → filiallar
class LocationListView(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]


# 2) GET /api/specializations/ → ixtisosliklar
#    GET /api/specializations/?location={id}
class SpecializationListView(generics.ListAPIView):
    serializer_class = SpecialitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Speciality.objects.all()
        location_id = self.request.query_params.get("location")

        if location_id:
            # Faqat tanlangan branchga bog‘langan specialities larni chiqaramiz
            queryset = queryset.filter(applicationbranch__branch_id=location_id).distinct()

        return queryset


# 3) GET /api/specializations/{id}/required-specialists/
class RequiredSpecialistsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        specialists = Specialist.objects.filter(speciality_id=id)
        serializer = SpecialistSerializer(specialists, many=True)
        return Response(serializer.data)


# 4) GET /api/specializations/{id}/required-equipments/
class RequiredEquipmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        equipments = Equipment.objects.filter(speciality_id=id)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)


__all__ = [
    "LocationListView", "SpecializationListView", "RequiredSpecialistsView", "RequiredEquipmentsView"
]