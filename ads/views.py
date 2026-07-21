from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Ad, AdImage
from .forms import AdForm, RegisterForm


def ad_list(request):
    """Главная страница: список объявлений + поиск и фильтры."""
    ads = Ad.objects.filter(status='active')  # витрина «только активные»

    # Читаем параметры фильтров из адресной строки (?q=...&category=...)
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    price_min = request.GET.get('min', '')
    price_max = request.GET.get('max', '')

    if q:
        ads = ads.filter(title__icontains=q)  # поиск по названию
    if category:
        ads = ads.filter(category=category)
    if price_min:
        ads = ads.filter(price__gte=price_min)
    if price_max:
        ads = ads.filter(price__lte=price_max)

    context = {
        'ads': ads,
        'categories': Ad.CATEGORY_CHOICES,
        'q': q,
        'category': category,
        'price_min': price_min,
        'price_max': price_max,
    }
    return render(request, 'ads/ad_list.html', context)


def ad_detail(request, pk):
    """Детальная страница объявления + счётчик просмотров."""
    ad = get_object_or_404(Ad, pk=pk)

    # Увеличиваем счётчик просмотров (F — чтобы считалось прямо в базе)
    Ad.objects.filter(pk=pk).update(views=F('views') + 1)
    ad.refresh_from_db()

    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_create(request):
    """Создание объявления (только для вошедших пользователей)."""
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user  # автор — текущий пользователь
            ad.save()
            # Сохраняем все загруженные фото (их может быть несколько)
            for f in request.FILES.getlist('images'):
                AdImage.objects.create(ad=ad, image=f)
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'Новое объявление'})


@login_required
def ad_edit(request, pk):
    """Редактирование. Разрешено только владельцу объявления."""
    ad = get_object_or_404(Ad, pk=pk, author=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            for f in request.FILES.getlist('images'):
                AdImage.objects.create(ad=ad, image=f)
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'Редактировать', 'ad': ad})


@login_required
def ad_delete(request, pk):
    """Удаление объявления (только владелец, с подтверждением)."""
    ad = get_object_or_404(Ad, pk=pk, author=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_delete.html', {'ad': ad})


@login_required
def my_ads(request):
    """Страница «Мои объявления» — все объявления текущего пользователя."""
    ads = Ad.objects.filter(author=request.user)
    return render(request, 'ads/my_ads.html', {'ads': ads})


def register(request):
    """Регистрация нового пользователя. После — сразу входим."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
