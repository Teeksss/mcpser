import React from "react";
import { Select } from "antd";
import api from "../api";

export default function TenantSwitcher({ tenant, setTenant, tenants }) {
  return (
    <Select
      value={tenant}
      style={{ width: 200 }}
      onChange={setTenant}
      options={tenants.map((t) => ({ value: t.id, label: t.name }))}
      placeholder="Tenant seçin"
    />
  );
}