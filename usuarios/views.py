from django.shortcuts import render, redirect
from .forms import CadastroForm

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('index')
    context = {}
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        context = {
            'form': CadastroForm(),
        }
    return render(request, 'cadastro.html', context)