from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)

from user_profile.forms import ProfileCreationForm, EditProfileForm, AdminEditPasswordForm, UserProfileEdit
from .decorators import admin_required

User = get_user_model()


def process_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_patient and user.is_active:
                login(request, user)
                return redirect(request, 'dashboard:main')
            else:
                messages.error(request, "Sorry, you are not allowed to access this page.")
                return render(request, 'auth_login.html')
        else:
            messages.error(request, "Your username and password didn't match. Please try again.")
            return render(request, 'auth_login.html')

    return render(request, 'auth_login.html')


@login_required
@admin_required
@permission_required('user_profile.view_user', raise_exception=True)
def profile_list(request):
    users = User.objects.filter(is_patient=False).order_by('-created_at')
    template_name = 'user_list.html'
    context = {'users': users}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('user_profile.add_user', raise_exception=True)
def profile_create(request):
    form = ProfileCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.is_staff = True
        user.save()
        uid = User.objects.get(id=user.id)
        uid.save()
        messages.success(request, 'User created successfully.')
        return redirect('/users')

    template_name = 'user_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('user_profile.change_user', raise_exception=True)
def my_profile_edit(request):
    user = get_object_or_404(User, id=request.user.id)
    form = UserProfileEdit(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Profile updated successfully.')
        return redirect('users:my_profile_edit')

    template_name = 'my_profile_edit.html'
    context = {'form': form, 'user_profile': user}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('user_profile.change_user', raise_exception=True)
def user_profile_edit(request, pk):
    user = get_object_or_404(User, id=pk)
    group = Group.objects.filter(user=user).first()
    form = EditProfileForm(request.POST or None, instance=user, initial={'group': group})
    if form.is_valid():
        user_edit = form.save(commit=False)
        user_edit.is_active = True
        user_edit.save()
        user.groups.clear()
        user.groups.add(request.POST['group'])
        messages.success(request, 'Users updated successfully.')
        return redirect('users:edit', pk)

    template_name = 'user_edit.html'
    context = {'form': form, 'user_profile': user}
    return render(request, template_name, context)


@login_required
@admin_required
@permission_required('user_profile.disable_user', raise_exception=True)
def profile_disable(request, pk):
    users = get_object_or_404(User, id=pk)
    users.is_active = False
    users.save()
    messages.success(request, 'Users has been disabled.')
    return redirect('/users')


@login_required
@admin_required
@permission_required('auth.view_group', raise_exception=True)
def group_list(request):
    group_list = Group.objects.all()
    template = 'group_list.html'
    context = {'group_list': group_list}
    return render(request, template, context)


@login_required
@admin_required
@permission_required('auth.add_group', raise_exception=True)
def group_create(request):
    if request.method == 'POST':
        permissions = request.POST.getlist('permission')
        new_group, group = Group.objects.get_or_create(
            name=request.POST['group_name']
        )
        new_group.permissions.set(permissions)
        return redirect('users:group_list')
    else:
        permission = Permission.objects.all()
        template = 'group_create.html'
    context = {
        'permission': permission
    }
    return render(request, template, context)


@login_required
@admin_required
@permission_required('auth.change_group', raise_exception=True)
def group_edit(request, pk):
    if request.method == 'GET':
        group = Group.objects.get(id=pk)
        group_permission = Permission.objects.filter(group__id=group.id)
        permission = Permission.objects.exclude(group__id=group.id)
    else:
        permissions = request.POST.getlist('permission')
        group = Group.objects.get(id=pk)
        obj, created = Group.objects.update_or_create(
            name=group,
            defaults={'name': request.POST['group_name']},
        )
        obj.permissions.set(permissions)
        return redirect('users:group_list')

    template = 'group_edit.html'
    context = {
        'group': group,
        'permission': permission,
        'group_permission': group_permission
    }
    return render(request, template, context)


@login_required
@admin_required
def admin_edit_password(request, pk):
    user = get_object_or_404(User, id=pk)
    form = AdminEditPasswordForm(data=request.POST or None, user=user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Password changed successfully.')
        return redirect('users:edit', pk)
    template_name = 'user_admin_edit_password.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
@admin_required
def profile_edit_password(request):
    user = get_object_or_404(User, id=request.user.id)
    form = AdminEditPasswordForm(data=request.POST or None, user=user)
    if form.is_valid():
        form.save()
        return redirect('/admin')

    template_name = 'user_profile_edit_password.html'
    context = {'form': form}
    return render(request, template_name, context)
