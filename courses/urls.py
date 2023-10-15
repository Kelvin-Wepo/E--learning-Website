from django.urls import path, include
from django.views.generic import TemplateView
from termsandconditions.decorators import terms_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('dashboard/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', never_cache(login_required(terms_required(views.CourseCreateView.as_view()))), name='course_create'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    # path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<int:module_id>/content/<str:model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<str:model_name>/<int:id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:subject>/add_review/', views.add_review, name='add_review'),
    path('videos/', views.list_videos, name='videos_list'),
    path('edit/', views.edit, name='edit'),
    path('about-company/', TemplateView.as_view(template_name='about.html'), name='about_company'),
    path('termsrequired/', never_cache(terms_required(login_required(TemplateView.as_view(template_name='terms_required.html')))), name='terms_required'),
    path('search/', views.SearchSubmitView.as_view(), name='search'),
    path('search-ajax-submit/', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
]
