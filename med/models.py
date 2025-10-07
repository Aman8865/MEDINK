from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    history = models.TextField()
    scan_type = models.CharField(max_length=20)
    body_part = models.CharField(max_length=50)
    ref_by = models.CharField(max_length=100)
    scan = models.TextField()  # store base64 image or file path
    entry_time = models.DateTimeField(auto_now_add=True)
    report = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('DRAFT','Draft'),('FINAL','Final')], default='DRAFT')

    def __str__(self):
        return f"{self.patient_id} - {self.name}"
