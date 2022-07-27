from pathlib import Path
from django.core.paginator import Paginator
from django.shortcuts import render


def delete_mc_notification(request):
    return render(request, 'notification/delete_mc_notification.html')

# Пагинатор
def Custom_paginator(request, orders, order_in_page=20):
    paginator = Paginator(orders, order_in_page)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return page


# Функция проверяет тип файла по расширению
def check_file_type(file_name):
    dangerous_list = ['.exe', '.pif', '.application', '.gadget', '.msi', '.msp', '.com', '.scr', '.hta', '.cpl', '.msc',
                      '.jar', '.bat', '.cmd', '.vb', '.vbs', '.vbe', '.js', '.jse', '.ws', '.wsf', '.wsc', '.wsh',
                      '.ps1', '.ps1xml', '.ps2', '.ps2xml', '.psc1', '.psc2', '.msh', '.msh1', '.msh2', '.mshxml',
                      '.msh1xml', '.msh2xml', '.scf', '.lnk', '.inf', '.reg', '.docm', '.dotm,', '.xlsm', '.xltm',
                      '.xlam', '.pptm', '.potm', '.ppam', '.ppsm'
                      ]
    document_list = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx']
    pictures_list = ['.bmp', '.gif', '.jpg', '.pcx', '.png', '.psd', '.tiff']
    # Картинки
    for i in pictures_list:
        if Path(str(file_name)).suffix.lower() == i:
            return {'status': True, 'type': 'pictures', 'extension': i}
    # Документы
    for i in document_list:
        if Path(str(file_name)).suffix.lower() == i:
            return {'status': True, 'type': 'document', 'extension': i}
    for i in dangerous_list:
        if Path(str(file_name)).suffix.lower() == i:
            return {'status': True, 'type': 'dangerous', 'extension': i}
    return {'status': False, 'type': None, 'extension': None}


# @login_required
# def get_pdf(request, mci_pk):
#
#     buf = io.BytesIO()
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#     textob = c.beginText()
#     textob.setTextOrigin(inch, inch)
#     pdfmetrics.registerFont(TTFont('FreeSans', 'https://medical-card1.s3.eu-central-1.amazonaws.com/static/FreeSans.ttf'))
#     textob.setFont('FreeSans', 16)
#     text = "При вызове add i know методов необходимо помнить, что строки в Python относятся к категории неизменяемых последовательностей, то есть все функции и методы могут лишь создавать новую строку."
#     import textwrap
#     lines = textwrap.wrap(text, 60)
#     print(lines)
#     for line in lines:
#         textob.textLine(line)
#     c.drawText(textob)



    # url = 'http://risovach.ru/upload/2014/02/mem/muzhik-bleat_43233947_orig_.jpg'
    # I = Image.open(urlopen(url))
    # p.drawImage('http://risovach.ru/upload/2014/02/mem/muzhik-bleat_43233947_orig_.jpg', 0, 500)
    # p.showPage()
    # p.drawImage('http://risovach.ru/upload/2014/02/mem/muzhik-bleat_43233947_orig_.jpg', 0, 500)
    # c.showPage()
    # c.save()
    # buf.seek(0)
    # return FileResponse(buf, as_attachment=True, filename='test.pdf')

# def PrintImage(request):
#     response = HttpResponse(content_type='application/pdf')
#     doc = SimpleDocTemplate(response, topMargin=2)
#
#     doc.pagesize = landscape(A6)
#     elements = []
#
#     I.drawHeight = 0.7*inch
#     I.drawWidth = 0.7*inch
#     elements.append(I)
#     doc.build(elements)
#     return response