import React, { useState, useEffect } from "react";
import { Layout, Menu, message } from "antd";
import AdminDashboard from "./components/AdminDashboard";
import TenantSwitcher from "./components/TenantSwitcher";
import TenantAdminPanel from "./components/TenantAdminPanel";
import AuditLogView from "./components/AuditLogView";
import api from "./api";

const { Sider, Content } = Layout;

export default function App() {
  const [tenant, setTenant] = useState(localStorage.getItem("tenant_id") || "");
  const [tenants, setTenants] = useState([]);
  const [selectedMenu, setSelectedMenu] = useState("admin");

  useEffect(() => {
    api
      .get("/api/v1/tenants/")
      .then((res) => setTenants(res.data))
      .catch(() => message.error("Tenantlar yüklenemedi"));
  }, []);

  useEffect(() => {
    if (tenant) {
      localStorage.setItem("tenant_id", tenant);
    }
  }, [tenant]);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedMenu]}
          onClick={(e) => setSelectedMenu(e.key)}
        >
          <Menu.Item key="admin">Admin Dashboard</Menu.Item>
          <Menu.Item key="tenant">Tenant Yönetimi</Menu.Item>
          <Menu.Item key="audit">Audit Logları</Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Content style={{ margin: 24 }}>
          <TenantSwitcher tenant={tenant} setTenant={setTenant} tenants={tenants} />
          {selectedMenu === "admin" && <AdminDashboard />}
          {selectedMenu === "tenant" && <TenantAdminPanel />}
          {selectedMenu === "audit" && <AuditLogView />}
        </Content>
      </Layout>
    </Layout>
  );
}