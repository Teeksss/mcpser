from fastapi import Request

def get_tenant_id(request: Request):
    tenant_id = request.headers.get("X-Tenant")
    if not tenant_id:
        raise Exception("Tenant header eksik.")
    return int(tenant_id)