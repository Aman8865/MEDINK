from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Patient
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import base64
from docx import Document
from docx.shared import Inches
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create your views here.


def login(request):
    return render(request, 'login.html')

# def index(request):
#     return render(request, 'index.html')
    

def profile(request):
    return render(request, 'profile.html')

def signup(request):
    return render(request,'signup.html')

def popupform(request):
    return render(request,'popupform.html')
# def report(request, id):
#     return render(request, 'report.html', {'id': id})



from django.shortcuts import render, get_object_or_404
from .models import UserAccount

from django.shortcuts import render, get_object_or_404, redirect
from .models import UserAccount

def user_detail(request, id):
    user = get_object_or_404(UserAccount, id=id)

    if request.method == "POST":
        # Login Details
        user.is_active = request.POST.get('status') == 'ACTIVE'
        # user.modality = request.POST.get('modality', user.modality)

        # Personal details
        user.name = request.POST.get('personName', user.name)
        # user.contact = request.POST.get('mobileNo', user.contact)
        # user.email = request.POST.get('email', user.email)

        # Password update
        new_password = request.POST.get('password')
        if new_password:
            user.password = new_password  # Optional: hash it in production

        user.save()
        return redirect('user_detail', id=id)  # Refresh page after saving

    return render(request, 'user_detail.html', {'user': user})


# views.py
from django.shortcuts import redirect

def update_user(request, id):
    user = get_object_or_404(UserAccount, id=id)
    if request.method == 'POST':
        user.name = request.POST.get('accountName')
        # user.contact = request.POST.get('mobileNo')
        user.usertype = request.POST.get('userType')
        user.is_active = request.POST.get('status') == 'ACTIVE'
        # add other fields
        user.save()
        return redirect('user_detail', id=user.id)
    return render(request, 'user_detail.html', {'user': user})


def imagingA(request):
    patients = Patient.objects.all().order_by('-entry_time')
    return render(request, 'imagingA.html', {'patients': patients})

def RADS(request):
    patients = Patient.objects.all().order_by('-entry_time')
    return render(request, 'RADS.html', {'patients': patients})

def invoice(request):
    return render(request, 'invoice.html')
def payment(request):
    return render(request, 'payment.html')


@csrf_exempt
def add_patient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # For debugging
            
            # Clean up base64 image data if needed
            scan_image = data.get('scan', '')  # Use get() with default value
            if ',' in scan_image:
                scan_image = scan_image.split(',')[1]
            
            patient = Patient.objects.create(
                name=data.get('name'),
                age=data.get('age'),
                gender=data.get('gender'),
                history=data.get('history'),
                scan_type=data.get('scanType'),  # Changed from scan_type
                body_part=data.get('bodyPart'),  # Changed from body_part
                ref_by=data.get('refBy'),        # Changed from ref_by
                scan_image=scan_image
            )
            return JsonResponse({
                'status': 'success',
                'patient_id': patient.patient_id
            })
        except KeyError as e:
            print("KeyError:", e)  # Add debug print
            return JsonResponse({
                'status': 'error',
                'message': f'Missing field: {str(e)}'
            })
        except Exception as e:
            print("Exception:", e)  # Add debug print
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

def index(request):
    patients = Patient.objects.all().order_by('-entry_time')
    return render(request, 'index.html', {'patients': patients})
@csrf_exempt
def update_report(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            patient = Patient.objects.get(id=id)
            patient.report = data['report']
            patient.status = data['status']
            patient.save()
            return JsonResponse({'status': 'success'})
        except Patient.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Patient not found'})

def report(request, id):
    try:
        patient = Patient.objects.get(id=id)
        return render(request, 'report.html', {'patient': patient})
    except Patient.DoesNotExist:
        return render(request, 'report.html', {'error': 'Patient not found'})
    

    
@csrf_exempt
def get_patient(request, id):
    try:
        patient = Patient.objects.get(id=id)
        data = {
            'id': patient.id,
            'patient_id': patient.patient_id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'history': patient.history,
            'scan_type': patient.scan_type,
            'body_part': patient.body_part,
            'ref_by': patient.ref_by,
            'scan_image': patient.scan_image,
            'status': patient.status,
            'report': patient.report
        }
        return JsonResponse(data)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)





@csrf_exempt
def delete_patient(request, id):
    if request.method == 'DELETE':
        try:
            patient = Patient.objects.get(id=id)
            patient.delete()
            return JsonResponse({'status': 'success'})
        except Patient.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Patient not found'})
        
        
@csrf_exempt
def download_report(request, id, format):
    try:
        patient = Patient.objects.get(id=id)
        if patient.status != 'FINAL':
            return JsonResponse({'error': 'Report not finalized'}, status=400)

        if format == 'pdf':
            # Create PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            
            # Add content
            p.setFont("Helvetica", 12)
            p.drawString(100, 750, f"Patient ID: {patient.patient_id}")
            p.drawString(100, 730, f"Name: {patient.name}")
            p.drawString(100, 710, f"Age/Gender: {patient.age}/{patient.gender}")
            p.drawString(100, 690, f"Scan Type: {patient.scan_type}")
            p.drawString(100, 670, f"Body Part: {patient.body_part}")
            p.drawString(100, 650, f"Referred By: {patient.ref_by}")
            p.drawString(100, 630, "Report:")
            p.drawString(120, 610, patient.report or "No report available")
            
            p.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="patient_report_{patient.patient_id}.pdf"'
            return response

        elif format == 'docx':
            # Create Word document
            doc = Document()
            doc.add_heading('Patient Report', 0)
            
            # Add content
            doc.add_paragraph(f'Patient ID: {patient.patient_id}')
            doc.add_paragraph(f'Name: {patient.name}')
            doc.add_paragraph(f'Age/Gender: {patient.age}/{patient.gender}')
            doc.add_paragraph(f'Scan Type: {patient.scan_type}')
            doc.add_paragraph(f'Body Part: {patient.body_part}')
            doc.add_paragraph(f'Referred By: {patient.ref_by}')
            doc.add_heading('Report:', level=1)
            doc.add_paragraph(patient.report or "No report available")
            
            # Save document
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="patient_report_{patient.patient_id}.docx"'
            return response

        return JsonResponse({'error': 'Invalid format'}, status=400)
        
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)
    





from django.shortcuts import render, redirect
from .models import UserAccount
from .forms import SignupForm, LoginForm

def signup_view(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('signup')
    users_list = UserAccount.objects.all()
    return render(request, 'signup.html', {'form': form, 'users': users_list})

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None
    if form.is_valid():
        userid = form.cleaned_data['userid']
        password = form.cleaned_data['password']
        try:
            user = UserAccount.objects.get(userid=userid, password=password)
            if user.usertype == 'RADS':
                return redirect('RADS')
            else:
                return redirect('imagingA')
        except UserAccount.DoesNotExist:
            error = "Invalid userid or password"
    return render(request, 'login.html', {'form': form, 'error': error})

# def rads_page(request):
#     return render(request, 'RADS.html')

# def imaging_page(request):
#     return render(request, 'imagingA.html')



    