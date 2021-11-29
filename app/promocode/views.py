from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import PromocodeForm
from .models import Promocode


@require_POST
def promocode_apply(request):
    time = timezone.now()
    form = PromocodeForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            promocode = Promocode.objects.get(code__iexact=code, actual_from__lte=time, actual_to__gte=time,
                                              active=True)
            request.session['promocode_id'] = promocode.id
        except Promocode.DoesNotExist:
            request.session['promocode_id'] = None
    return redirect('orderlist:orderlist_detail')


