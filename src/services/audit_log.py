import datetime

class AuditLogger:
    def __init__(self, path="./logs/audit.log"):
        self.path = path

    def log(self, user, action, detail=None):
        with open(self.path, "a", encoding="utf-8") as f:
            line = f"{datetime.datetime.utcnow().isoformat()} | user={user} | action={action} | detail={detail or ''}\n"
            f.write(line)

audit_logger = AuditLogger()