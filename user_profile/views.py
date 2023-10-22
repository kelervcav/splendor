from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from user_profile.forms import ProfileCreationForm
from .utils import unique_id_generator


User = get_user_model()


class ProfileListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    ordering = ['-created_at']
    permission_required = 'profiles.view_user'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        return context


@login_required
# @permission_required('profiles.add_user', raise_exception=True)
def profile_create(request):
    form = ProfileCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        uid = User.objects.get(id=user.id)
        uid.user_id = unique_id_generator(user.id)
        uid.set_custom_password()
        uid.save()
        messages.success(request, 'User created successfully.')
        return redirect('/users')

    template_name = 'user_create.html'
    context = {'form': form}
    return render(request, template_name, context)


def profile_edit(request, pk):
    users = get_object_or_404(User, id=pk)
    form = ProfileCreationForm(request.POST or None, instance=users)
    if form.is_valid():
        form.save()
        messages.success(request, 'Users updated successfully.')
        return redirect('users:edit', pk)
    template_name = 'user_edit.html'
    context = {'form': form, 'users': users}
    return render(request, template_name, context)


def profile_disable(request, pk):
    users = get_object_or_404(User, id=pk)
    users.is_active = False
    users.save()
    messages.success(request, 'Users has been disabled.')
    return redirect('/users')


def group_list(request):
    group_list = Group.objects.all()
    template = 'group_list.html'
    context = {'group_list': group_list}
    return render(request, template, context)


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

    template = 'profiles/group_edit.html'
    context = {
        'group': group,
        'permission': permission,
        'group_permission': group_permission
    }
    return render(request, template, context)


def patient_list(request):
    patients_list = User.objects.filter(is_patient=True).order_by('-created_at')
    template_name = 'patient_list.html'
    context = {'patients_list': patients_list}
    return render(request, template_name, context)







