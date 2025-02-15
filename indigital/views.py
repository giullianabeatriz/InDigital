from django.shortcuts import render, redirect, get_object_or_404
from .models import Laboratorio, Reserva, Disponibilidade
from .forms import DisponibilidadeForm, LaboratorioForm, ReservaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    return render(request, "index.html")

# crud de disponibilidade

@login_required
@permission_required('indigital.criar_reserva', raise_exception=True)
def criar_reserva(request):
    laboratorios = Laboratorio.objects.all()
    if request.method == "POST":
        form = DisponibilidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva cadastrada com sucesso!')
            return redirect('horarios')
        else:
            messages.error(request, 'Erro ao cadastrar reserva!')
    else:
        form = DisponibilidadeForm()
    
    return render(request, "criar_reserva.html", {'form' : form, "laboratorios": laboratorios})

@login_required
@permission_required('indigital.editar_reserva', raise_exception=True)
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Disponibilidade, id=reserva_id)

    context = {
        "reserva" : reserva,
        "form" : DisponibilidadeForm(instance=reserva),
        "laboratorios": Laboratorio.objects.all()
    }

    if request.method == 'POST':
        form = DisponibilidadeForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('listar_reservas')
        else:
            context["form"] = form
    
    return render(request, "editar_reserva.html", context)

@login_required
def listar_reservas(request):
    reserva = Disponibilidade.objects.all()
    return render(request, "listar_reservas.html", {'reservas' : reserva})

@login_required
@permission_required('indigital.excluir_reserva', raise_exception=True)
def excluir_reserva(request, reserva_id):
    context = {
        "reserva": get_object_or_404(Disponibilidade, id=reserva_id)
    }

    if request.method == "POST":
        context["reserva"].delete()
        return redirect('listar_reservas')
    else:
        return render(request, "excluir_reserva.html", context)

# crud laboratorio

@login_required
@permission_required('indigital.criar_laboratorio', raise_exception=True)
def criar_laboratorio(request):
    if request.method == "POST":
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laboratório cadastrado com sucesso!')
            return redirect('listar_laboratorios')
        else:
            messages.error(request, 'Erro ao cadastrar laboratório!')
    else:
        form = LaboratorioForm()
    
    return render(request, "criar_laboratorio.html", {'form' : form})

@login_required
@permission_required('indigital.editar_laboratorio', raise_exception=True)
def editar_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    context = {
        "reserva" : laboratorio,
        "form" : LaboratorioForm(instance=laboratorio),
        "laboratorios": Laboratorio.objects.all()
    }

    if request.method == 'POST':
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            return redirect('listar_laboratorios')
        else:
            context["form"] = form
    return render(request, "editar_laboratorio.html", context)

@login_required
def listar_laboratorios(request):
    laboratorios = Laboratorio.objects.all()
    return render(request, "listar_laboratorios.html", {'laboratorios': laboratorios})

@login_required
@permission_required('indigital.excluir_laboratorio', raise_exception=True)
def excluir_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    if request.method == "POST":
        laboratorio.delete()
        return redirect('listar_laboratorios')
    else:
        return render(request, "excluir_laboratorio.html", {'laboratorio': laboratorio})
    
# horarios e reservas
@login_required
def horarios(request):
    reservas = Disponibilidade.objects.all()
    return render(request, "horarios.html", {'reservas': reservas})

@login_required
def reservar_laboratorio(request, disponibilidade_id):
    print(f"Disponibilidade ID recebido: {disponibilidade_id}")  # Depuração
    disponibilidade = get_object_or_404(Disponibilidade, id=disponibilidade_id)

    print(f"Vagas disponíveis: {disponibilidade.laboratorio.vagas}")  # Depuração

    if disponibilidade.laboratorio.vagas <= 0:
        print("Não há vagas disponíveis.")  # Depuração
        messages.error(request, "Não há vagas disponíveis para este horário.")
        return redirect('horarios')

    if Reserva.objects.filter(usuario=request.user, disponibilidade=disponibilidade).exists():
        print("Usuário já possui reserva para este horário.")  # Depuração
        messages.error(request, "Você já possui uma reserva para este horário.")
        return redirect('horarios')

    if request.method == "POST":
        print("Formulário enviado.")  # Depuração
        form = ReservaForm(request.POST)
        if form.is_valid():
            print("Formulário válido.")  # Depuração
            reserva = form.save(commit=False)
            reserva.usuario = request.user  # Associa o usuário logado à reserva
            print(f"Usuário associado à reserva: {reserva.usuario.username}")
            reserva.disponibilidade = disponibilidade
            reserva.save()
            print("Reserva salva com sucesso.")  # Depuração

            # Atualiza o número de vagas
            disponibilidade.laboratorio.vagas -= 1
            disponibilidade.laboratorio.save()
            print(f"Vagas atualizadas: {disponibilidade.laboratorio.vagas}")  # Depuração

            messages.success(request, "Reserva realizada com sucesso!")
            return redirect("reservas")
        else:
            print("Formulário inválido:", form.errors)  # Depuração
    else:
        print("Método da requisição não é POST.")  # Depuração
        form = ReservaForm()

    return render(request, "horarios.html", {"form": form, "disponibilidade": disponibilidade})
@login_required
def reservas(request):
    print("Acessando a view 'reservas'.")  # Depuração
    if request.user.is_staff:
        print("Usuário é staff. Renderizando admin_reservas.html.")  # Depuração
        return render(request, "admin_reservas.html")
    
    reservas = Reserva.objects.filter(usuario=request.user)
    print(f"Reservas encontradas: {reservas.count()}")  # Depuração
    return render(request, "user_reservas.html", {"reservas": reservas})
@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if reserva.usuario == request.user:
        disponibilidade = reserva.disponibilidade
        reserva.delete()  
        disponibilidade.laboratorio.vagas += 1 
        disponibilidade.save()
        messages.success(request, "Reserva cancelada com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para cancelar esta reserva.")

    return redirect('reservas')

def esqueceuasenha(request):
    return render(request, "esqueceuasenha.html")

def contaexcluida(request):
    return render(request, "contaexcluida.html")

def confirmacaodasenha(request):
    return render(request, "confirmacaodasenha.html")