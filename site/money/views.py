from django.shortcuts import render

from .models import Assets, Exchange, Total


def summary(request):
    assets = Assets.objects.all()
    totals = Total.objects.all()
    exchanges = Exchange.objects.all()
    context = {
        'assets': assets,
        'totals': totals,
        'exchanges': exchanges
    }
    return render(request, 'index.html', context)
