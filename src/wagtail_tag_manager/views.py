from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import TemplateView

from .forms import ConsentForm
from .utils import set_cookie


class ManageView(TemplateView):
    template_name = "manage.html"

    def get(self, request, *args, **kwargs):
        if hasattr(settings, 'WTM_MANAGE_VIEW') and getattr(settings, 'WTM_MANAGE_VIEW'):
            return super().get(request, *args, **kwargs)
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect('')

        form = ConsentForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                set_cookie(response, f'wtm_{key}', str(value).lower())

        return response