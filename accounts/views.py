from django.shortcuts import render, redirect,get_object_or_404
from .models import Answer, EvaluationForm
from django.db.models import Avg
from .forms import EvaluationFormForm, AnswerForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
import logging

@login_required
def evaluation_input(request, reviewee_name):
    """評価入力フォーム"""
    latest_form = EvaluationForm.objects.order_by('-created_at').first()

    if latest_form is None:
        return render(request, 'accounts/no_evaluation_form.html')

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.reviewer = request.user  # 現在のログインユーザーを評価者としてセット
            answer.reviewer_name = request.user.username  # 評価者の名前
            try:
                answer.reviewee = User.objects.get(username=reviewee_name)  # 被評価者をセット
            except User.DoesNotExist:
                return render(request, 'accounts/error.html', {'message': '被評価者が存在しません。'})
            
            answer.evaluation_form = latest_form  # 評価フォームをセット
            answer.save()
            return redirect('evaluation_complete')
    else:
        form = AnswerForm()

    return render(request, 'accounts/evaluation_input.html', {
        'form': form,
        'evaluation_form': latest_form,
        'reviewee_name': reviewee_name
    })

@login_required
def home(request):
    """ホーム画面（評価フォーム一覧と評価対象者一覧を表示）"""
    evaluation_forms = EvaluationForm.objects.order_by('-created_at')  # すべてのフォームを取得（新しい順）

    # 被評価者（評価対象者）
    reviewees = User.objects.values_list('username', flat=True)  # DB からユーザー一覧を取得

    return render(request, 'accounts/home.html', {
        'evaluation_forms': evaluation_forms,
        'reviewees': reviewees  # 全員を渡す
    })

@login_required
def evaluation_complete(request):
    """評価完了ページ"""
    return render(request, 'accounts/evaluation_complete.html')

@login_required
def evaluation_result_list(request):
    """評価結果一覧（フォームタイトルごとに表示）"""
    user = request.user

    # 自分が被評価者となっている回答を取得
    evaluations = Answer.objects.filter(reviewee=user).order_by('-created_at')

    # フォームごとにグループ化
    evaluation_groups = {}
    for eval in evaluations:
        form = eval.evaluation_form  # フォームオブジェクト
        if form.title not in evaluation_groups:
            evaluation_groups[form.title] = form

    return render(request, 'accounts/evaluation_result_list.html', {
        'evaluation_groups': evaluation_groups,
    })

@login_required
def evaluation_result_detail(request, form_title):
    """特定の評価フォームの詳細（平均スコア、評価データ）を表示"""
    user = request.user

    # 評価フォームを取得（存在しない場合はエラーページを表示）
    evaluation_form = get_object_or_404(EvaluationForm, title=form_title)

    # ログインユーザーが受けた評価（被評価者）
    all_received_answers = Answer.objects.filter(reviewee=user, evaluation_form=evaluation_form)

    # 自分以外の人が評価したデータのみ取得
    received_answers = all_received_answers.exclude(reviewer=user)

    # 自分が行った評価（評価者として）
    given_answers = Answer.objects.filter(reviewer=user, evaluation_form=evaluation_form)

    # 平均スコア計算（他人からの評価のみ）
    received_avg = received_answers.aggregate(
        question1_avg=Avg('question1'),
        question2_avg=Avg('question2'),
        question3_avg=Avg('question3')
    )

    # 平均スコア計算（自分が行った評価）
    given_avg = given_answers.aggregate(
        question1_avg=Avg('question1'),
        question2_avg=Avg('question2'),
        question3_avg=Avg('question3')
    )

    # ギャップ計算（自分の評価 - 他人からの評価平均）
    gap = {
        'question1': (given_avg['question1_avg'] or 0) - (received_avg['question1_avg'] or 0),
        'question2': (given_avg['question2_avg'] or 0) - (received_avg['question2_avg'] or 0),
        'question3': (given_avg['question3_avg'] or 0) - (received_avg['question3_avg'] or 0)
    }

    return render(request, 'accounts/evaluation_result_detail.html', {
        'evaluation_form': evaluation_form,
        'received_answers': received_answers,  # 他人からの評価のみ表示
        'given_answers': given_answers,
        'received_avg': received_avg,
        'given_avg': given_avg,
        'gap': gap
    })

# @user_passes_test(is_admin)
# def create_evaluation_form(request):
#     """管理者が評価フォームを作成する画面"""
#     if request.method == "POST":
#         form = EvaluationFormForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # 管理画面がない場合はホームへ

#     else:
#         form = EvaluationFormForm()

#     return render(request, 'accounts/create_evaluation_form.html', {'form': form})

def is_admin(user):
    """管理者判定関数"""
    return user.is_superuser

