from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from courses.models import Course, Enrollment, Lesson, MaterialCompletion, TaskSubmission
from .forms import CustomAuthenticationForm, QuickCreateAccountForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def create_account(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = QuickCreateAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = QuickCreateAccountForm()
    return render(request, "users/create_account.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    """
    Home page view - accessible to all authenticated users
    Shows personalized content based on user role (student/admin)
    """
    context = {
        'user': request.user,
    }
    
    if request.user.is_student:
        # Student-specific context
        enrollments = Enrollment.objects.filter(
            student=request.user,
            status=Enrollment.STATUS_ACCEPTED
        ).select_related('course').prefetch_related('course__lessons')
        
        # Find next available lesson across all courses
        next_lesson = None
        next_course = None
        total_completed = 0
        total_lessons = 0
        
        for enrollment in enrollments:
            course = enrollment.course
            lessons = list(course.lessons.all())
            total_lessons += len(lessons)
            
            for lesson in lessons:
                if lesson.completed_for(request.user):
                    total_completed += 1
                elif next_lesson is None and lesson.is_available_for(request.user):
                    next_lesson = lesson
                    next_course = course
        
        # Recent enrollments for quick access
        recent_enrollments = enrollments[:3]
        
        context.update({
            'enrollments': enrollments,
            'recent_enrollments': recent_enrollments,
            'next_lesson': next_lesson,
            'next_course': next_course,
            'total_completed': total_completed,
            'total_lessons': total_lessons,
            'total_courses': enrollments.count(),
        })
    else:
        # Admin-specific context
        context.update({
            'total_courses': Course.objects.filter(is_published=True).count(),
            'pending_enrollments': Enrollment.objects.filter(status=Enrollment.STATUS_PENDING).count(),
        })
    
    # Featured courses for all users
    featured_courses = Course.objects.filter(is_published=True).prefetch_related('lessons')[:3]
    context['featured_courses'] = featured_courses
    
    return render(request, "users/home.html", context)


@login_required
def profile(request):
    """
    User profile page showing stats, info, and edit options
    """
    user = request.user
    context = {'user': user}
    
    if request.method == 'POST':
        # Handle profile updates
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        if first_name or last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=['first_name', 'last_name'])
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
    
    if user.is_student:
        # Student statistics
        enrollments = Enrollment.objects.filter(
            student=user,
            status=Enrollment.STATUS_ACCEPTED
        ).select_related('course').prefetch_related('course__lessons')
        
        total_courses = enrollments.count()
        total_lessons = 0
        completed_lessons = 0
        total_materials = 0
        completed_materials = MaterialCompletion.objects.filter(student=user).count()
        
        for enrollment in enrollments:
            lessons = enrollment.course.lessons.all()
            total_lessons += len(lessons)
            for lesson in lessons:
                if lesson.completed_for(user):
                    completed_lessons += 1
                total_materials += lesson.materials.count()
        
        # Task submission stats
        total_submissions = TaskSubmission.objects.filter(student=user).count()
        passing_submissions = TaskSubmission.objects.filter(
            student=user,
            status=TaskSubmission.STATUS_GRADED
        ).filter(score__gte=90).count()
        
        # Recent activity
        recent_submissions = TaskSubmission.objects.filter(
            student=user
        ).select_related('material__lesson__course').order_by('-submitted_at')[:5]
        
        # Calculate overall progress
        overall_progress = 0
        if total_lessons > 0:
            overall_progress = int((completed_lessons / total_lessons) * 100)
        
        context.update({
            'total_courses': total_courses,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'total_materials': total_materials,
            'completed_materials': completed_materials,
            'overall_progress': overall_progress,
            'total_submissions': total_submissions,
            'passing_submissions': passing_submissions,
            'recent_submissions': recent_submissions,
            'enrollments': enrollments,
        })
    else:
        # Admin statistics
        context.update({
            'total_courses': Course.objects.filter(is_published=True).count(),
            'total_students': Enrollment.objects.values('student').distinct().count(),
            'pending_enrollments': Enrollment.objects.filter(status=Enrollment.STATUS_PENDING).count(),
            'total_submissions': TaskSubmission.objects.filter(status=TaskSubmission.STATUS_PENDING_REVIEW).count(),
        })
    
    return render(request, 'users/profile.html', context)
