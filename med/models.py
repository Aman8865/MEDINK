from django.db import models
from datetime import datetime

class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    history = models.TextField()
    scan_type = models.CharField(max_length=10)
    body_part = models.CharField(max_length=100, default='Head')
    ref_by = models.CharField(max_length=100, default='Doctor Unknown')
    # Changed from ImageField to TextField
    scan_image = models.TextField()
    entry_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='UNREAD')
    report = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            now = datetime.now()
            self.patient_id = f"P{now.strftime('%Y%m%d%H%M%S')}"
        super(Patient, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'patients'