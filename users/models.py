from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model

User = get_user_model()

# ==========================================
# CHOICE ENUMS (Inheriting from TextChoices)
# ==========================================

class AssetCategory(models.TextChoices):
    IT = 'IT', 'IT'
    OT = 'OT', 'OT'
    INFRASTRUCTURE = 'INFRASTRUCTURE', 'Infrastructure'

class OperationalStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'
    RETIRED = 'RETIRED', 'Retired'
    
class Classification(models.TextChoices):
    PUBLIC = 'PUBLIC', 'Public'
    INTERNAL = 'INTERNAL', 'Internal'
    CONFIDENTIAL = 'CONFIDENTIAL', 'Confidential'
    RESTRICTED = 'RESTRICTED', 'Restricted'
    
class AssetCriticality(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'

class CiaRating(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'

class RiskTreatment(models.TextChoices):
    MODIFY = 'Modify', 'Modify'
    RETAIN = 'Retain', 'Retain'
    AVOID = 'Avoid', 'Avoid'
    SHARE = 'Share', 'Share'
    
class RiskStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    MITIGATED = 'MITIGATED', 'Mitigated'
    CLOSED = 'CLOSED', 'Closed'

class ProgressStatus(models.TextChoices):
    NOT_STARTED = 'NOT STARTED', 'Not Started'
    IN_PROGRESS = 'IN PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'

class ActionType(models.TextChoices):
    CREATE = 'CREATE', 'CREATE'
    UPDATE = 'UPDATE', 'UPDATE'
    DELETE = 'DELETE', 'DELETE'
    LOGIN = 'LOGIN', 'LOGIN'

class RiskCategory(models.TextChoices):
    DEFAULT_DATA = 'DEFAULT DATA', 'Default Data'
    CYBERSECURITY = 'CYBERSECURITY', 'Cybersecurity'
    OPERATIONAL = 'OPERATIONAL', 'Operational'
    SAFETY = 'SAFETY', 'Safety'
    COMPLIANCE = 'COMPLIANCE', 'Compliance'
    PHYSICAL_SECURITY = 'PHYSICAL_SECURITY', 'Physical Security'
    ENVIRONMENTAL = 'ENVIRONMENT', 'Environment'
    
# ==========================================
# APPLICATION DATABASE MODELS
# ==========================================

class Asset(models.Model):
    asset = models.BigAutoField(primary_key=True)
    asset_name = models.CharField(max_length=150)
    asset_description = models.TextField()
    asset_category = models.CharField(max_length=20, choices=AssetCategory.choices)
    operational_status = models.CharField(
        max_length=20, 
        choices=OperationalStatus.choices, 
        default=OperationalStatus.ACTIVE
    )
    classification = models.CharField(max_length=20, choices=Classification.choices)
    
    asset_criticality = models.CharField(max_length= 20, choices=AssetCriticality.choices)
    
    cia_confidentiality = models.CharField(max_length=20, choices=CiaRating.choices)
    cia_integrity = models.CharField(max_length=20, choices=CiaRating.choices)
    cia_availability = models.CharField(max_length=20, choices=CiaRating.choices)
    
    asset_owner = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset_name


class Risk(models.Model):
    risk_id = models.BigAutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='risks')
    risk_description = models.TextField()
    likelihood = models.IntegerField()
    impact = models.IntegerField()
    
    risk_category = models.CharField( max_length=20, choices=RiskCategory.choices, 
                                     default=RiskCategory.DEFAULT_DATA)

    risk_rating = models.GeneratedField(
        expression=F("likelihood") * F("impact"),
        output_field=models.IntegerField(),
        db_persist=True,
    )
    
    risk_treatment = models.CharField(max_length=10, choices=RiskTreatment.choices)
    risk_owner = models.CharField(max_length=100,default="")
    review_date = models.DateField()
    risk_status = models.CharField(max_length=20, choices=RiskStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    annex_control = models.TextField(default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(likelihood__gte=1) & Q(likelihood__lte=5), 
                name="likelihood_between_1_and_5"
            ),
            models.CheckConstraint(
                condition=Q(impact__gte=1) & Q(impact__lte=5),
                name="impact_between_1_and_5"
            )
        ]
        indexes = [
            models.Index(fields=["asset", "risk_status"], name="idx_risks_asset_status")
        ]

    def __str__(self):
        return f"Risk {self.risk_id} (Rating: {self.risk_rating})"

class RiskControl(models.Model):
    risk_control_id = models.BigAutoField(primary_key=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='controls')
    control_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.control_code} for Risk {self.risk_id}"


class Mitigation(models.Model):
    mitigation_id = models.BigAutoField(primary_key=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='mitigations')
    action_description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mitigations')
    target_date = models.DateField()
    progress_status = models.CharField(
        max_length=20, 
        choices=ProgressStatus.choices, 
        default=ProgressStatus.NOT_STARTED
    )
    comments = models.TextField()
    effectiveness_review_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["risk", "target_date", "progress_status"], 
                name="idx_mitigations_target_status"
            )
        ]


class AuditLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action_type = models.CharField(max_length=10, choices=ActionType.choices)
    entity_name = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=50)
    action_date = models.DateTimeField(auto_now_add=True)
    action_details = models.TextField()

    class Meta:
        indexes = [
            models.Index(
                fields=["user", "action_type", "action_date"], 
                name="idx_audit_logs_user_type_date"
            )
        ]