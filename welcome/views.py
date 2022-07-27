from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from welcome.forrms import *
from django import forms
from django.urls import reverse, reverse_lazy
from welcome.functions import *
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from welcome.models import MedicineCardInstance, MedicineCard, PrivateDocument, MedicalEstablishments
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import MciFilter


# Просмотр списка записей в медицинской карте + их фильтрация
# Viewing the list of entries in the medical record + filtering them
class ShowAllMedicineCardInstances(LoginRequiredMixin, ListView):
    model = MedicineCardInstance

    def get_queryset(self):
        return MedicineCardInstance.objects.filter(medicine_card__user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MciFilter(self.request.GET, queryset=self.get_queryset())
        return context


# Добавление медицинской карточки
# Adding a medical card
class AddAddMedicineCard(LoginRequiredMixin, CreateView):
    model = MedicineCard
    form_class = AddMedicineCard
    success_url = reverse_lazy('mc-add')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddAddMedicineCard, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        if MedicineCard.objects.filter(user=self.request.user).exists():
            return HttpResponseRedirect(reverse_lazy('delete-mc-notification'))
        return super().form_valid(form)


# Редактирование медицинской карточки
# Editing a medical record
@login_required
def edit_mc(request):
    if request.user.is_authenticated is False:
        content = {'temp': _('To edit a medical card, you need to log in')}
        return render(request, 'welcome/AddMc.html', content)
    mc = MedicineCard.objects.all().filter(user=request.user)
    if not mc.exists():
        content = {'temp': _('You do not have a medical card record to edit')}
        return render(request, 'welcome/AddMc.html', content)
    mc = MedicineCard.objects.get(user=request.user)
    form = EditMedicineCard(instance=mc)
    if request.method == 'POST':
        form = EditMedicineCard(request.POST, instance=mc)
        if form.is_valid():
            form.save()
            content = {'temp': _('You have successfully edited the medical card record')}
            return render(request, 'welcome/AddMc.html', content)
    content = {'temp': _('Editing a medical card record'), 'form': form}
    return render(request, 'welcome/AddMc.html', content)


# Добавление нового доктора
# Add new Doctor
class AddDoctor(LoginRequiredMixin, CreateView):
    model = Doctors
    form_class = AddDoctorForm
    success_url = reverse_lazy('add-doctor')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddDoctor, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Отображает список докторов
# Displays a list of doctors
class ShowAllDoctor(LoginRequiredMixin, ListView):
    template_name = 'welcome/ShowDoctor_detail.html'
    model = Doctors

    def get_queryset(self):
        return Doctors.objects.filter(user=self.request.user)


# Редактирует выбранного доктора
# Edits the selected doctor
class EditDoctor(LoginRequiredMixin, UpdateView):
    model = Doctors
    form_class = EditDoctorForm
    success_url = reverse_lazy('show_all_doctor')
    template_name = 'welcome/Doctors_form.html'

    def get_queryset(self):
        return Doctors.objects.filter(user=self.request.user)


# Предупреждение при удалении врача, если врач фигурирует в записях медицинской карты.
# Warning when removing a doctor if the doctor appears in the medical records.
@login_required
def pre_delete_doctor(request, pk):
    if not Doctors.objects.all().filter(user=request.user).exists():
        raise Http404()
    doctor = Doctors.objects.get(pk=pk)
    if MedicineCardInstance.objects.filter(doctors=doctor).exists():
        return render(request, 'notification/delete_doctor_notification.html')
    return HttpResponseRedirect(reverse_lazy('delete-doctor', args=[pk]))


# Функция удаления врача
# Doctor delete function
class DeleteDoctor(LoginRequiredMixin, DeleteView):
    model = Doctors
    success_url = reverse_lazy('show_all_doctor')

    def get_queryset(self):
        return Doctors.objects.filter(user=self.request.user)


# Функция добавления медицинского учреждения
# Function to add a medical facility
class AddMedicalEstablishment(LoginRequiredMixin, CreateView):
    model = MedicalEstablishments
    form_class = AddMedicalEstablishmentForm
    success_url = reverse_lazy('add-medical-establishments')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddMedicalEstablishment, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Функция отображения медицинское учреждение
# Medicine facility showing function
class ShowAllMedicalEstablishment(LoginRequiredMixin, ListView):
    template_name = 'welcome/MedicalEstablishment_detail.html'
    model = MedicalEstablishments

    def get_queryset(self):
        return MedicalEstablishments.objects.filter(user=self.request.user)


# Функция редактирования медицинское учреждение
# Medicine facility editing function
class EditMedicalEstablishment(LoginRequiredMixin, UpdateView):
    model = MedicalEstablishments
    form_class = EditMedicalEstablishmentForm
    success_url = reverse_lazy('show-medical-establishments')
    template_name = 'welcome/MedicalEstablishment_form.html'


# Предупреждение при удалении медицинского учреждения, если медицинское учреждение фигурирует в записях медицинской карты.
# Warning when removing a medical facility if the medical facility appears in the medical records.
@login_required
def pre_delete_medical_establishments(request, pk):
    if not MedicalEstablishments.objects.all().filter(user=request.user).exists():
        raise Http404()
    medical_establishment = MedicalEstablishments.objects.get(pk=pk)
    if MedicineCardInstance.objects.filter(medical_establishments=medical_establishment).exists():
        return render(request, 'notification/delete_medical_establishment_notification.html')
    return HttpResponseRedirect(reverse_lazy('delete-medical-establishments', args=[pk]))


# Функция удаления медицинского учреждения
# Medical Establishment delete function
class DeleteMedicalEstablishment(LoginRequiredMixin, DeleteView):
    model = MedicalEstablishments
    success_url = reverse_lazy('show-medical-establishments')

    def get_queryset(self):
        return MedicalEstablishments.objects.filter(user=self.request.user)


# Функция добавления области медицины
# Function to add medicine area
class AddMedicalMedicalField(LoginRequiredMixin, CreateView):
    model = MedicalField
    form_class = AddMedicalField
    success_url = reverse_lazy('add-medical-field')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddMedicalMedicalField, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Функция отображения области медицины
# Medicine area showing function
class ShowAllMedicalField(LoginRequiredMixin, ListView):
    template_name = 'welcome/MedicalField_detail.html'
    model = MedicalField

    def get_queryset(self):
        return MedicalField.objects.filter(user=self.request.user)


# Функция редактирования области медицины
# Medicine area editing function
class EditMedicalField(LoginRequiredMixin, UpdateView):
    model = MedicalField
    form_class = EditMedicalFieldForm
    success_url = reverse_lazy('show-medical-field')
    template_name = 'welcome/MedicalField_form.html'

    def get_queryset(self):
        return MedicalField.objects.filter(user=self.request.user)


# Предупреждение при удалении области медицины, если область медицины фигурирует в записях медицинской карты.
# Warning when removing a Medical Field if the Medical Field appears in the medical records.
@login_required
def pre_delete_medical_field(request, pk):
    if not MedicalField.objects.all().filter(user=request.user).exists():
        raise Http404()
    medical_field = MedicalField.objects.get(pk=pk)
    if MedicineCardInstance.objects.filter(medical_field=medical_field).exists():
        return render(request, 'notification/delete_medical_field_notification.html')
    return HttpResponseRedirect(reverse_lazy('delete-medical-field', args=[pk]))


# Функция удаления области медицины
# Function to delete the Medical Field
class DeleteMedicalField(LoginRequiredMixin, DeleteView):
    model = MedicalField
    success_url = reverse_lazy('show-medical-field')

    def get_queryset(self):
        return MedicalField.objects.filter(user=self.request.user)


class ShowMciForPrint(LoginRequiredMixin, DetailView):
    model = MedicineCardInstance
    context_object_name = 'mci'

    def get_queryset(self):
        mc = MedicineCard.objects.get(user=self.request.user)
        return MedicineCardInstance.objects.all().filter(medicine_card=mc)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mci = MedicineCardInstance.objects.get(pk=self.object.pk)
        documents = PrivateDocument.objects.all().filter(mci=mci)
        documents_url = []
        for i in documents:
            if check_file_type(i.upload.file)['type'] == 'pictures':
                documents_url.append(i.upload.url)
        context['documents_url'] = documents_url
        return context


# Функция алерт перед удалением записи в медицинской карте
# Alert function before deleting an entry in the medical record
@login_required
def alert_delete_mci(request, mci_pk):
    notification_class = "notification is-danger"
    part1 = _("Are you sure you want to delete the entry number")
    part2 = str(mci_pk)
    part3 = _(' from a medical card record?')
    part4 = ''
    part5 = ''
    docs = PrivateDocument.objects.all().filter(mci=mci_pk, mci__medicine_card__user=request.user)
    if len(docs) > 0:
        part4 = _(' Attached documents will also be deleted along with this entry: ')
        for i in docs:
            part5 = part5 + ' ' + str(i.upload.name)
    part6 = _(' All data will be deleted without the possibility of recovery. Click Delete to confirm.')
    var1 = part1 + part2 + part3 + part4 + part5 + part6
    if request.method == 'POST':
        # Разные проверки на случай если нас пытаются сломать
        mc = MedicineCard.objects.all().filter(user=request.user)
        if not mc.exists():
            raise Http404()
        mc = MedicineCard.objects.get(user=request.user)
        mci = MedicineCardInstance.objects.all().filter(medicine_card=mc)
        if not mci.exists():
            raise Http404()

        mci = MedicineCardInstance.objects.get(medicine_card__user=request.user, pk=mci_pk)
        docs = PrivateDocument.objects.all().filter(mci=mci)
        if len(docs) != 0:
            for i in docs:
                i.upload.delete()
                i.delete()
        mci.delete()
        notification_class = "notification is-info"
        var1 = 'The entry was successfully deleted'
        content = {'var1': var1, 'notification_class': notification_class, 'flag': 1}
        print('+++++')
        return render(request, 'welcome/DeleteMci.html', content)

    content = {'var1': var1, 'notification_class': notification_class, 'mci_pk': mci_pk, 'flag': 0}
    return render(request, 'welcome/DeleteMci.html', content)


# Выбор записи в медицинской карте для удаления
# Select an entry in the medical record to delete
@login_required
def select_for_delete_mci(request):
    if request.user.is_authenticated is False:
        context = {'temp': _('To edit an entry in the medical record, you must log in'), }
        return render(request, 'welcome/SelectForEditDelete.html', context)
    if len(MedicineCard.objects.all().filter(user=request.user)) != 1:
        context = {'temp': _('You do not have medicine card'), }
        return render(request, 'welcome/SelectForEditDelete.html', context)
    mc = MedicineCard.objects.get(user=request.user)
    mci = MedicineCardInstance.objects.all().filter(medicine_card=mc)
    if len(mci) != 0:
        mci_name_list = []
        for i in mci:
            label = str(i.pk) + ' ' + str(i.title) + ' ' + str(i.registration_at)
            mci_name_list.append((i.pk, label))

        class SelectMci(forms.Form):
            pk = forms.ChoiceField(
                choices=mci_name_list,
                required=True,
                label=_('Selecting an Entry')
            )

        form = SelectMci()
        if request.method == 'POST':
            form = SelectMci(request.POST)
            if form.is_valid():
                mci_instance = MedicineCardInstance.objects.get(medicine_card=mc,
                                                                pk=form.cleaned_data['pk'])
                return redirect(reverse('alert-delete-mci', args=[mci_instance.pk]))
        context = {'temp': _('Form for selecting an entry in a medical card record'), 'form': form}
        return render(request, 'welcome/SelectForEditDelete.html', context)
    else:
        context = {'temp': _('You have not added any entry in the medical card record'), }
        return render(request, 'welcome/SelectForEditDelete.html', context)


# Удаление документа из записи в карточке(запрос)
# Deleting a document from an entry in a card (request)
class DeleteDocumentFromMci(LoginRequiredMixin, DeleteView, ):
    model = PrivateDocument

    def get_success_url(self):
        self.success_url = reverse_lazy('add-attach-medicine-card-instance', args=[self.kwargs['mci_pk']])
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

    def form_valid(self, form, **kwargs):
        mci = PrivateDocument.objects.get(pk=self.object.pk).mci
        if self.request.user == MedicineCard.objects.get(medicinecardinstance=mci).user:
            self.object = self.get_object()
            self.object.upload.delete()
            self.object.delete()
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            raise Http404()


# Функция редактирования записи в медицинской карте (не вложения к этой записи)
# The function of editing an entry in the medical record (not attachments to this entry)
class EditMedicineCardInstance(LoginRequiredMixin, UpdateView):
    model = MedicineCardInstance
    form_class = EditMedicineCardInstance
    success_url = reverse_lazy('show-all-medicine-card-instances')

    def get_queryset(self):
        return MedicineCardInstance.objects.filter(medicine_card__user=self.request.user)


# Добавление вложений в запись в медицинской карточке
# Adding attachments to a medical record entry
@login_required
def add_attach_medicine_card_instance(request, mci_id):
    mci = MedicineCardInstance.objects.get(pk=mci_id)
    if request.user == mci.medicine_card.user:
        mc = MedicineCard.objects.get(user=request.user)
        all_mci = MedicineCardInstance.objects.all().filter(medicine_card=mc)
        documents = PrivateDocument.objects.all().filter(mci=mci)
        document = PrivateDocument()
        document.mci = mci
        documents_url = []
        for i in documents:
            if check_file_type(i.upload.file)['type'] == 'pictures':
                documents_url.append(i.upload.url)
        size = 0
        for i in all_mci:
            temp_size = 0
            mci_documents = PrivateDocument.objects.all().filter(mci=i)
            for z in mci_documents:
                temp_size = z.upload.size
            size = size + temp_size
        # Проверка на общий объем загруженных документов.
        if size > 100000000:
            flag = False
            context = {
                'temp': _(
                    'Unfortunately, you have uploaded the maximum possible amount of documents, in order to upload new documents, delete some of the old documents or contact the project administration.'),
                'mci': mci, 'documents': documents, 'documents_url': documents_url, 'flag': flag}
            return render(request, 'welcome/Add_Attach_MedCardInst.html', context)
        form = AddPrivateDocument(instance=document)
        if request.method == "POST":
            form = AddPrivateDocument(request.POST, request.FILES, instance=document)
            if form.is_valid():
                form.save()
                document = PrivateDocument()
                document.mci = mci
                form = AddPrivateDocument(instance=document)
                documents = PrivateDocument.objects.all().filter(mci=mci)
                documents_url = []
                for i in documents:
                    if check_file_type(i.upload.file)['type'] == 'pictures':
                        documents_url.append(i.upload.url)
                context = {'temp': _('Add attachments to a medical card entry'),
                           'mci': mci, 'form': form, 'documents': documents, 'documents_url': documents_url}
                return render(request, 'welcome/Add_Attach_MedCardInst.html', context)
        context = {'temp': _('Add attachments to a medical card entry'),
                   'mci': mci, 'form': form, 'documents': documents, 'documents_url': documents_url}
        return render(request, 'welcome/Add_Attach_MedCardInst.html', context)
    else:
        raise Http404()


# Функция добавления новой записи в карточку
# The function of adding a new entry to the card
class AddMedicineCardInstance(LoginRequiredMixin, CreateView):
    model = MedicineCardInstance
    form_class = AddMedicineCardInstance
    success_url = reverse_lazy('add-medicine-card-instance')

    def form_valid(self, form):
        if MedicineCard.objects.filter(user=self.request.user).exists():
            medicine_card = MedicineCard.objects.get(user=self.request.user)
            form.instance.medicine_card = medicine_card
            return super().form_valid(form)
        return render(self.request, 'notification/create_medical_card_for_mci.html')


def index(request):
    if request.user.is_authenticated:
        m_cards = MedicineCard.objects.all().filter(user=request.user)
        if len(m_cards) != 0:
            context = {'temp': ''}
            return render(request, 'welcome/index.html', context)
        else:
            context = {
                'temp': _(
                    'To start using the system, you need to create a list of medical institutions and your medical card.')}
            return render(request, 'welcome/index.html', context)

    context = {
        'temp': _(
            'You are on the main page of the project, my medical card, in order to start using the resource, please log in to the site.'), }
    return render(request, 'welcome/index.html', context)
