from fpdf import FPDF

class GeneradorRecetas(FPDF):
    
    def header(self):
        self.set_font("Times","BU",14)
        self.cell(0,10,"Receta médica",0,1,"C")
        
    
    # def footer(self):
    #     self.set_y(-15)
    #     self.set_font("Arial","I",8)
    #     self.cell(0,10,"Página %s"% self.page_no(),0,0,"C")
    
    def chapter_body(self, datos):
        self.set_font("Arial", "", 10)
        self.set_fill_color(255, 250, 250)
        
        labels = [
            "Fecha", "Hora", "Consultorio", "Paciente", "Altura", "Peso", "Edad", "Temperatura", 
            "Oxigenación", "Glucosa","Latidos por Minuto", "Sintomas", "Diagnostico", "Tratamiento",
            "Estudios"
        ]
        
        for label, data in zip(labels, datos):
            self.cell(50, 10, label, 0, 0, 'L', True)
            self.cell(0, 10, str(data), 0, 1, 'L', True)
            self.ln(2)
        
        