# coding:utf-8
from django.shortcuts import redirect, reverse
from django.views.generic import View
from app.libs.base_rander import rander_to_response


class Base(View):
    TEMPLATE = 'dashboard/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return rander_to_response(request, self.TEMPLATE)
