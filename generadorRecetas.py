from fpdf import FPDF

class GeneradorRecetas(FPDF):
    def __init__(self,datosDoctor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datosDoctor = datosDoctor
        
    def header(self):
        # Logo (si tienes una imagen, puedes agregarla aquí con self.image())
        self.image('static/images/logo.png', x=10, y=8, w=33)
        
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Doctor: ' + self.datosDoctor['Doctor'] , ln=True, align='C')
        self.cell(0, 10, 'Cédula Profesional: ' + self.datosDoctor['Cedula'], ln=True, align='C')
        self.cell(0, 10, 'Consultorio: ' + self.datosDoctor['Consultorio'], ln=True,align='C')

    def footer(self):
        # Posicionarse a 1.5 cm del final
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Horario de Lunes a Viernes 15:00 a 21:00 horas', 0, 0, 'L')
        self.cell(0, 10, 'Firma del medico', 0, 0, 'R')

    def chapter_body(self):
        
        total_width = self.w - 2 * self.l_margin
        cell_width1 = total_width / 3
        cell_width2 = total_width / 5

        self.set_x((self.w - total_width) / 2)

        self.set_font('Arial', '', 12)

        
        self.set_y(self.get_y() + 10)
        self.cell(cell_width1, 10, 'Paciente: ' + self.datosDoctor['Paciente'], ln=0)
        self.cell(cell_width1, 10, 'Edad: ' + self.datosDoctor['Edad'], ln=0)
        self.cell(cell_width1, 10, 'Fecha: ' + self.datosDoctor['Fecha'] + ' ' + self.datosDoctor['Hora'], ln=0)


        self.set_y(self.get_y() + 10)  

        
        self.set_line_width(0.5)

        x = self.get_x() 
        self.line(x, self.get_y(), total_width, self.get_y())

        
        self.set_y(self.get_y() + 5)  
        self.cell(cell_width2, 10, 'Altura: ' + self.datosDoctor['Altura'], ln=0)
        self.cell(cell_width2, 10, 'Peso: ' + self.datosDoctor['Peso'], ln=0)
    
    
        self.set_y(self.get_y() + 20)
        self.cell(cell_width2, 10, 'Temperatura: ' + self.datosDoctor['Temperatura'], ln=0)
        self.cell(cell_width2, 10, 'Oxigenación: ' + self.datosDoctor['Oxigenacion'], ln=0)
        self.cell(cell_width2, 10, 'Glucosa: ' + self.datosDoctor['Glucosa'], ln=0)
        self.cell(cell_width2, 10, 'BPM: ' + self.datosDoctor['BPM'], ln=0)

        
        self.set_y(self.get_y() + 20)
        
        self.cell(0, 10, 'Sintomas: ' + self.datosDoctor['Sintomas'], ln=True)
        self.set_y(self.get_y() + 10)
        
        self.cell(0, 10, 'Diagnostico: ' + self.datosDoctor['Diagnostico'], ln=True)
        self.set_y(self.get_y() + 10)
        
        self.cell(0, 10, 'Tratamiento: ' + self.datosDoctor['Tratamiento'], ln=True)
        self.set_y(self.get_y() + 10)
        
        self.cell(0, 10, 'Estudios: ' + self.datosDoctor['Estudios'], ln=True)

