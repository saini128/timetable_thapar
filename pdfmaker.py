import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle

def create_timetable_pdf(json_file, output_pdf):
    with open(json_file, 'r') as file:
        timetable_data = json.load(file)

    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf.setTitle("Timetable")

    
    pdf.setFont("Helvetica", 12)

    
    y_coordinate = pdf._pagesize[1] - 40

    
    for day, classes in timetable_data.items():
        
        pdf.drawString(100, y_coordinate, day)
        y_coordinate -= 20  

        
        table_data = [["Time", "Subject", "Venue"]]

        
        for class_info in classes:
            time = class_info["time"]
            class_name = class_info["class"]
            venue = class_info["venue"]

            
            table_data.append([time, class_name, venue])

            y_coordinate -= 20  

        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
            ('BOX', (0, 0), (-1, -1), 0.25, 'black'),
        ]))

        
        table.wrapOn(pdf, 400, 600)  
        table.drawOn(pdf, 100, y_coordinate)

        
        y_coordinate -= 20  
        # pdf.drawString(100, y_coordinate, "-" * 60)
        # y_coordinate -= 10  

    pdf.save()

if __name__ == "__main__":
    json_file_path = "2 CO 36 output.json"
    output_pdf_path = "2 CO 36 timetable.pdf"
    create_timetable_pdf(json_file_path, output_pdf_path)
