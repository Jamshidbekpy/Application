from apps.base.models import BaseModel
from rest_framework import generics, permissions
from apps.application.models import Application
from apps.application.api_endpoints.Application.serializers import ApplicationListSerializer, ApplicationCreateSerializer, ApplicationFormSerializer
from rest_framework.response import Response
from rest_framework import status

class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Application.objects.filter(is_active=True)
        status_param = self.request.query_params.get("status")

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationCreate(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class ApplicationForm(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # faqat draft bo‘lsa yuborishga ruxsat
        if instance.status != "draft":
            return Response(
                {"error": "Faqat qoralama (draft) arizani yuborishingiz mumkin."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        return Response(
            {"success": "Ariza yuborildi", "data": ApplicationFormSerializer(instance).data},
            status=status.HTTP_200_OK
        )
        

class ApplicationDetail(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

__all__ = ["ApplicationList", "ApplicationCreate", "ApplicationForm", "ApplicationDetail"]