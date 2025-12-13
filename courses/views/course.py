from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch, Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from ..forms import TaskSubmissionForm
from ..models import (
    Course,
    Enrollment,
    Lesson,
    Material,
    MaterialCompletion,
    TaskSubmission,
)


def course_list(request):
    courses = Course.objects.filter(is_published=True).prefetch_related('lessons')
    
    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(summary__icontains=search_query)
        )
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'title')
    if sort_by == 'lessons':
        courses = courses.annotate(lesson_count=Count('lessons')).order_by('-lesson_count')
    elif sort_by == 'title':
        courses = courses.order_by('title')
    elif sort_by == '-title':
        courses = courses.order_by('-title')
    
    context = {
        'courses': courses,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'courses/list.html', context)


def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = course.enrollment_for(request.user)
    lesson_states = []
    for lesson in course.lessons.all():
        lesson_states.append({
            'lesson': lesson,
            'completed': lesson.completed_for(request.user),
            'available': lesson.is_available_for(request.user),
        })
    context = {
        'course': course,
        'enrollment': enrollment,
        'lesson_states': lesson_states,
    }
    return render(request, 'courses/detail.html', context)


@login_required
def enroll_course(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    if request.method != 'POST':
        return redirect('course_detail', course_slug=course.slug)
    enrollment, created = Enrollment.objects.get_or_create(course=course, student=request.user)
    if not created and enrollment.status == Enrollment.STATUS_REJECTED:
        enrollment.status = Enrollment.STATUS_PENDING
        enrollment.answered_at = None
        enrollment.save(update_fields=['status', 'answered_at'])
    if not created:
        messages.info(request, _('Your enrollment request is already pending or accepted.'))
    else:
        messages.success(request, _('Enrollment request submitted.'))
    return redirect('course_detail', course_slug=course.slug)


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    enrollment = get_object_or_404(
        Enrollment,
        course=lesson.course,
        student=request.user,
        status=Enrollment.STATUS_ACCEPTED,
    )
    if not lesson.is_available_for(request.user) and not lesson.completed_for(request.user):
        messages.warning(request, _('Complete the previous lessons before continuing.'))
        return redirect('course_detail', course_slug=course_slug)
    materials = lesson.materials.select_related('lesson').order_by('order')
    completed = set(
        MaterialCompletion.objects.filter(material__lesson=lesson, student=request.user)
        .values_list('material_id', flat=True)
    )
    
    # Get submission data for task materials
    material_data = []
    for material in materials:
        data = {'material': material, 'completed': material.id in completed}
        if material.material_type == Material.TASK:
            submissions = TaskSubmission.objects.filter(
                material=material, 
                student=request.user
            ).order_by('-submitted_at')
            data['submissions'] = submissions
            data['can_submit'] = TaskSubmission.can_submit(material, request.user)
            data['attempts_used'] = TaskSubmission.get_attempts_count(material, request.user)
            data['latest_submission'] = submissions.first()
        material_data.append(data)
    
    context = {
        'lesson': lesson,
        'course': lesson.course,
        'material_data': material_data,
        'enrollment': enrollment,
        'completed_ids': completed,
    }
    return render(request, 'courses/lesson.html', context)


@login_required
def complete_material(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    if request.method != 'POST':
        raise PermissionDenied
    enrollment = get_object_or_404(
        Enrollment,
        course=material.lesson.course,
        student=request.user,
        status=Enrollment.STATUS_ACCEPTED,
    )
    lesson = material.lesson
    if not lesson.is_available_for(request.user) and not lesson.completed_for(request.user):
        raise PermissionDenied
    
    # Only allow completion for learning materials (not tasks)
    if material.material_type == Material.TASK:
        messages.error(request, _('Task materials require submission, not simple completion.'))
        return redirect('course_lesson', course_slug=lesson.course.slug, lesson_slug=lesson.slug)
    
    MaterialCompletion.objects.get_or_create(material=material, student=request.user)
    messages.success(request, _('Material marked as complete.'))
    return redirect('course_lesson', course_slug=lesson.course.slug, lesson_slug=lesson.slug)


@login_required
def submit_task(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk, material_type=Material.TASK)
    enrollment = get_object_or_404(
        Enrollment,
        course=material.lesson.course,
        student=request.user,
        status=Enrollment.STATUS_ACCEPTED,
    )
    lesson = material.lesson
    
    if not lesson.is_available_for(request.user) and not lesson.completed_for(request.user):
        raise PermissionDenied
    
    # Check attempt limit
    if not TaskSubmission.can_submit(material, request.user):
        messages.error(request, _('You have used all 3 attempts for this task.'))
        return redirect('course_lesson', course_slug=lesson.course.slug, lesson_slug=lesson.slug)
    
    if request.method == 'POST':
        form = TaskSubmissionForm(material, request.POST)
        if form.is_valid():
            attempt_number = TaskSubmission.get_attempts_count(material, request.user) + 1
            submission = TaskSubmission.objects.create(
                material=material,
                student=request.user,
                answer_payload=form.get_answer_payload(),
                attempt_number=attempt_number,
            )
            
            # Try auto-grading
            if submission.auto_grade():
                if submission.is_passing():
                    MaterialCompletion.objects.get_or_create(material=material, student=request.user)
                    messages.success(request, _('Correct! Score: {score}%. Material completed.').format(score=int(submission.score)))
                else:
                    messages.warning(request, _('Incorrect. Score: {score}%. You have {remaining} attempts remaining.').format(
                        score=int(submission.score),
                        remaining=3 - attempt_number
                    ))
            else:
                messages.info(request, _('Your answer has been submitted for review.'))
            
            return redirect('course_lesson', course_slug=lesson.course.slug, lesson_slug=lesson.slug)
    else:
        form = TaskSubmissionForm(material)
    
    context = {
        'material': material,
        'lesson': lesson,
        'form': form,
        'attempts_used': TaskSubmission.get_attempts_count(material, request.user),
    }
    return render(request, 'courses/submit_task.html', context)


@login_required
def submission_history(request):
    """Display all task submissions by the current student."""
    if not request.user.is_student:
        raise PermissionDenied
    
    # Get all enrolled courses with their lessons and task materials
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status=Enrollment.STATUS_ACCEPTED
    ).select_related('course').prefetch_related(
        Prefetch(
            'course__lessons',
            queryset=Lesson.objects.prefetch_related(
                Prefetch(
                    'materials',
                    queryset=Material.objects.filter(material_type='task').prefetch_related(
                        Prefetch(
                            'submissions',
                            queryset=TaskSubmission.objects.filter(student=request.user).order_by('-submitted_at'),
                            to_attr='student_submissions'
                        )
                    )
                )
            )
        )
    )
    
    # Build structured data for template
    history_data = []
    for enrollment in enrollments:
        course_data = {
            'course': enrollment.course,
            'lessons': []
        }
        for lesson in enrollment.course.lessons.all():
            task_materials = [m for m in lesson.materials.all() if m.material_type == 'task']
            if task_materials:
                lesson_data = {
                    'lesson': lesson,
                    'tasks': []
                }
                for material in task_materials:
                    submissions = material.student_submissions if hasattr(material, 'student_submissions') else []
                    if submissions:
                        lesson_data['tasks'].append({
                            'material': material,
                            'submissions': submissions,
                            'best_score': max(s.score for s in submissions if s.score is not None) if any(s.score is not None for s in submissions) else None,
                            'total_attempts': len(submissions),
                        })
                if lesson_data['tasks']:
                    course_data['lessons'].append(lesson_data)
        if course_data['lessons']:
            history_data.append(course_data)
    
    context = {
        'history_data': history_data,
    }
    return render(request, 'courses/submission_history.html', context)


@login_required
def progress_dashboard(request):
    """Display student's progress dashboard with all enrolled courses and statistics."""
    if not request.user.is_student:
        raise PermissionDenied
    
    # Get all enrollments with course and lesson data
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status=Enrollment.STATUS_ACCEPTED
    ).select_related('course').prefetch_related('course__lessons__materials')
    
    # Build dashboard data
    dashboard_data = []
    total_lessons = 0
    completed_lessons = 0
    
    for enrollment in enrollments:
        course = enrollment.course
        lessons = list(course.lessons.all())
        total_lessons += len(lessons)
        
        # Calculate course statistics
        course_completed = 0
        next_lesson = None
        
        for lesson in lessons:
            if lesson.completed_for(request.user):
                course_completed += 1
                completed_lessons += 1
            elif next_lesson is None and lesson.is_available_for(request.user):
                next_lesson = lesson
        
        # Calculate progress percentage
        progress_percentage = round((course_completed / len(lessons) * 100)) if lessons else 0
        
        # Count materials
        total_materials = sum(material.material_type == 'learning' for lesson in lessons for material in lesson.materials.all())
        total_tasks = sum(material.material_type == 'task' for lesson in lessons for material in lesson.materials.all())
        
        dashboard_data.append({
            'enrollment': enrollment,
            'course': course,
            'total_lessons': len(lessons),
            'completed_lessons': course_completed,
            'progress_percentage': progress_percentage,
            'next_lesson': next_lesson,
            'total_materials': total_materials,
            'total_tasks': total_tasks,
            'is_completed': course_completed == len(lessons) and len(lessons) > 0,
        })
    
    # Overall statistics
    overall_progress = round((completed_lessons / total_lessons * 100)) if total_lessons else 0
    
    context = {
        'dashboard_data': dashboard_data,
        'total_courses': len(dashboard_data),
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'overall_progress': overall_progress,
    }
    return render(request, 'courses/progress_dashboard.html', context)
