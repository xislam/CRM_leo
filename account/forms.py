from django import forms

from account.models import University, Course, BeforeUniversity, Mailing


class StudentFilterForm(forms.Form):
    MANAGER_STATUSES = [
        ('', 'Все'),
        ('lead', 'Лид'),
        ('in_progress', 'В работе у менеджера'),
        ('rejected', 'Отказ'),
        ('waiting_for_payment', 'Ожидает оплаты'),
        ('partially_paid', 'Частично оплачен'),
        ('paid', 'Оплачен'),
    ]

    EDUCATION_STATUSES = [
        ('', 'Все'),
        ('free_subscription_registration', 'Регистрация на бесплатную подписку'),
        ('completed_free_subscription', 'Завершена бесплатная подписка'),
        ('paid_subscription_member', 'Участник платной подписки'),
        ('course_participant', 'Участник курса'),
        ('dropped_out', 'Выбыл'),
        ('completed_education', 'Завершил обучение'),
    ]

    before_university = forms.ModelChoiceField(queryset=BeforeUniversity.objects.all(), empty_label="Образование",
                                               widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    university = forms.ModelChoiceField(queryset=University.objects.all(), empty_label="Все университеты",
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Все курсы",
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    manager_status = forms.ChoiceField(choices=MANAGER_STATUSES, required=False,
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    education_status = forms.ChoiceField(choices=EDUCATION_STATUSES, required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}))


class MailingForm(forms.ModelForm):
    subject = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема'}))
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}))
    message = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение'}))
    photo = forms.ImageField(label=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Mailing
        fields = ['subject', 'title', 'message', 'photo']
