from django import forms
from .models import Answer

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['reviewee_name', 'reviewee_role', 'question1', 'question2', 'question3']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("reviewee_role")
        question3 = cleaned_data.get("question3")

        # マネージャー・リーダー以外は質問3を無効にする
        if role in ["general"] and question3 is not None:
            self.add_error("question3", "一般の人には質問3は不要です。")

        return cleaned_data
