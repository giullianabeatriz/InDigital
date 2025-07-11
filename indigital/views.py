from django.shortcuts import render, redirect, get_object_or_404
from .models import Laboratorio, Reserva, Disponibilidade
from .forms import DisponibilidadeForm, LaboratorioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

# crud de disponibilidade

@login_required
@permission_required('indigital.criar_disponibilidade', raise_exception=True)
def criar_disponibilidade(request):
    laboratorios = Laboratorio.objects.all()
    if request.method == "POST":
        form = DisponibilidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disponibilidade cadastrada com sucesso!')
            return redirect('listar_disponibilidades')
        else:
            messages.error(request, 'Erro ao cadastrar nova disponibilidade!')
    else:
        form = DisponibilidadeForm()
    
    return render(request, "criar_disponibilidade.html", {'form' : form, "laboratorios": laboratorios})

@login_required
@permission_required('indigital.editar_reserva', raise_exception=True)
def editar_disponibilidade(request, reserva_id):
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
            messages.success(request, "Disponibilidade editada com sucesso!")
            return redirect('listar_disponibilidades')
        else:
            context["form"] = form
            messages.error(request, "Erro ao editar disponibilidade!")
    
    return render(request, "editar_disponibilidade.html", context)

@login_required
@permission_required('indigital.listar_disponibilidades', raise_exception=True)
def listar_disponibilidades(request):
    reserva = Disponibilidade.objects.all()
    return render(request, "listar_disponibilidades.html", {'reservas' : reserva})

@login_required
@permission_required('indigital.excluir_disponibilidade', raise_exception=True)
def excluir_disponibilidade(request, reserva_id):
    disponibilidade = get_object_or_404(Disponibilidade, id=reserva_id)

    reservas_existentes = Reserva.objects.filter(disponibilidade=disponibilidade).exists()

    if reservas_existentes:
        messages.error(request, "Não é possível excluir esta disponibilidade porque existem reservas associadas.")
        return redirect('listar_disponibilidades')

    if request.method == "POST":
        disponibilidade.delete()
        messages.success(request, "Disponibilidade excluída com sucesso!")
        return redirect('listar_disponibilidades')
    else:
        return render(request, "excluir_disponibilidade.html", {'reserva': disponibilidade})

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
            messages.success(request, "Laboratório editado com sucesso!")
            return redirect('listar_laboratorios')
        else:
            context["form"] = form
            messages.error(request, "Erro ao editar laboratório!")

    return render(request, "editar_laboratorio.html", context)

@login_required
@permission_required('indigital.listar_laboratorios', raise_exception=True)
def listar_laboratorios(request):
    laboratorios_list = Laboratorio.objects.all()
    paginator = Paginator(laboratorios_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_laboratorios.html', {'page_obj': page_obj})

@login_required
@permission_required('indigital.excluir_laboratorio', raise_exception=True)
def excluir_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    if request.method == "POST":
        laboratorio.delete()
        messages.success(request, "Laboratório excluído com sucesso!")
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
    disponibilidade = get_object_or_404(Disponibilidade, id=disponibilidade_id)

    if disponibilidade.vagas <= 0:
        messages.error(request, "Não há vagas disponíveis para este horário.")
        return redirect('horarios')

    if Reserva.objects.filter(usuario=request.user, disponibilidade=disponibilidade).exists():
        messages.error(request, "Você já possui uma reserva para este horário.")
        return redirect('horarios')

    reserva = Reserva.objects.create(usuario=request.user, disponibilidade=disponibilidade)
    disponibilidade.vagas -= 1
    disponibilidade.save()

    messages.success(request, "Reserva realizada com sucesso!")
    return redirect("minhas_reservas")

@login_required
@permission_required('indigital.reservas', raise_exception=True)
def reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, "gerenciar_reservas.html", {"reservas": reservas})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    disponibilidade = reserva.disponibilidade

    disponibilidade.vagas += 1
    disponibilidade.save()

    reserva.delete()

    messages.success(request, "Sua reserva foi cancelada com sucesso!")
    return redirect("minhas_reservas")

@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'minhas_reservas.html', {'reservas': reservas})

def is_monitor_ou_admin(user):
    return user.perfil in ['monitor', 'admin']

@login_required
@user_passes_test(is_monitor_ou_admin)
def reservas_do_dia(request):
    from datetime import date
    reservas = Reserva.objects.filter(disponibilidade__data=date.today())
    return render(request, 'reservas_do_dia.html', {'reservas': reservas})