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


class MaterialInline(admin.StackedInline):
    model = Material
    extra = 0
    min_num = 1
    show_change_link = True
    fields = (
        'title',
        'material_type',
        'question_type',
        'question_payload',
        'content',
        'media_file',
        'is_protected',
        'order',
    )


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    show_change_link = True
    fields = ('title', 'slug', 'order', 'description')


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    show_change_link = True
    fields = ('student', 'status', 'requested_at', 'answered_at')
    readonly_fields = ('requested_at', 'answered_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_filter = ('is_published',)
    inlines = [LessonInline, EnrollmentInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'course__title')
    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'material_type', 'order', 'is_protected')
    list_filter = ('material_type', 'lesson__course')
    autocomplete_fields = ('lesson',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'status', 'requested_at', 'answered_at')
    list_filter = ('status', 'course')
    search_fields = ('student__phone_number', 'course__title')
    actions = ('make_accepted', 'make_rejected')

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
	list_display = ('material', 'student', 'completed_at')
	list_filter = ('material__lesson__course',)


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
	list_display = ('material', 'student', 'attempt_number', 'status', 'score', 'submitted_at', 'graded_at')
	list_filter = ('status', 'material__lesson__course', 'material__question_type')
	search_fields = ('student__phone_number', 'material__title')
	readonly_fields = ('submitted_at', 'attempt_number', 'answer_payload')
	fieldsets = (
		(_('Submission Info'), {
			'fields': ('material', 'student', 'attempt_number', 'submitted_at', 'answer_payload')
		}),
		(_('Grading'), {
			'fields': ('status', 'score', 'feedback', 'graded_at')
		}),
	)
	actions = ['mark_as_graded', 'mark_as_passing']

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
	mark_as_graded.short_description = _('Mark as graded (if score set)')

	def mark_as_passing(self, request, queryset):
		"""Mark selected submissions with 100% score and complete."""
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
	mark_as_passing.short_description = _('Mark as 100% passing')

