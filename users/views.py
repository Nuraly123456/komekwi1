from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Pricing, Rating, Schedule
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RatingSerializer
from rest_framework import filters
from rest_framework import permissions
from .permissions import IsAdminUserOnly
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from datetime import timedelta
from rest_framework import serializers
from users.models import Schedule
from .serializers import (
    RegisterSerializer,
    CustomUserSerializer,
    UserSerializer,
    PricingSerializer,
    ScheduleSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=201)
        return Response(serializer.errors, status=400)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = CustomUser.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }, status=200)
            return Response({'error': 'Invalid credentials'}, status=400)
        return Response({'error': 'Please provide username and password'}, status=400)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class PricingViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class UserWithPricingView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_data = CustomUserSerializer(instance).data

        try:
            pricing = Pricing.objects.get(role=instance.role)
            user_data['pricing'] = {
                'hourly_rate': float(pricing.hourly_rate),
                'bonus_percentage': float(pricing.bonus_percentage)
            }
        except Pricing.DoesNotExist:
            user_data['pricing'] = None

        return Response(user_data)

    @action(detail=False, methods=['GET'])
    def by_role(self, request):
        role = request.query_params.get('role')
        if role:
            users = CustomUser.objects.filter(role=role)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response([])


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rater=self.request.user)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')  # ?role=chef
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUserOnly]  # Тек админдерге рұқсат

    def perform_create(self, serializer):
        serializer.save(rater=self.request.user)


class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Schedule.objects.all()
        return Schedule.objects.filter(employee=user)

    def perform_create(self, serializer):
        serializer.save()

    print(Schedule.objects.all())

class TopWorkersView(generics.ListAPIView):
    serializer_class = serializers.Serializer  # Custom Response
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Жұмысшылардың жұмыс уақыттарын суммалау үшін сұрау
        durations = (
            Schedule.objects.annotate(
                duration=ExpressionWrapper(
                    F('end_time') - F('start_time'),
                    output_field=DurationField()
                )
            )
            .values('employee__username')
            .annotate(total_duration=Sum('duration'))
            .order_by('-total_duration')
        )

        result = [
            {
                "employee": entry['employee__username'],
                "total_hours": round(entry['total_duration'].total_seconds() / 3600, 2)
            }
            for entry in durations
        ]

        # Сұраныстың нәтижесін қайтарады
        return result
