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

@login_required
def list_videos(request):
    subjects = Subject.objects.all()
    videos = []
    q  = None
    max_lengths = [10, 15, 20, 25, 30, 50]
    results = None
    if 'q' and 'results' in request.GET:
        q = request.GET['q'] + ' programming' # mostly tech targeted
        results = request.GET['results']
        request.user.profile.get_award_points(5)
        possibly_award_badge("list_videos", user=request.user)
        videos =  youtube_search(q, results)
    return render(request,'videos/list.html', {'videos': videos, 'q': q, 'results': results, 'subjects': subjects, 'max_lengths': max_lengths})
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')

        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.annotate(total_modules=Count('modules', distinct=True)).annotate(total_reviews=Count('reviews', distinct=True)).annotate(average_rating=Avg(F('reviews__rating'), distinct=False))
        page = request.GET.get('page', 1)

        # subjects = Course.objects.annotate(total_modules=Count('courses'))
        # courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = 'subject_{}_courses'.format(subject.id)
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
            paginator = Paginator(courses, 10)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
            paginator = Paginator(courses, 10)

        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)
        
        return self.render_to_response({'subjects': subjects, 'subject': subject, 'courses': courses})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        context['review_form'] = ReviewForm()
        context['reviews'] = Review.objects.order_by('-pub_date')[:9]
        return context