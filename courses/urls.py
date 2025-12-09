from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("submissions/history/", views.submission_history, name="submission_history"),
    path("<slug:course_slug>/", views.course_detail, name="course_detail"),
    path("<slug:course_slug>/enroll/", views.enroll_course, name="course_enroll"),
    path("<slug:course_slug>/lessons/<slug:lesson_slug>/", views.lesson_detail, name="course_lesson"),
    path("materials/<int:material_pk>/complete/", views.complete_material, name="material_complete"),
    path("materials/<int:material_pk>/submit/", views.submit_task, name="task_submit"),
]
