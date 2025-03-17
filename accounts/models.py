from django.db import models
from django.contrib.auth.models import User

class EvaluationForm(models.Model):  
    title = models.CharField(max_length=255, unique=True)  # フォームのタイトル（例：2025年1月評価）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時

    def __str__(self):
        return self.title

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

    evaluation_form = models.ForeignKey(EvaluationForm, on_delete=models.CASCADE)  # どの評価フォームに紐づくか
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewee_answers", default=1)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer_answers")  # 評価者
    reviewer_name = models.CharField(max_length=255)  # 評価者の名前
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewee_answers")  # 被評価者
    reviewee_role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    question1 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    question2 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    question3 = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # 回答日時

    def __str__(self):
        return f"{self.reviewer} → {self.reviewee} ({self.reviewee_role})"
