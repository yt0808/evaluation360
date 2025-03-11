from django.db import models
from django.contrib.auth.models import User

class Answer(models.Model):
    ROLE_CHOICES = [
        ('general', '一般'),
        ('manager', 'マネージャー'),
        ('leader', 'リーダー'),
    ]
    
    SCORE_CHOICES = [
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
        (None, 'わからない')
    ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer_answers")  # 評価者
    reviewee_name = models.CharField(max_length=255)  # 被評価者の名前（記述式）
    reviewee_role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # 役職（選択式）
    question1 = models.IntegerField(choices=SCORE_CHOICES)  # 質問1
    question2 = models.IntegerField(choices=SCORE_CHOICES)  # 質問2
    question3 = models.IntegerField(choices=SCORE_CHOICES, null=True, blank=True)  # 質問3（マネージャー/リーダーのみ）

    created_at = models.DateTimeField(auto_now_add=True)  # 回答日時

    def __str__(self):
        return f"{self.reviewer} → {self.reviewee_name} ({self.reviewee_role})"
