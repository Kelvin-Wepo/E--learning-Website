import requests
import datetime

from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, Sum, FloatField, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.template import loader
from django.template.loader import get_template
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from .models import Course, Module, Content, Subject, Review
from .forms import ModuleFormSet, ReviewForm, CourseCreateForm
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from students.forms import CourseEnrollForm
from django.utils.decorators import method_decorator
from students.decorators import teacher_required
from django.core.cache import cache
from courses.forms import UserEditForm, ProfileEditForm

from courses.badges import possibly_award_badge

from courses.search import youtube_search

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            request.user.profile.get_award_points(5)
            possibly_award_badge("edit_profile", user=request.user)
            user.save()
            profile.save()
            messages.success(request, _('Profile updated successfully'))
        else:
            messages.error(request, _('Error updating profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/edit.html', {'user_form': user_form, 'profile_form': profile_form})

