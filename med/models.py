from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Patient(models.Model):
    center = models.CharField(max_length=100, null=True, blank=True)

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
    created_by = models.ForeignKey('UserAccount', on_delete=models.CASCADE, null=True, blank=True)

    assigned_to = models.ForeignKey(
        'UserAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_patients'
    )
    def save(self, *args, **kwargs):
        if not self.patient_id:
            now = datetime.now()
            self.patient_id = f"P{now.strftime('%Y%m%d%H%M%S')}"
        super(Patient, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'patients'


from django.db import models
from django.utils import timezone
USERTYPES = (
    ('RADS', 'RADS'),
    ('IMAGING', 'IMAGING'),
    ('SUPERADMIN', 'Super Admin'),
    ('ADMIN', 'Admin'),
)

class UserAccount(models.Model):
    created_at = models.DateTimeField(default=timezone.now) 
    name = models.CharField(max_length=100)
    userid = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=10, choices=USERTYPES)
    is_active = models.BooleanField(default=True)
    
    parent_admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_users')



    def __str__(self):
        return f"{self.name} ({self.userid})"
        

class SuperAdminCreatedUsers(models.Model):
    name = models.CharField(max_length=200)
    userid = models.CharField(max_length=200)
    usertype = models.CharField(max_length=50)
    contact = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
