from django.shortcuts import render

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



def user_detail(request):
    return render(request, 'user_detail.html')

def imagingA(request):
    return render(request, 'imagingA.html')

def RADS(request):
    return render(request, 'RADS.html')

def invoice(request):
    return render(request, 'invoice.html')
def payment(request):
    return render(request, 'payment.html')






from django.shortcuts import render
from django.http import JsonResponse
from .models import Patient
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import base64
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