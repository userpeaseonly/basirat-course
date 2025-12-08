from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Material, TaskSubmission


class TaskSubmissionForm(forms.Form):
	"""
	Dynamic form for task submissions.
	Field type depends on material's question_type.
	"""
	def __init__(self, material, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.material = material

		if not material.material_type == Material.TASK:
			raise ValueError("Material must be a task type")

		payload = material.question_payload or {}
		choices = payload.get('choices', [])

		if material.question_type == Material.SINGLE_CHOICE:
			self.fields['answer'] = forms.ChoiceField(
				choices=[(c, c) for c in choices],
				widget=forms.RadioSelect,
				label=payload.get('question', _('Select an answer')),
				required=True,
			)
		elif material.question_type == Material.MULTI_CHOICE:
			self.fields['answer'] = forms.MultipleChoiceField(
				choices=[(c, c) for c in choices],
				widget=forms.CheckboxSelectMultiple,
				label=payload.get('question', _('Select all that apply')),
				required=True,
			)
		elif material.question_type == Material.FREE_RESPONSE:
			self.fields['answer'] = forms.CharField(
				widget=forms.Textarea(attrs={'rows': 6}),
				label=payload.get('question', _('Your answer')),
				required=True,
				max_length=5000,
			)

	def clean(self):
		cleaned_data = super().clean()
		return cleaned_data

	def get_answer_payload(self):
		"""Convert form data to JSON-serializable answer payload."""
		return {'answer': self.cleaned_data['answer']}
