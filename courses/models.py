from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
	title = models.CharField(max_length=255, verbose_name=_('Title'))
	slug = models.SlugField(unique=True, verbose_name=_('Slug'))
	summary = models.TextField(blank=True, verbose_name=_('Summary'))
	is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['title']
		verbose_name = _('course')
		verbose_name_plural = _('courses')

	def __str__(self):
		return self.title

	def enrollment_for(self, user):
		if not user.is_authenticated:
			return None
		return self.enrollments.filter(student=user).first()


class Lesson(models.Model):
	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE,
		related_name='lessons',
		verbose_name=_('Course'),
	)
	title = models.CharField(max_length=255, verbose_name=_('Title'))
	slug = models.SlugField(verbose_name=_('Slug'))
	description = models.TextField(blank=True, verbose_name=_('Description'))
	order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['order', 'title']
		unique_together = [('course', 'slug')]
		verbose_name = _('lesson')
		verbose_name_plural = _('lessons')

	def __str__(self):
		return f"{self.course.title} — {self.title}"

	def completed_for(self, user):
		if not user.is_authenticated:
			return False
		return all(material.is_completed_by(user) for material in self.materials.all())

	def is_available_for(self, user):
		if not user.is_authenticated:
			return False
		previous_lessons = self.course.lessons.filter(order__lt=self.order)
		return all(lesson.completed_for(user) for lesson in previous_lessons)


class Material(models.Model):
	LEARNING = 'learning'
	TASK = 'task'
	MATERIAL_TYPE_CHOICES = [
		(LEARNING, _('Learning resource')),
		(TASK, _('Task/assignment')),
	]

	MULTI_CHOICE = 'multiple_choice'
	SINGLE_CHOICE = 'single_choice'
	FREE_RESPONSE = 'free_response'
	QUESTION_TYPE_CHOICES = [
		(SINGLE_CHOICE, _('Single choice')),
		(MULTI_CHOICE, _('Multiple choice')),
		(FREE_RESPONSE, _('Free response')),
	]

	lesson = models.ForeignKey(
		Lesson,
		on_delete=models.CASCADE,
		related_name='materials',
	)
	title = models.CharField(max_length=255)
	material_type = models.CharField(
		max_length=16,
		choices=MATERIAL_TYPE_CHOICES,
		default=LEARNING,
	)
	content = models.TextField(blank=True, help_text=_('Body text, transcript, or instructions written by administrators.'))
	media_file = models.FileField(
		upload_to='materials/%Y/%m/%d',
		blank=True,
		null=True,
		help_text=_('Upload videos, PDFs, images, or other assets that play inline.'),
	)
	is_protected = models.BooleanField(default=True, help_text=_('Controls UI hints that discourage downloads/copying.'))
	question_type = models.CharField(max_length=24, choices=QUESTION_TYPE_CHOICES, blank=True)
	question_payload = models.JSONField(
		blank=True,
		null=True,
		help_text=_('Structured payload for task questions (choices, answers, hints).'),
	)
	order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['order', 'title']
		verbose_name = _('material')
		verbose_name_plural = _('materials')

	def __str__(self):
		return f"{self.lesson.title} — {self.title}"

	def clean(self):
		errors = {}
		if self.material_type == self.TASK:
			if self.media_file:
				errors['material_type'] = _('Task questions must not include uploaded learning files.')
			if not self.question_type:
				errors['question_type'] = _('Task materials require a question type.')
			if not self.question_payload:
				errors['question_payload'] = _('Task materials require a payload describing the question.')
		else:
			if self.question_type or self.question_payload:
				errors['material_type'] = _('Learning materials should not define question metadata.')
			if not (self.content or self.media_file):
				errors['content'] = _('Learning materials must include text or an uploaded asset.')
		if errors:
			raise ValidationError(errors)

	def is_completed_by(self, user):
		if not user.is_authenticated:
			return False
		return self.completions.filter(student=user).exists()

class Enrollment(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_ACCEPTED = 'accepted'
	STATUS_REJECTED = 'rejected'
	STATUS_CHOICES = [
		(STATUS_PENDING, _('Pending')),
		(STATUS_ACCEPTED, _('Accepted')),
		(STATUS_REJECTED, _('Rejected')),
	]

	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE,
		related_name='enrollments',
		verbose_name=_('Course'),
	)
	student = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='enrollments',
		verbose_name=_('Student'),
	)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	requested_at = models.DateTimeField(auto_now_add=True)
	answered_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		unique_together = ('course', 'student')
		verbose_name = _('enrollment')
		verbose_name_plural = _('enrollments')

	def __str__(self):
		return f"{self.student} — {self.course} ({self.status})"

	def mark_accepted(self):
		self.status = self.STATUS_ACCEPTED
		self.answered_at = timezone.now()
		self.save(update_fields=['status', 'answered_at'])

	def mark_rejected(self):
		self.status = self.STATUS_REJECTED
		self.answered_at = timezone.now()
		self.save(update_fields=['status', 'answered_at'])

	def is_active(self):
		return self.status == self.STATUS_ACCEPTED


class MaterialCompletion(models.Model):
	material = models.ForeignKey(
		Material,
		on_delete=models.CASCADE,
		related_name='completions',
		verbose_name=_('Material'),
	)
	student = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='material_completions',
		verbose_name=_('Student'),
	)
	completed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('material', 'student')
		verbose_name = _('material completion')
		verbose_name_plural = _('material completions')
