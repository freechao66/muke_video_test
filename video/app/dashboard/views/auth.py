from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from app.libs.base_rander import rander_to_response
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        data = {'error': ''}
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        return rander_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {}
        print('用户名:', username)
        print('密码:', password)
        exists = User.objects.filter(username=username).exists()

        if not exists:
            data['error'] = '用户不存在'
            return rander_to_response(request, self.TEMPLATE, data=data)
        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return rander_to_response(request, self.TEMPLATE, data=data)
        if not user.is_superuser:
            data['error'] = '无权登录'
            return rander_to_response(request, self.TEMPLATE, data=data)
        login(request, user)
        return redirect(reverse('dashboard_index'))


class AdminManger(View):
    TEMPLATE = 'dashboard/auth/admin_manager.html'

    def get(self, request):
        data = {'users': ''}
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        users = User.objects.all()
        if users:
            data = {'users': users}
        return rander_to_response(request, self.TEMPLATE, data=data)


class LogoutUser(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class UpdateAdminStatus(View):
    def get(self, request):
        status = request.GET.get('status', 'on')
        print(status)
        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()
        return redirect(reverse('admin_manager'))
