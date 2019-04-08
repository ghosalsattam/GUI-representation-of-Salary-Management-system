from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
width, height = A4

def generatePdf(filename,
                id,
                name,
                designation,
                originalPay,
                originalPayGrade,
                DOJ,
                pan,
                da, hra, ta, incomeTax, professionTax,
                presentPay, totalEarnings, totalDeductions,
                netPay,
                month, year):

    # -----------------------[ Page Generation ]-----------------------

    pageElements = []

    logo = Image("Resources/iiitk.png")
    logo.drawHeight = 1.5*inch
    logo.drawWidth = 1.5*inch

    header =\
    '''
    <para align="center">
        <font face="times">
            <font size=16><b>INDIAN INSTITUTE OF INFORMATION TECHNOLOGY</b></font>
            <br></br>
            <font size=13>
                (Autonomous Institute under MHRD, Govt. of India
                <br></br>
                & Department of Information Technology & Electronics, Govt. of West Bengal)
                <br></br>
                C/o WEBEL IT Park, Opposite Water Treatment Plant
                <br></br>
                Near Buddha Park, Dist-Nadia, P.O-Kalyani, PIN-741235,
                <br></br>
                Email-ID iiitkalyani.office@gmail.com Website www.iiitkalyani.ac.in
                
            </font>       
        </font>   
    </para>
    '''
    p = Paragraph(header, ParagraphStyle('Normal', leading=15))
    htable = Table([[logo, p]], colWidths=[1.5*inch, 6*inch])
    htable.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (1, 0), "CENTER"),
                                ('BOTTOMPADDING', (0,0), (1,0), 15),
                                ('VALIGN', (0, 0), (1, 0), 'MIDDLE'),
                                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)]))
    pageElements.append(htable)

    monthYear =\
    '''
    <para align="center">
    <font face="times" size=16>
        <br></br>
        <br></br>
        <b>Salary for the month of %s, %d</b>
    </font>
    </para>
    '''
    monthYear = monthYear % (month.upper(), year)

    # pageElements.append(Paragraph(header, ParagraphStyle('Normal', leading=15)))
    pageElements.append(Paragraph(monthYear, ParagraphStyle('Normal', leading=15)))

    info = \
    [
        ("ID No.", ":", id),
        ("Name", ":",name),
        ("Designation", ":",designation),
        ("Original Pay", ":","%0.2f Rs."%originalPay),
        ("Original Grade Pay", ":","%0.2f Rs."%originalPayGrade),
        ("Date of joining", ":","%s"%DOJ),
        ("Pan No.", ":",pan)
    ]
    infotable = Table(info, colWidths=[130,10,130], rowHeights=15, spaceBefore=30, hAlign="LEFT")
    infotable.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 12),
                                   ('TEXTFONT', (0,0), (-1,-1), 'Times')]))

    pageElements.append(infotable)


    data =\
    [
        ("EARNINGS", " ", "DEDUCTIONS", " "),
        ("Present Pay", presentPay, "Income Tax", incomeTax),
        ("Dearness Allowance", da, "Profession Tax", professionTax),
        ("House Rent Allowance", hra),
        ("Transport Allowance", ta),
        (" "),
        ("Gross Earnings", totalEarnings, "Gross Deductions", totalDeductions),
        (" "),
        (" ", " ", "Net Pay", netPay)
    ]
    table = Table(data, colWidths=[150, 100, 150, 100], rowHeights=25,spaceBefore=30)
    table.setStyle(TableStyle([('SPAN', (0, 0), (1, 0)),
                               ('SPAN', (2, 0), (3, 0)),
                               ('ALIGN', (0, 0), (3, 0), "CENTER"),
                               ('VALIGN',(0,0),(-1,-1),'TOP'),
                               ('LINEABOVE', (0,0), (-1,0), 1.3, colors.black),
                               ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                               ('LINEABOVE', (0, 6), (-1, 6), 1, colors.black),
                               ('LINEABOVE', (0, 8), (-1, 8), 1, colors.black),
                               ('LINEBELOW', (0, 8), (-1, 8), 1.3, colors.black),
                               # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('TEXTFONT', (0, 0), (-1, -1), 'Times')]))
    pageElements.append(table)


    signatureText =\
    '''
    <para align="right">
        <font face="times" size=13>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            Assistant Registrar (Finance)
        </font>
    </para>
    '''
    pageElements.append(Paragraph(signatureText, ParagraphStyle('Normal', leading=15)))

    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)
    doc.build(pageElements)


if __name__ == "__main__":
    generatePdf("test.pdf", "RANDOM001", "John Doe", "Nobody", 80000, 10000, "12/12/12", "ABCPD1234E",
                120.0, 100, 10, 20, 30, 90000, 100000, 80000, 20000,"February",2019)
