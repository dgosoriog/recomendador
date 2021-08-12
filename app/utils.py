from functools import wraps
#import tkFileDialog

from flask_login import current_user
from sqlalchemy.orm import class_mapper
from fpdf import FPDF
from flask_mail import Message
from flask import url_for, abort
from app import mail
from app.models import Permission, Alternativas
import xlwt
from datetime import datetime

def MedicionesToExcel(lista):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Mediciones ',cell_overwrite_ok=True)
    ws.write(0, 0, 'Reporte de Mediciones')
    style1 = xlwt.XFStyle()
    style1.num_format_str = 'dd/mm/yyyy'
    columnas = ["Fecha",
                    "Bloque",
                    "Muestreo",
                    "Variedad",
                    "Cama",
		 			"pH",
		 			"Densidad",
		 			"CE",
                    "pH Compost",
                    "Densidad Compost",
                    "CE Compost",
                    "pH Tanque",
                    "CE Tanque",
                    "pH Goteo",
                    "CE Goteo",
		 			"pH Programación",
                    "CE Programación",
                    "Cant. Arroz",
                    "Prom. Arroz",
                    "Cant. Arveja",
                    "Prom. Arveja",
                    "Cant. Garbanzo",
                    "Prom. Garbanzo",
                    "Cant. Lenteja",
                    "Prom. Lenteja",
                    "Cant. Rayando Color",
                    "Prom. Rayando Color",
                    "Cant. Pintando Color",
                    "Prom. Pintando Color",
                    "Cant. Color Def",
                    "Prom. Color Def",
                    ]
    c = 0
    for columna in columnas:
        ws.write(1, c, columna)
        c = c + 1
    fila = 2
    i = 0
    for item in lista:
        print(item)
        for j in item:
            ws.write(fila, i, j)
            i += 1
        fila +=1
        i = 0
        # ws.write(fila, 1, item[1])
        # ws.write(fila, 2, item[2])
        # ws.write(fila, 3, item[3])
        # ws.write(fila, 4, item[4])
        # ws.write(fila, 5, item[5])
        # ws.write(fila, 6, item[6])
        # ws.write(fila, 7, item[7])
        # ws.write(fila, 8, item[8])
        # ws.write(fila, 9, item[9])
        # ws.write(fila, 10, item[10])
        # ws.write(fila, 11, item[11])
        # ws.write(fila, 12, item[12])
        # ws.write(fila, 13, item[13])
        # ws.write(fila, 14, item[14])
        # ws.write(fila, 15, item[15])
        # ws.write(fila, 16, item[16])
        # ws.write(fila, 17, item[17])
        # ws.write(fila, 18, item[18])
        # ws.write(fila, 19, item[19])
        # ws.write(fila, 20, item[20])
        # ws.write(fila, 21, item[21])
        # ws.write(fila, 22, item[22])
        # ws.write(fila, 23, item[23])
        # ws.write(fila, 24, item[24])
        # ws.write(fila, 25, item[25])
        # ws.write(fila, 26, item[26])
        # ws.write(fila, 27, item[27])
        # ws.write(fila, 28, item[28])
        # ws.write(fila, 29, item[29])
        # ws.write(fila, 30, item[30])
        #fila = fila + 1
    return wb
    # def guardarPlanilla(self):
    #     # if not os.path.isdir("DirectoryName"):
    #     #     os.makedirs("DirectoryName")
    #     #
    #     # if not os.path.isfile('FileName.xlsx'):
    #     #     wb = openpyxl.Workbook(
    #     #     dest_filename = 'FileName.xlsx'
    #     #     self.wb.save(os.path.join('DirectoryName', dest_filename), as_template=False)
    #     # #self.wb.save(save_spot)
    #     print("Generado")
    #     return self.wb


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                    abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Solicitud para reestablecer contraseña',
                  sender='floricolaasistente5@gmail@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Para reestablecer tu contraseña, visita el siguiente link:
{url_for('reset_token', token=token, _external=True)}
Si no hiciste esta solicitud simplemente ignora este correo y no se hará ningún cambio.
'''
    mail.send(msg)

def alternativas_todict():
    alt = {
        Alternativas.A0 : 'No hacer nada',
        Alternativas.A1 : 'Incorporar Compost o Cambio de lugar',
        Alternativas.A2 : 'Drenchado,Trinchar camas o Levantar camas',
        Alternativas.A3 : 'Aplicar sulfato de calcio o Aplicar nitrato de calcio',
        Alternativas.A4 : 'Aplicar sulfato de amonio o Aplicar nitrato de amonio'
    }

    return alt

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('app/static/images/hoja.png', 10, 8, 20)
        # helvetica bold 15
        self.set_font('helvetica', 'B', 15)
        self.page_width = self.w - 2 * self.l_margin
        # Title
        self.cell(self.page_width, 0.0, 'Reporte de Recomendaciones', align='C')
        # Line break
        # self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

