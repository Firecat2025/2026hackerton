def test_repro_lv5_admin_vault_rbac(client):
    # Step 1: Confirm unauthenticated /api/admin/export request returns 403 Forbidden
    resp = client.get("/api/admin/export")
    assert resp.status_code == 403 and "Unauthorized admin vault" in resp.text
