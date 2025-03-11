from django.shortcuts import render, redirect
from .forms import EvaluationForm

def evaluation_input(request):
    if request.method == "POST":
        form = EvaluationForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.reviewer = request.user  # ログインユーザーを評価者としてセット
            answer.save()
            return redirect('evaluation_complete')  # 送信後、完了ページへリダイレクト
    else:
        form = EvaluationForm()

    return render(request, 'accounts/evaluation_input.html', {'form': form})

def home(request):
    return render(request, 'accounts/home.html')

def evaluation_complete(request):
    return render(request, 'accounts/evaluation_complete.html')
