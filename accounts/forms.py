from django import forms
from .models import Answer, EvaluationForm 

class AnswerForm(forms.ModelForm):  # 回答フォーム
    class Meta:
        model = Answer
        fields = ['reviewee_role', 'question1', 'question2', 'question3']
        labels = {
            'reviewee_role': '被評価者の役職',
            'question1': '与えられた役割を遂行している？',
            'question2': '自分のアイディアを率先して提案している？',
            'question3': 'チームのニーズや疑問に対して迅速に対応しているか？(マネージャー、リーダーのみ)',
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("reviewee_role")
        question3 = cleaned_data.get("question3")

        print(f"デバッグ: reviewee_role = {role}")  # ここでログ出力

        # マネージャー・リーダー以外は質問3を無効にする
        if role in ["general"] and question3 is not None: # 一般を弾く
            self.add_error("question3", "被り評価者がリーダー、マネージャーのみ回答してください")

        return cleaned_data

class EvaluationFormForm(forms.ModelForm):  # （管理者用のフォーム作成）
    class Meta:
        model = EvaluationForm
        fields = ['title']