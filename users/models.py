from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter'),
        ('cleaner', 'Cleaner'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Pricing(models.Model):
    role = models.CharField(max_length=10, choices=CustomUser.ROLE_CHOICES, unique=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Баға"
        verbose_name_plural = "Бағалар"

    def __str__(self):
        return f"{self.get_role_display()}: {self.hourly_rate}₸/сағ (+{self.bonus_percentage}%)"

class Rating(models.Model):
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')  # кім қойды
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_ratings')  # кімге
    score = models.IntegerField()  # 1-5 арасы
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Автоматты түрде қызметкердің орташа рейтингін жаңарту
        all_scores = [r.score for r in self.employee.received_ratings.all()]
        avg_score = sum(all_scores) / len(all_scores)
        self.employee.rating = round(avg_score, 2)
        self.employee.save()

    def __str__(self):
        return f"{self.rater} → {self.employee} : {self.score}"


class Schedule(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    note = models.CharField(max_length=255, blank=True, null=True)  # мысалы: "тазалық", "ас үй"

    def __str__(self):
        return f"{self.employee.username} | {self.date} | {self.start_time}-{self.end_time}"
