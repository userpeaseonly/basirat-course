from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import (
    Course,
    Enrollment,
    Lesson,
    Material,
    MaterialCompletion,
    TaskSubmission,
)


# Configure admin site
admin.site.site_header = _('Basirat LMS Administration')
admin.site.site_title = _('Basirat Admin')
admin.site.index_title = _('Learning Management System')


class MaterialInline(admin.StackedInline):
    model = Material
    extra = 0
    min_num = 1
    show_change_link = True
    classes = ('collapse',)
    fields = (
        'title',
        'order',
        'material_type',
        'question_type',
        'question_payload',
        'content',
        'media_file',
        'is_protected',
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order')


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    show_change_link = True
    fields = ('order', 'title', 'slug', 'description')
    ordering = ('order',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order')


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    show_change_link = True
    can_delete = False
    fields = ('student', 'status', 'requested_at', 'answered_at')
    readonly_fields = ('student', 'requested_at', 'answered_at')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_count', 'enrollment_count', 'is_published', 'updated_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [LessonInline, EnrollmentInline]
    
    fieldsets = (
        (_('Course Information'), {
            'fields': ('title', 'slug', 'summary', 'is_published')
        }),
        (_('Dates'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = _('Lessons')
    lesson_count.admin_order_field = 'lessons__count'
    
    def enrollment_count(self, obj):
        return obj.enrollments.filter(status=Enrollment.STATUS_ACCEPTED).count()
    enrollment_count.short_description = _('Students')
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('lessons', 'enrollments')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'course', 'material_count', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('course',)
    list_editable = ('order',)
    search_fields = ('title', 'course__title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('course', 'order')
    inlines = [MaterialInline]
    
    fieldsets = (
        (_('Lesson Information'), {
            'fields': ('course', 'title', 'slug', 'order', 'description')
        }),
        (_('Dates'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def material_count(self, obj):
        return obj.materials.count()
    material_count.short_description = _('Materials')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course').prefetch_related('materials')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'lesson', 'material_type', 'question_type', 'is_protected')
    list_display_links = ('title',)
    list_filter = ('material_type', 'question_type', 'lesson__course', 'is_protected')
    list_editable = ('order',)
    search_fields = ('title', 'lesson__title', 'lesson__course__title')
    autocomplete_fields = ('lesson',)
    ordering = ('lesson__course', 'lesson__order', 'order')
    
    fieldsets = (
        (_('Material Information'), {
            'fields': ('lesson', 'title', 'order', 'material_type')
        }),
        (_('Learning Content'), {
            'fields': ('content', 'media_file', 'is_protected'),
            'description': _('For learning materials only. Leave empty for tasks.')
        }),
        (_('Task Content'), {
            'fields': ('question_type', 'question_payload'),
            'description': _('For task materials only. Leave empty for learning materials.')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('lesson', 'lesson__course')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_phone', 'course', 'status', 'requested_at', 'answered_at')
    list_filter = ('status', 'course', 'requested_at')
    search_fields = ('student__phone_number', 'student__first_name', 'student__last_name', 'course__title')
    date_hierarchy = 'requested_at'
    ordering = ('-requested_at',)
    actions = ('make_accepted', 'make_rejected')
    
    fieldsets = (
        (_('Enrollment Details'), {
            'fields': ('student', 'course', 'status')
        }),
        (_('Dates'), {
            'fields': ('requested_at', 'answered_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('requested_at', 'answered_at')
    
    def student_name(self, obj):
        return obj.student.get_full_name() or _('(No name)')
    student_name.short_description = _('Student Name')
    student_name.admin_order_field = 'student__first_name'
    
    def student_phone(self, obj):
        return obj.student.phone_number
    student_phone.short_description = _('Phone Number')
    student_phone.admin_order_field = 'student__phone_number'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course')

    def make_accepted(self, request, queryset):
        updated = queryset.exclude(status=Enrollment.STATUS_ACCEPTED).update(
            status=Enrollment.STATUS_ACCEPTED,
            answered_at=timezone.now(),
        )
        self.message_user(request, _('{count} enrollments accepted').format(count=updated))
    make_accepted.short_description = _('Mark selected enrollments as accepted')

    def make_rejected(self, request, queryset):
        updated = queryset.exclude(status=Enrollment.STATUS_REJECTED).update(
            status=Enrollment.STATUS_REJECTED,
            answered_at=timezone.now(),
        )
        self.message_user(request, _('{count} enrollments rejected').format(count=updated))
    make_rejected.short_description = _('Mark selected enrollments as rejected')


@admin.register(MaterialCompletion)
class MaterialCompletionAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_phone', 'material', 'lesson', 'course', 'completed_at')
    list_filter = ('material__lesson__course', 'completed_at')
    search_fields = ('student__phone_number', 'student__first_name', 'student__last_name', 'material__title')
    date_hierarchy = 'completed_at'
    ordering = ('-completed_at',)
    readonly_fields = ('material', 'student', 'completed_at')
    
    fieldsets = (
        (_('Completion Details'), {
            'fields': ('student', 'material', 'completed_at')
        }),
    )
    
    def student_name(self, obj):
        return obj.student.get_full_name() or _('(No name)')
    student_name.short_description = _('Student Name')
    student_name.admin_order_field = 'student__first_name'
    
    def student_phone(self, obj):
        return obj.student.phone_number
    student_phone.short_description = _('Phone')
    
    def lesson(self, obj):
        return obj.material.lesson.title
    lesson.short_description = _('Lesson')
    
    def course(self, obj):
        return obj.material.lesson.course.title
    course.short_description = _('Course')
    course.admin_order_field = 'material__lesson__course__title'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'material', 'material__lesson', 'material__lesson__course')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_phone', 'material', 'question_type', 'attempt_number', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'material__question_type', 'material__lesson__course', 'submitted_at')
    search_fields = ('student__phone_number', 'student__first_name', 'student__last_name', 'material__title', 'material__lesson__title')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    readonly_fields = ('material', 'student', 'submitted_at', 'attempt_number', 'answer_payload', 'graded_at')
    actions = ['mark_as_graded', 'mark_as_passing']
    
    fieldsets = (
        (_('Submission Information'), {
            'fields': ('material', 'student', 'attempt_number', 'submitted_at')
        }),
        (_('Student Answer'), {
            'fields': ('answer_payload',),
            'description': _('The answer submitted by the student')
        }),
        (_('Grading'), {
            'fields': ('status', 'score', 'feedback', 'graded_at'),
            'description': _('Enter score (0-100) and feedback, then use actions to mark as graded')
        }),
    )
    
    def student_name(self, obj):
        return obj.student.get_full_name() or _('(No name)')
    student_name.short_description = _('Student Name')
    student_name.admin_order_field = 'student__first_name'
    
    def student_phone(self, obj):
        return obj.student.phone_number
    student_phone.short_description = _('Phone')
    
    def question_type(self, obj):
        return obj.material.get_question_type_display() if obj.material.question_type else '-'
    question_type.short_description = _('Question Type')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'material', 'material__lesson', 'material__lesson__course')
    
    def has_add_permission(self, request):
        return False

    def mark_as_graded(self, request, queryset):
        """Mark selected submissions as graded (requires manual score entry)."""
        pending = queryset.filter(status=TaskSubmission.STATUS_PENDING)
        count = 0
        for submission in pending:
            if submission.score is not None:
                submission.status = TaskSubmission.STATUS_GRADED
                submission.graded_at = timezone.now()
                submission.save(update_fields=['status', 'graded_at'])
                
                # Create completion if passing
                if submission.is_passing():
                    MaterialCompletion.objects.get_or_create(
                        material=submission.material,
                        student=submission.student
                    )
                count += 1
        self.message_user(request, _('{count} submissions marked as graded').format(count=count))
    mark_as_graded.short_description = _('Mark as graded if score set')

    def mark_as_passing(self, request, queryset):
        """Mark selected submissions with 100 percent score and complete."""
        updated = queryset.update(
            status=TaskSubmission.STATUS_GRADED,
            score=100,
            graded_at=timezone.now(),
        )
        # Create completions for all passing submissions
        for submission in queryset:
            MaterialCompletion.objects.get_or_create(
                material=submission.material,
                student=submission.student
            )
        self.message_user(request, _('{count} submissions marked as passing').format(count=updated))
    mark_as_passing.short_description = _('Mark as 100 percent passing')

