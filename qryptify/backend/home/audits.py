from .models import AuditLog

def audit_logs(actor, action, message, target_user=None,created_at=None):
    AuditLog.objects.create(
        actor=actor,
        action=action,
        message=message,
        target_user=target_user,
        created_at=created_at
    )

    