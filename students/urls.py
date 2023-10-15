from django.urls import path, re_path, include
from .views import students, classroom, teachers
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('classroom/', classroom.index, name='classroom'),
    path('contact/', classroom.contact_us_view, name='contact_us'),
    re_path(r'^users/(?P<username>.+)/$', classroom.user_detail, name='user_detail'),

    path('register/student/', students.StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', students.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', students.StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<int:pk>/', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/<int:pk>/<int:module_id>/', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail_module'),
    path('student/quiz/', students.QuizListView.as_view(), name='student_quiz_list'),
    path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
    path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('student/quiz/<int:pk>/', students.take_quiz, name='take_quiz'),

    path('register/teacher/', teachers.TeacherRegistrationView.as_view(), name='teacher_registration'),
    path('quiz/', teachers.TeacherQuizListView.as_view(), name='teacher_quiz_change_list'),
    path('quiz/add/', teachers.QuizCreateView.as_view(), name='teacher_add_quiz'),
    path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='teacher_update_quiz'),
    path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='teacher_delete_quiz'),
    path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='teacher_quiz_results'),
    path('quiz/<int:pk>/question/add/', teachers.question_add, name='teacher_add_question'),
    re_path(r'^quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/$', teachers.question_change, name='teacher_change_question'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='teacher_delete_question'),
]
