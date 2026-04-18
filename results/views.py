from django.shortcuts import get_object_or_404, render , redirect
from .models import Result
from .forms import SemesterSelectForm
from accounts.models import CustomUser
from django.http import HttpResponse, HttpResponseForbidden
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Flowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.contrib.auth.decorators import login_required

@login_required
def form_result(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        return redirect("login")
    
    # ensure student has some result records (for demo/testing)
    student_obj = request.user
    if not Result.objects.filter(student=student_obj).exists():
        # choose dummy marks depending on stream
        stream = student_obj.stream.lower() if student_obj.stream else ''
        for sem_i in range(1, 7):
            if stream == 'commerce':
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=70, c_sharp=75, php=80, python=60, java=65)
            elif stream == 'science':
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=80, c_sharp=70, php=65, python=75, java=60)
            elif stream == 'arts':
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=65, c_sharp=60, php=75, python=70, java=80)
            else:
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=60, c_sharp=70, php=65, python=80, java=75)
    result = None
    subject_headers = []
    # setup dummy results if needed (kept earlier logic)
    student_obj = request.user
    if not Result.objects.filter(student=student_obj).exists():
        stream = student_obj.stream.lower() if student_obj.stream else ''
        for sem_i in range(1, 7):
            if stream == 'commerce':
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=70, c_sharp=75, php=80, python=60, java=65)
            elif stream == 'science':
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=80, c_sharp=70, php=65, python=75, java=60)
            elif stream == 'arts':
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=65, c_sharp=60, php=75, python=70, java=80)
            else:
                Result.objects.create(student=student_obj, sem=sem_i, ac_year="2025",
                                      seo=60, c_sharp=70, php=65, python=80, java=75)
    if request.method == "POST":
        form = SemesterSelectForm(request.POST)
        if form.is_valid():
            sem = form.cleaned_data['sem']
            try:
                result = Result.objects.get(student=student_obj,sem=sem)
            except Result.DoesNotExist:
                return render(request, "results/form_result.html", {"form": form,"sem_not_found":" Result Not Found "})
            # determine headers by stream
            stream = student_obj.stream.lower() if student_obj.stream else ''
            if stream == 'commerce':
                subject_headers = ['Accounting','Business','Economics','Math','English']
            elif stream == 'science':
                subject_headers = ['Physics','Chemistry','Biology','Math','English']
            elif stream == 'arts':
                subject_headers = ['History','Geography','Political Science','Economics','English']
            else:
                subject_headers = ['SEO','C#','PHP','Python','Java']
    else:
        form = SemesterSelectForm()
    return render(request, "results/form_result.html", {"form": form, "result": result, "subject_headers": subject_headers})

@login_required
def view_result(request,result_id):
    result = Result.objects.get(id=result_id)

    student = request.user

    if request.user != result.student:
        return HttpResponseForbidden("Not allowed!")
    
    # determine subject headers depending on student's stream
    stream = student.stream.lower() if student.stream else ''
    if stream == 'commerce':
        subject_headers = ['Accounting','Business','Economics','Math','English']
        value_fields = ['seo','c_sharp','php','python','java']
    elif stream == 'science':
        subject_headers = ['Physics','Chemistry','Biology','Math','English']
        value_fields = ['seo','c_sharp','php','python','java']
    elif stream == 'arts':
        subject_headers = ['History','Geography','Political Science','Economics','English']
        value_fields = ['seo','c_sharp','php','python','java']
    else:
        subject_headers = ['SEO','C#','PHP','Python','Java']
        value_fields = ['seo','c_sharp','php','python','java']

    return render(request, "results/view_result.html", {
        "result": result,
        "student": student,
        "subject_headers": subject_headers,
        "value_fields": value_fields,
    })


class ReportHeader(Flowable):
    """
    A custom flowable to draw the document header with the university name 
    and a distinct background color band.
    """
    def __init__(self, university_name, title, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.university_name = university_name
        self.title = title

    def draw(self):
        c = self.canv
        
        # 1. Background Color Band (Primary Color: University Blue)
        PRIMARY_COLOR = colors.HexColor('#002D62') # Deep Navy Blue
        c.setFillColor(PRIMARY_COLOR)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)

        # 2. University Name (White, Large, Bold)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(self.width / 2, self.height - 20, self.university_name)

        # 3. Document Title (White, Smaller)
        c.setFont("Helvetica", 12)
        c.drawCentredString(self.width / 2, self.height - 40, self.title)

class VerticalLine(Flowable):
    """A simple flowable to draw a vertical line separator."""
    def __init__(self, height):
        Flowable.__init__(self)
        self.height = height
        self.width = 0 # It's a vertical line

    def draw(self):
        self.canv.line(0, 0, 0, self.height)

# --- PDF Generation Function ---
@login_required
def download_result(request, result_id):
    from .models import Result
    try:
        result = Result.objects.get(id=result_id)
    except Result.DoesNotExist:
        return HttpResponse("Result not found", status=404)

    # --- Setup ---
    response = HttpResponse(content_type='application/pdf')
    filename = f'Result_Sheet_{str(result.student).replace(" ", "_")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Colors and Styles
    PRIMARY_COLOR = colors.HexColor('#002D62') # Deep Navy Blue
    ACCENT_COLOR = colors.HexColor('#F5A623') # Bright Gold/Orange
    PASS_COLOR = colors.HexColor('#008000')   # Green
    FAIL_COLOR = colors.HexColor('#CC0000')   # Red

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='H1_Main', alignment=TA_LEFT, fontSize=16, fontName='Helvetica-Bold', textColor=PRIMARY_COLOR, spaceAfter=8))
    styles.add(ParagraphStyle(name='H2_Sidebar', alignment=TA_LEFT, fontSize=14, fontName='Helvetica-Bold', textColor=colors.black, spaceAfter=8))
    styles.add(ParagraphStyle(name='DataLabel', alignment=TA_LEFT, fontSize=10, fontName='Helvetica-Bold', textColor=colors.HexColor('#666666')))
    styles.add(ParagraphStyle(name='DataValue', alignment=TA_LEFT, fontSize=12, fontName='Helvetica', spaceAfter=10))
    styles.add(ParagraphStyle(name='FinalGrade', alignment=TA_CENTER, fontSize=36, fontName='Helvetica-Bold', spaceAfter=10, leading=40))

    # Document Template Setup
    pdf = SimpleDocTemplate(
        response, 
        pagesize=A4,
        topMargin=20, # Reduced top margin as header is built-in
        bottomMargin=30,
        leftMargin=50,
        rightMargin=50
    )
    elements = []

    # --- 1. Header (Custom Flowable) ---
    # Width is A4_width - leftMargin - rightMargin
    doc_width = A4[0] - 100 
    elements.append(ReportHeader("ABC UNIVERSITY", "Official Semester Result Statement", doc_width, 60))
    elements.append(Spacer(1, 25))

    # --- 2. Two-Column Layout (Using a Table for structure) ---
    
    # 2a. Left Column (Student Info & Summary)
    summary = result.get_summary() 
    percentage = summary.get('percentage', 0)
    grade = summary.get('grade', 'N/A')
    
    # Determine grade color
    grade_color = PASS_COLOR if grade not in ['F', 'N/A'] else FAIL_COLOR
    
    sidebar_elements = []
    sidebar_elements.append(Paragraph("STUDENT PROFILE", styles['H2_Sidebar']))
    
    # Student Info
    sidebar_elements.append(Paragraph("Student Name:", styles['DataLabel']))
    sidebar_elements.append(Paragraph(str(result.student), styles['DataValue']))
    sidebar_elements.append(Paragraph("Semester:", styles['DataLabel']))
    sidebar_elements.append(Paragraph(str(result.sem), styles['DataValue']))
    sidebar_elements.append(Spacer(1, 20))
    
    # Final Grade Box
    sidebar_elements.append(Paragraph("FINAL GRADE", styles['H2_Sidebar']))
    sidebar_elements.append(Spacer(1, 5))
    
    # FIX APPLIED HERE: Used grade_color.hexval() instead of grade_color.hexa()
    final_grade_p = Paragraph(f"<font color='{grade_color.hexval()}' face='Helvetica-Bold'>{grade}</font>", styles['FinalGrade'])
    
    # Table to style the grade box
    grade_box = Table([[final_grade_p]], colWidths=[180])
    grade_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#FFFDE7')), # Very Light Yellow background
        ('GRID', (0, 0), (0, 0), 1.5, grade_color), # Border matching grade color
        ('PADDING', (0, 0), (0, 0), 10),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
    ]))
    sidebar_elements.append(grade_box)
    sidebar_elements.append(Spacer(1, 15))
    
    # Percentage
    sidebar_elements.append(Paragraph("Total Percentage:", styles['DataLabel']))
    sidebar_elements.append(Paragraph(f"{percentage}%", styles['DataValue']))
    
    sidebar_elements_cell = sidebar_elements # This will be the content for the left column

    # 2b. Right Column (Marks Table)
    main_elements = []
    main_elements.append(Paragraph("COURSE GRADES", styles['H1_Main']))

    data = [
        ['COURSE TITLE', 'MARKS', 'MAX'],
        ['Python', result.python, 100],
        ['Java', result.java, 100],
        ['PHP', result.php, 100],
        ['C#', result.c_sharp, 100],
        ['SEO', result.seo, 100],
    ]
    
    # Col Widths: Subject (Wide) | Marks (Narrow) | Max Marks (Narrow)
    table_col_widths = [180, 60, 60] 
    marks_table = Table(data, colWidths=table_col_widths)
    
    marks_table.setStyle(TableStyle([
        # Header Row Style
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Data Rows Style
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),     # Subject aligned left
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Marks and Max Marks centered
        
        # Grid/Borders
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F8FF")]), # Alternating rows
    ]))
    main_elements.append(marks_table)
    main_elements_cell = main_elements # This will be the content for the right column

    # Combine into a single table (simulates two columns)
    # Col Widths: Left (200) | Separator (20) | Right (Auto)
    main_layout_data = [[sidebar_elements_cell, VerticalLine(500), main_elements_cell]]
    main_layout_table = Table(main_layout_data, colWidths=[200, 20, doc_width - 220])
    
    # Table styles for the two-column layout
    main_layout_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 20),
        ('LEFTPADDING', (2, 0), (2, 0), 0),
    ]))
    
    elements.append(main_layout_table)
    elements.append(Spacer(1, 40))

    # --- 4. Build the PDF ---
    pdf.build(elements)
    return response