from django.test import TestCase

# Create your tests here.
# Добавление медицинской карточки
# Adding a medical card
# @login_required
# def mc_add(request):
#     if request.user.is_authenticated is False:
#         content = {'temp': _('To add a medical card, you need to log in')}
#         return render(request, 'AddMc.html', content)
#     mc = MedicineCard.objects.all().filter(user=request.user)
#     if len(mc) == 1:
#         content = {'temp': _('You already have a medical card')}
#         return render(request, 'AddMc.html', content)
#     mc = MedicineCard()
#     mc.user = request.user
#     form = AddMedicineCard(instance=mc)
#     if request.method == 'POST':
#         form = AddMedicineCard(request.POST, instance=mc)
#         if form.is_valid():
#             form.save()
#             content = {'temp': _('You have successfully created a medical card')}
#             return render(request, 'AddMc.html', content)
#     content = {'temp': _('Adding a medical card'), 'form': form}
#     return render(request, 'AddMc.html', content)

# Открывает запись в медицинской карте с возможностью печати или импорта в PDF
# Opens a record in a medical card record with the option to print or import to PDF
# @login_required
# def show_mci_for_print(request, mci_pk):
#     if len(MedicineCard.objects.all().filter(user=request.user)) != 1:
#         raise Http404()
#     mci = MedicineCardInstance.objects.get(pk=mci_pk)
#     if mci.medicine_card.user != request.user:
#         raise Http404()
#     documents = PrivateDocument.objects.all().filter(mci=mci)
#     documents_url = []
#     for i in documents:
#         if check_file_type(i.upload.file)['type'] == 'pictures':
#             documents_url.append(i.upload.url)
#     content = {'mci': mci, 'documents_url': documents_url}
#     return render(request, 'temp/ShowMciForPrint.html', content)

# # Формирует PDF с текстовой информацией из записи в медицинской карте.
# # Generates a PDF with textual information from a record in a medical card.
# @login_required
# def get_pdf(request, mci_pk):
#     if len(MedicineCard.objects.all().filter(user=request.user)) != 1:
#         raise Http404()
#     mci = MedicineCardInstance.objects.get(pk=mci_pk)
#     if mci.medicine_card.user != request.user:
#         raise Http404()
#
#     buf = io.BytesIO()
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=1)
#     textob = c.beginText()
#     textob.setTextOrigin(inch, inch)
#     pdfmetrics.registerFont(
#         TTFont('FreeSans', 'https://medical-card1.s3.eu-central-1.amazonaws.com/static/FreeSans.ttf'))
#     textob.setFont('FreeSans', 16)
#     textob.moveCursor(0, -650)
#
#     registration_number = _('Registration number: ') + str(mci.pk)
#     registration_at = _('Date: ') + str(mci.registration_at)
#     try:
#         mci_title = _("Short description: ") + mci.title
#         textob.textLine(mci_title)
#     except:
#         pass
#     mci_p_age = _("Full years at the time the record was created: ") + str(mci.p_age)
#     try:
#         mci_medical_field = _('Medical field: ') + mci.medical_field.name
#         textob.textLine(mci_medical_field)
#     except:
#         pass
#     try:
#         mci_doctors = _('Attending doctor: ') + mci.doctors.name
#         textob.textLine(mci_doctors)
#     except:
#         pass
#     try:
#         mci_medical_establishments = _('Medical facility: ') + mci.medical_Establishments.name
#         textob.textLine(mci_medical_establishments)
#     except:
#         pass
#     textob.textLine(registration_number)
#     textob.textLine(registration_at)
#     textob.textLine(mci_p_age)
#
#     description = _('Description:') + ''
#     textob.textLine(description)
#     lines = textwrap.wrap(mci.description, 60)
#     i = 0
#     for line in lines:
#         textob.textLine(line)
#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)
#     filename = 'MCI_'+str(mci_pk)+'.pdf'
#     return FileResponse(buf, as_attachment=True, filename=filename)


# Удаление документа из записи в карточке(запрос)
# Deleting a document from an entry in a card (request)
# @login_required
# def delete_document_from_mci_request(request, doc_id, mci_pk):
#     mc = MedicineCard.objects.all().filter(user=request.user)
#     if len(mc) == 0:
#         content = {'temp': _("You don't have a medical card"), 'var1': 0}
#         return render(request, 'DeleteDocument.html', content)
#     mc = MedicineCard.objects.get(user=request.user)
#     docs = PrivateDocument.objects.all().filter(mci__medicine_card=mc)
#     if len(docs) == 0:
#         content = {'temp': _('You do not have documents to delete'), 'var1': 0}
#         return render(request, 'DeleteDocument.html', content)
#     doc = docs.filter(pk=doc_id)
#     if len(doc) != 1:
#         content = {'temp': _('You cannot delete this document'), 'var1': 0}
#         return render(request, 'DeleteDocument.html', content)
#     doc = docs.get(pk=doc_id)
#     temp = _('Are you sure you want to delete the document? ') + str(doc.upload.file)
#     if request.method == 'POST':
#         doc.upload.delete()
#         doc.delete()
#         notification_class = "notification is-info"
#         var2 = _("You have successfully deleted the attached file")
#         content = {'temp': temp, 'var1': 0, 'var2': var2, 'doc': doc, 'mci_pk': mci_pk,
#                    'notification_class': notification_class}
#         return render(request, 'DeleteDocument.html', content)
#
#     content = {'temp': temp, 'var1': 1, 'doc': doc, 'mci_pk': mci_pk}
#     return render(request, 'DeleteDocument.html', content)



# # Функция добавления новой записи в карточку
# # The function of adding a new entry to the card
# @login_required
# def add_medicine_card_instance(request):
#     if request.user.is_authenticated:
#         medicine_card = MedicineCard.objects.all().filter(user=request.user)
#         if len(medicine_card) == 1:
#             medicine_card = MedicineCard.objects.get(user=request.user)
#             medicine_card_inst = MedicineCardInstance()
#             medicine_card_inst.medicine_card = medicine_card
#             form = AddMedicineCardInstance(instance=medicine_card_inst)
#             if request.method == 'POST':
#                 form = AddMedicineCardInstance(request.POST, instance=medicine_card_inst)
#                 if form.is_valid():
#                     form.save()
#                     return redirect(reverse('add-attach-medicine-card-instance', args=[medicine_card_inst.pk]))
#             context = {'temp': _('Adding a new entry to the medical card record'), 'form': form}
#             return render(request, 'Add_Doctor_MF_MCI_ME.html', context)
#         else:
#             context = {'temp': _('To add an entry to the medical card, you must create a medical card'), }
#             return render(request, 'Add_Doctor_MF_MCI_ME.html', context)
#     else:
#         context = {'temp': _('To add an entry to the medical card, you must log in'), }
#         return render(request, 'Add_Doctor_MF_MCI_ME.html', context)

# Просмотр списка записей в медицинской карте + их фильтрация
# Viewing the list of entries in the medical record + filtering them
# @login_required
# def show_all_medicine_card_instances(request):
#     mc = MedicineCard.objects.all().filter(user=request.user)
#     if len(mc) == 1:
#         mc = MedicineCard.objects.get(user=request.user)
#         all_mci = MedicineCardInstance.objects.all().filter(medicine_card=mc).order_by('registration_at')
#         if all_mci != 0:
#
#             time_range = [
#                 (None, '------'),
#                 (1, _('1 month')),
#                 (6, _('6 month')),
#                 (12, _('1 year')),
#                 (24, _('2 year')),
#                 (36, _('3 year')),
#                 (60, _('5 year')),
#             ]
#             doctors_list = [(None, '------')]
#             doctors = Doctors.objects.all().filter(user=request.user)
#             for i in doctors:
#                 doctors_list.append((i.name, i.name))
#
#             medical_establishments_list = [(None, '------')]
#             medical_establishments = MedicalEstablishments.objects.all().filter(user=request.user)
#             for i in medical_establishments:
#                 medical_establishments_list.append((i.name, i.name))
#
#             medical_field_list = [(None, '------')]
#             medical_field = MedicalField.objects.all().filter(user=request.user)
#             for i in medical_field:
#                 medical_field_list.append((i.name, i.name))
#
#             class FilterForm(forms.Form):
#                 time = forms.ChoiceField(
#                     choices=time_range,
#                     label=_('Time range'),
#                     required=False,
#
#                 )
#                 doctor = forms.ChoiceField(
#                     choices=doctors_list,
#                     label=_('Doctor'),
#                     required=False,
#                 )
#                 medical_establishments = forms.ChoiceField(
#                     choices=medical_establishments_list,
#                     label=_('Medical facility'),
#                     required=False,
#                 )
#                 medical_field = forms.ChoiceField(
#                     choices=medical_field_list,
#                     label=_('Medical field'),
#                     required=False,
#
#                 )
#
#             form = FilterForm()
#             if request.method == "POST":
#                 form = FilterForm(request.POST)
#                 if form.is_valid():
#                     t1 = (form.cleaned_data['time'])
#                     if t1 == '': t1 = None
#                     d2 = (form.cleaned_data['doctor'])
#                     if d2 == '': d2 = None
#                     me3 = (form.cleaned_data['medical_establishments'])
#                     if me3 == '': me3 = None
#                     mf4 = (form.cleaned_data['medical_field'])
#                     if mf4 == '': mf4 = None
#                     mci = MedicineCardInstance.objects.all().all().filter(medicine_card__user=request.user)
#
#                     if t1 is not None:
#                         enddate = date.today()
#                         startdate = enddate - timedelta(days=float(t1) * 30.4167)
#                         if d2 is None and me3 is not None and mf4 is not None and t1 is not None:
#                             all_mci = mci.filter(medical_Establishments__name=me3). \
#                                 filter(medical_field__name=mf4).filter(registration_at__range=[startdate, enddate])
#                         elif me3 is None and d2 is not None and mf4 is not None and t1 is not None:
#                             all_mci = mci.filter(doctors__name=d2). \
#                                 filter(medical_field__name=mf4).filter(registration_at__range=[startdate, enddate])
#                         elif mf4 is None and d2 is not None and me3 is not None and t1 is not None:
#                             all_mci = mci.filter(doctors__name=d2).filter(medical_Establishments__name=me3) \
#                                 .filter(registration_at__range=[startdate, enddate])
#                         elif d2 is None and me3 is None and mf4 is not None and t1 is not None:
#                             all_mci = mci.filter(medical_field__name=mf4).filter(
#                                 registration_at__range=[startdate, enddate])
#                         elif d2 is None and mf4 is None and me3 is not None and t1 is not None:
#                             all_mci = mci.filter(medical_Establishments__name=me3). \
#                                 filter(registration_at__range=[startdate, enddate])
#                         elif me3 is None and mf4 is None and d2 is not None and t1 is not None:
#                             all_mci = mci.filter(doctors__name=d2).filter(registration_at__range=[startdate, enddate])
#                         elif d2 is None and me3 is None and mf4 is None and t1 is not None:
#                             all_mci = mci.filter(registration_at__range=[startdate, enddate])
#
#                     if t1 is None and d2 is None and me3 is None and mf4 is None:
#                         all_mci = mci
#                     elif t1 is None and d2 is not None and me3 is not None and mf4 is not None:
#                         all_mci = mci.filter(doctors__name=d2).filter(medical_Establishments__name=me3). \
#                             filter(medical_field__name=mf4)
#                     elif t1 is None and d2 is None and me3 is not None and mf4 is not None:
#                         all_mci = mci.filter(medical_Establishments__name=me3).filter(medical_field__name=mf4)
#                     elif t1 is None and me3 is None and d2 is not None and mf4 is not None:
#                         all_mci = mci.filter(doctors__name=d2).filter(medical_field__name=mf4)
#                     elif t1 is None and mf4 is None and d2 is not None and me3 is not None:
#                         all_mci = mci.filter(doctors__name=d2).filter(medical_Establishments__name=me3)
#                     elif t1 is None and me3 is None and mf4 is None and d2 is not None:
#                         all_mci = mci.filter(doctors__name=d2)
#                     elif t1 is None and d2 is None and mf4 is None and me3 is not None:
#                         all_mci = mci.filter(medical_Establishments__name=me3)
#                     elif t1 is None and d2 is None and me3 is None and mf4 is not None:
#                         all_mci = mci.filter(medical_field__name=mf4)
#                     elif t1 is None and d2 is not None and me3 is not None and mf4 is not None:
#                         enddate = date.today()
#                         startdate = enddate - timedelta(days=float(t1) * 30.4167)
#                         all_mci = mci.filter(doctors__name=d2).filter(medical_Establishments__name=me3). \
#                             filter(medical_field__name=mf4).filter(registration_at__range=[startdate, enddate])
#                     page = Custom_paginator(request, all_mci)
#                     context = {'temp': _('Viewing records in the medical card'), 'all_mci': page.object_list,
#                                'page': page, 'form': form}
#                     return render(request, 'AllMedCardInsts.html', context)
#
#             page = Custom_paginator(request, all_mci)
#             context = {'temp': _('Viewing records in the medical card'), 'all_mci': page.object_list,
#                        'page': page, 'form': form}
#             return render(request, 'AllMedCardInsts.html', context)
#         else:
#             context = {'temp': _("You don't have any records in medical card to view")}
#             return render(request, 'AllMedCardInsts.html', context)
#     else:
#         context = {'temp': _('To view records in a medical card, you first need to add it')}
#         return render(request, 'AllMedCardInsts.html', context)

#~ msgid "Uploaded at"
#~ msgstr "Время загрузки"

#~ msgid "Size"
#~ msgstr "Размер"

#, fuzzy
#~| msgid "Please add medical facilities using the form below."
#~ msgid "Please add doctors using the form below."
#~ msgstr "Пожалуйста добавьте медицинское учреждение используя форму ниже."

#~ msgid "Adding a new field of medicine"
#~ msgstr "Добавление новой области медицины"

#, fuzzy
#~| msgid "Editing a medical facility"
#~ msgid "Editing a medical field"
#~ msgstr "Редактирование медицинского учреждения"

#~ msgid "View/Attachments"
#~ msgstr "Просмотр/Вложения"

#~ msgid "View"
#~ msgstr "Просмотреть"

#~ msgid "Previous page"
#~ msgstr "Предыдущая"

#~ msgid "Next page"
#~ msgstr "Следующая"

#~ msgid "View all entries in the medical record"
#~ msgstr "Просмотр всех записей в медицинской карте"

#~ msgid "Deleting a medical card"
#~ msgstr "Удаление медицинской карты"

#~ msgid "Editing doctors who appear in the records"
#~ msgstr "Редактирование врачей, фигурирующих в записях"

#~ msgid ""
#~ "Editing the areas of medicine that are used in your entries, such as "
#~ "urology"
#~ msgstr ""
#~ "Редактирование областей медицины, которые используются в ваших записях, "
#~ "например урология"

#~ msgid "Deleting entries"
#~ msgstr "Удаление записи"

#~ msgid "Removal of doctors who appear in the records"
#~ msgstr "Удаление врачей, фигурирующих в записях "

#~ msgid "Removing a medical facility"
#~ msgstr "Удаление медицинского учреждения."

#~ msgid ""
#~ "Removing medical fields that are used in your records, such as urology"
#~ msgstr ""
#~ "Удаление медицинских областей, которые используются в ваших записях, "
#~ "например урология"

#~ msgid "Deleting an entry from a medical card record"
#~ msgstr "Удаление записи из медицинской карты"

#~ msgid "Description:"
#~ msgstr "Описание:"

#~ msgid "To edit the field of medicine, you must log in"
#~ msgstr ""
#~ "Для редактирования записей в медицинской карте вам нужно авторизоваться"

#~ msgid "Editing form field of medicine"
#~ msgstr "Форма редактирования области медицины"

#~ msgid "You have not added any field of medicine, there is nothing to edit"
#~ msgstr "Вы еще не добавили ни одной области медицины, редактировать нечего"

#~ msgid "You must be logged in to edit a doctor."
#~ msgstr "Для редактирования врача вам нужно авторизоваться."

#~ msgid "You have not added a single doctor, there is nothing to edit"
#~ msgstr "Вы еще не добавили ни одного врача, редактировать нечего"

#~ msgid "You must be logged in to edit a medical institution."
#~ msgstr "Для редактирования медицинских учреждений вам нежно авторизоваться."

#~ msgid "Select a medical facility to edit"
#~ msgstr "Выберите медицинское учреждение для редактирования"

#~ msgid "You have not added any medical institution, there is nothing to edit"
#~ msgstr ""
#~ "Вы еще не добавили ни одного медицинского учреждения, редактировать "
#~ "нечего."

#~ msgid "To add a medical card, you need to log in"
#~ msgstr "Для добавления записи в медицинскую карту вам нужно авторизоваться"

#~ msgid "You have successfully created a medical card"
#~ msgstr "Вы успешно создали медицинскую карту"

#~ msgid "You don't have a medical card"
#~ msgstr "Вы не имеете медицинской карты"

#~ msgid "You cannot delete this document"
#~ msgstr "Вы не можете удалить этот документ"

#~ msgid "You have successfully deleted the attached file"
#~ msgstr "Вы успешно удалили прикрепленный файл"

#~ msgid "Time range"
#~ msgstr "Временной диапазон"

#~ msgid "Viewing records in the medical card"
#~ msgstr "Просмотр записей в медицинской карте"

#~ msgid "You don't have any records in medical card to view"
#~ msgstr "Вы не имеете записей в медицинской карте для просмотра"

#~ msgid "To view records in a medical card, you first need to add it"
#~ msgstr ""
#~ "Для просмотра записей в медицинской карте вам сначала нужно создать их"

#~ msgid "Editing an entry in a medical record"
#~ msgstr "Редактирование записей в медицинской карте"

#~ msgid "Adding a new entry to the medical card record"
#~ msgstr "Добавление новой записи в медицинскую карту"

#~ msgid "To add an entry to the medical card, you must log in"
#~ msgstr "Для добавления записи в медицинской карте вам нужно авторизоваться"

#~ msgid "Medical area added, if needed you can add another area of medicine"
#~ msgstr ""
#~ "Область медицины успешно добавлена, если это необходимо вы можете "
#~ "добавить еще одну область медицины"

#~ msgid "You must be logged in to add a field of medicine."
#~ msgstr "Вы должны быть авторизованны для добавления новой области медицины"

#~ msgid "Data has been edited successfully"
#~ msgstr "Дата успешно отредактирована"

#~ msgid "Medical field editing form"
#~ msgstr "Форма редактирования области медицины"

#~ msgid "Select the area of medicine to remove"
#~ msgstr "Выберите область медицины для удаления"

#~ msgid "  these records Id: "
#~ msgstr " id этих записей: "

#~ msgid "The medical field has been successfully deleted"
#~ msgstr "Область медицины успешно удалена"

#~ msgid ""
#~ "You have not added a single field of medicine, there is nothing to delete"
#~ msgstr "У вас не добавлено ни одной области медицины, удалять нечего"

#~ msgid ""
#~ "An unexpected error has occurred, you may have already deleted this "
#~ "medical area in another browser window, try to perform the operation again"
#~ msgstr ""
#~ "Обнаружена не предвиденная ошибка, возможно вы уже удалили эту область "
#~ "медицины в другом окне браузера, попробуйте произвести операцию еще раз"

#~ msgid "Deleting a Medical Area"
#~ msgstr "Удаление области медицины"

#~ msgid "To delete a field of medicine, log in"
#~ msgstr "Для удаления области медицины необходимо авторизоваться"

#~ msgid "Choose a doctor to remove"
#~ msgstr "Выберите доктора для удаления"

#~ msgid " these records Id : "
#~ msgstr " id этих записей"

#~ msgid "The doctor was successfully removed"
#~ msgstr "Врач был успешно удален"

#~ msgid "You have not added a single doctor, there is nothing to delete"
#~ msgstr "У вас не добавлено ни одного врача, нечего удалять"

#~ msgid ""
#~ "An unexpected error has occurred, you may have already deleted this "
#~ "doctor in another browser window, try to perform the operation again"
#~ msgstr ""
#~ "Обнаружена не предвиденная ошибка, возможно вы уже удалили этого врача в "
#~ "другом окне браузера, попробуйте произвести операцию еще раз"

#~ msgid "Removing a doctor"
#~ msgstr "Удаление врача"

#~ msgid "You must be logged in to delete a doctor."
#~ msgstr "Для удаления врача вам нужно авторизоваться"

#~ msgid "You already have a doctor with that name"
#~ msgstr "Вы уже имеете врача с таким именем"

#~ msgid ""
#~ "The doctor has been successfully added, if necessary, you can add another "
#~ "doctor."
#~ msgstr ""
#~ "Врач был успешно добавлен, если это необходимо вы можете добавить еще "
#~ "одного врача"

#~ msgid "Adding a new doctor"
#~ msgstr "Добавление нового врача"

#~ msgid "You must be logged in to add a doctor."
#~ msgstr "Для добавления врача вам нужно авторизоваться."

#~ msgid "You already have a medical facility with that name with that name."
#~ msgstr "Вы уже имеете медицинское учреждение с таким именем"

#~ msgid "Data has been edited successfully."
#~ msgstr "Данные были успешно добавлены"

#~ msgid ""
#~ "The medical facility data has been successfully added, if necessary, you "
#~ "can add another medical facility."
#~ msgstr ""
#~ "Медицинское учреждение было успешно добавлено, если это необходимо вы "
#~ "можете добавить еще одно медицинское учреждение."

#~ msgid "You must be logged in to add a medical facility."
#~ msgstr "Для добавления медицинского учреждения вам нужно авторизоватся."

#~ msgid "Choose a medical institution for removal"
#~ msgstr "Выберите медицинское учреждение для удаления"

#~ msgid " these records Id: "
#~ msgstr " id этих записей"

#~ msgid "Select a medical facility for removal"
#~ msgstr " Укажите медицинское учреждение для удаления"

#~ msgid "The medical facility has been successfully removed"
#~ msgstr "Медицинское учреждение было успешно удалено"

#~ msgid ""
#~ "You have not added a single medical facility, there is nothing to delete"
#~ msgstr ""
#~ "У вас не добавлено ни одного медицинского учреждения, удалять нечего"

#~ msgid ""
#~ "An unexpected error has occurred, you may have already deleted this "
#~ "medical facility in another browser window, try to perform the operation "
#~ "again"
#~ msgstr ""
#~ "Обнаружена не предвиденная ошибка, возможно вы уже удалили это "
#~ "медицинское учреждение в другом окне браузера, попробуйте произвести "
#~ "операцию еще раз"

#~ msgid "You must be logged in to delete a medical facility."
#~ msgstr "Для удаления медицинского учреждения вам нужно авторизоваться"

#~ msgid ""
#~ "Very often, people are faced with the need to find a new doctor and "
#~ "provide him with his medical history, for example, various tests or "
#~ "diagnoses of previous doctors. Often This analyzes and conclusions are "
#~ "stored with us in paper form or as a set of photographs on the phone, and "
#~ "this is not very convenient. В этм сервисе вы можете создать и хранить "
#~ "свою медецинскую карту вместе с приложением всех заключений врачей, "
#~ "анализов и необходимых цифровых данных, например результаты томограммы, "
#~ "фотографии узи, оцифрованные рентгеновские снимки и так далее."
#~ msgstr ""
#~ "Очень часто люди сталкиваются с необходимостью найти нового врача и "
#~ "предоставить ему свою историю болезни, например, различные исследования "
#~ "или заключения предыдущих врачей. Очень часто эти анализы или заключения "
#~ "хранятся у нас в в бумажном виде или как набор фотографий в нашем "
#~ "телефоне и это не очень удобно. "