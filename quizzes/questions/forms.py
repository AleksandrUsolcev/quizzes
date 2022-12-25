from django import forms
from django.forms import ValidationError

from .models import UserAnswer, UserVariant


class QuizProcessForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(QuizProcessForm, self).__init__(*args, **kwargs)
        self.question = self.initial.get('question')
        self.quiz = self.initial.get('quiz')
        self.progress = self.initial.get('progress')
        self.user = self.initial.get('user')
        self.stage = self.initial.get('stage')

        if self.progress.answers < self.stage:
            if self.quiz.shuffle_variants:
                self.variants = self.question.variants.all().order_by('?')
            else:
                self.variants = self.question.variants.all()
            self.corrected = self.variants.filter(
                correct=True).values_list('id', flat=True)
            self.add_variants_fields(self.variants)

    def add_variants_fields(self, variants_list: list) -> None:
        if self.question.many_correct:
            for variant in variants_list:
                self.fields[str(variant.id)] = forms.BooleanField(
                    label=variant.text,
                    required=False
                )

        if self.question.one_correct:
            RADIOS = []
            for variant in variants_list:
                RADIOS.append((str(variant.id), variant.text))
            self.fields['result'] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=RADIOS,
            )

    def clean(self):
        v_count = [v for v in self.cleaned_data.values() if v is False]
        if (self.question.many_correct
            and len(v_count) == len(self.cleaned_data.keys())
                and self.quiz.empty_answers is False):
            raise ValidationError('Выберите хотя бы один вариант ответа')
        return self.cleaned_data

    def add_results(
            self,
            results: list,
            correct: bool,
            no_answers: bool = False
    ) -> None:
        variants = self.question.variants.all()
        answer = UserAnswer.objects.create(
            user=self.user,
            quiz=self.quiz,
            quiz_revision=self.quiz.revision,
            quiz_title=self.quiz.title,
            question=self.question,
            question_text=self.question.text,
            correct=correct,
            no_answers=no_answers
        )
        for_create = []
        for variant in variants:
            selected = False
            corrected = False
            if variant.id in results:
                selected = True
            if variant.id in self.corrected:
                corrected = True
            for_create.append(
                UserVariant(
                    answer=answer,
                    variant=variant,
                    variant_text=variant.text,
                    selected=selected,
                    correct=corrected,
                )
            )
        UserVariant.objects.bulk_create(for_create)

    def answer(self):
        correct = True

        if self.question.one_correct:
            result = [int(self.cleaned_data.get('result'))]
            variant = self.variants.filter(id=result[0], correct=True)
            if not variant.exists():
                correct = False
            if result and self.progress.answers < self.stage:
                self.add_results(result, correct)

        if self.question.many_correct:
            results = []
            for variant_id in self.cleaned_data:
                status = self.cleaned_data.get(variant_id)
                if status is True:
                    results.append(int(variant_id))
            if self.quiz.empty_answers and not results:
                variants = self.variants.filter(
                    question=self.question,
                    correct=True
                )
                if variants.exists():
                    correct = False
                self.add_results(results, correct, no_answers=True)
            uncorrects = self.variants.filter(id__in=results, correct=False)
            corrects_count = self.variants.filter(
                question=self.question,
                correct=True
            ).count()
            if uncorrects.exists() or len(results) < corrects_count:
                correct = False
            if results and self.progress.answers < self.stage:
                self.add_results(results, correct)
