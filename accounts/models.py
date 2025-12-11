from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CourseRequest(models.Model):
    COURSE=[
        ("web_design", "Основы веб-дизайна"),
        ("database_design", "Основы проектирования баз данных"),
        ("algorithms_programming", "Основы алгоритмизации и программирования"),
    ]
    
    STATUS=[
        ("not_started","Ещё не начал"),
        ("in_progress","Начал"),
         ("finished","Завершил"),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.CharField(max_length=50,choices=COURSE)
    date_start = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS,default="not_started")
    created_at=models.DateTimeField(auto_now_add=True)

    review = models.TextField(blank=True, null=True, verbose_name="Отзыв")

    def __str__(self):
        return f"{self.user.username} - {self.course}"