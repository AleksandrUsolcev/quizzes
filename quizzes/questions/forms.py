from django import forms

from .models import Quiz, UserAnswer, UserVariant, Variant


class QuizProcessForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(QuizProcessForm, self).__init__(*args, **kwargs)
        self.question = self.initial.get('question')
        self.quiz = self.initial.get('quiz')
        self.user = self.initial.get('user')
        already_answered = self.initial.get('already_answered')
        if not already_answered:
            if self.quiz.shuffle_variants:
                question_set = self.question.variants.all().order_by('?')
            else:
                question_set = self.question.variants.all()
            if self.question.many_correct:
                for variant in question_set:
                    self.fields[str(variant.id)] = forms.BooleanField(
                        label=variant.text,
                        required=False
                    )
            if self.question.one_correct:
                RADIOS = []
                for variant in question_set:
                    RADIOS.append((str(variant.id), variant.text))
                self.fields['result'] = forms.ChoiceField(
                    widget=forms.RadioSelect,
                    choices=RADIOS,
                )

    def add_results(self, results, correct):
        variants = self.question.variants.all()
        answer = UserAnswer.objects.create(
            user=self.user,
            quiz=self.quiz,
            quiz_revision=self.quiz.revision,
            quiz_title=self.quiz.title,
            question=self.question,
            question_text=self.question.text,
            correct=correct
        )
        for_create = []
        for v_id in results:
            variant = variants.get(id=v_id)
            for_create.append(
                UserVariant(
                    answer=answer,
                    variant=variant,
                    variant_text=variant.text,
                    correct=variant.correct
                )
            )
        UserVariant.objects.bulk_create(for_create)

    def answer(self):
        answer = UserAnswer.objects.filter(
            user=self.user,
            quiz=self.quiz,
            quiz_revision=self.quiz.revision,
            question=self.question
        )
        correct = True
        if self.question.one_correct:
            result = [int(self.cleaned_data.get('result'))]
            variant = Variant.objects.filter(id=result[0], correct=True)
            if not variant.exists():
                correct = False
            if result and not answer.exists():
                self.add_results(result, correct)
        if self.question.many_correct:
            results = []
            for variant_id in self.cleaned_data:
                status = self.cleaned_data.get(variant_id)
                if status is True:
                    results.append(int(variant_id))
            variants = Variant.objects.filter(id__in=results, correct=False)
            if variants.exists():
                correct = False
            if results and not answer.exists():
                self.add_results(results, correct)


class QuizAddUpdateView(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        exclude = ('slug', 'author')
