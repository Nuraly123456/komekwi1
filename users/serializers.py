from rest_framework import serializers
from .models import CustomUser, Pricing
from .models import Rating
from .models import Schedule


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'rating']
        read_only_fields = ['rating']


# Добавляем недостающий UserSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']


class PricingSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Pricing
        fields = ['id', 'role', 'role_display', 'hourly_rate', 'bonus_percentage']


class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.ReadOnlyField(source='rater.username')
    employee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Rating
        fields = ['id', 'rater', 'employee', 'score', 'comment', 'created_at']


class ScheduleSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.username')

    class Meta:
        model = Schedule
        fields = ['id', 'employee', 'employee_name', 'date', 'start_time', 'end_time', 'note']

