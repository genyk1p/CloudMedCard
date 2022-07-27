from django.urls import path
from welcome.views import *

urlpatterns = [
    path('', index, name='index'),
    path('add-medical-establishments', AddMedicalEstablishment.as_view(), name='add-medical-establishments'),
    path('delete-medical-establishments/<int:pk>', DeleteMedicalEstablishment.as_view(),
         name='delete-medical-establishments'),
    path('predelete-medical-establishments/<int:pk>', pre_delete_medical_establishments, name='predelete-medical-establishments'),
    path('delete-doctor/<int:pk>', DeleteDoctor.as_view(), name='delete-doctor'),
    path('predelete-doctor/<int:pk>', pre_delete_doctor, name='predelete-doctor'),
    path('add-medical-field', AddMedicalMedicalField.as_view(), name='add-medical-field'),
    path('delete-medical-field/<int:pk>', DeleteMedicalField.as_view(), name='delete-medical-field'),
    path('predelete-medical-field/<int:pk>', pre_delete_medical_field, name='predelete-medical-field'),
    path('add-medicine-card-instance', AddMedicineCardInstance.as_view(), name='add-medicine-card-instance'),
    path('show-all-medicine-card-instances', ShowAllMedicineCardInstances.as_view(), name='show-all-medicine-card-instances'),
    path('add-attach-medicine-card-instance/<int:mci_id>', add_attach_medicine_card_instance,
         name='add-attach-medicine-card-instance'),
    path('delete-document-from-mci-request/<int:pk>/<int:mci_pk>', DeleteDocumentFromMci.as_view(),
         name='delete-document-from-mci-request'),
    path('mc-add', AddAddMedicineCard.as_view(), name='mc-add'),
    path('edit-mc', edit_mc, name='edit-mc'),
    path('select-for-delete-mci', select_for_delete_mci, name='select-for-delete-mci'),
    path('alert-delete-mci/<int:mci_pk>', alert_delete_mci, name='alert-delete-mci'),
    path('edit-medicine-card-instance/<int:pk>', EditMedicineCardInstance.as_view(), name='edit-medicine-card'
                                                                                              '-instance'),
    path('show-mci-for-print/<int:pk>', ShowMciForPrint.as_view(), name='show-mci-for-print'),
    path('show-doctor', ShowAllDoctor.as_view(), name='show_all_doctor'),
    path('edit-doctor/<int:pk>', EditDoctor.as_view(), name='edit-doctor'),
    path('show-medical-field', ShowAllMedicalField.as_view(), name='show-medical-field'),
    path('edit-medical-field/<int:pk>', EditMedicalField.as_view(), name='edit-medical-field'),
    path('show-medical-establishments', ShowAllMedicalEstablishment.as_view(), name='show-medical-establishments'),
    path('edit-medical-establishments/<int:pk>', EditMedicalEstablishment.as_view(), name='edit-medical-establishments'),
    path('add-doctor', AddDoctor.as_view(), name='add-doctor'),
    path('delete-mc-notification', delete_mc_notification, name='delete-mc-notification'),
]







