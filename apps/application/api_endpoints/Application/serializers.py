from rest_framework import serializers
from apps.application.models import  Application, Branch, Speciality, Specialist, Equipment, ApplicationBranch

class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'user', 'full_name', 'phone', 'email', 'document_type', 'file', 'status', 'app_id', 'created_at', 'updated_at')
        
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'full_name', 'phone', 'email', 'document_type', 'file', 'status','app_id','created_at', 'updated_at')
        

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ("id", "name")


class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ("id", "full_name", "speciality")


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "name", "speciality")


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ("id", "name", "address")


class ApplicationBranchSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    specialities = serializers.PrimaryKeyRelatedField(queryset=Speciality.objects.all(), many=True)
    specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, required=False)
    equipments = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), many=True, required=False)

    class Meta:
        model = ApplicationBranch
        fields = ("branch", "specialities", "specialists", "equipments")


class ApplicationFormSerializer(serializers.ModelSerializer):
    # Asosiy Application fieldlari
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    document_type = serializers.CharField(max_length=100)
    file = serializers.FileField(required=True)

    # Bog‘langan branch va boshqa ma’lumotlar
    branches = ApplicationBranchSerializer(many=True)

    class Meta:
        model = Application
        fields = [
            "full_name", "phone", "email", "document_type", "file",
            "branches"
        ]

    def update(self, instance, validated_data):
        branches_data = validated_data.pop("branches", [])

        # Asosiy maydonlarni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.status = "sent"
        instance.save()

        # Eski branchlarni tozalash
        instance.branches.all().delete()

        # Yangi branchlarni saqlash
        for branch_data in branches_data:
            specialities = branch_data.pop("specialities", [])
            specialists = branch_data.pop("specialists", [])
            equipments = branch_data.pop("equipments", [])

            app_branch = ApplicationBranch.objects.create(
                application=instance,
                branch=branch_data["branch"],
            )
            app_branch.specialities.set(specialities)
            app_branch.specialists.set(specialists)
            app_branch.equipments.set(equipments)

        return instance

    