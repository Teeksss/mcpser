import React, { useEffect, useState } from "react";
import { Card, Table, Button, Form, Input, message } from "antd";
import api from "../api";

export default function TenantAdminPanel() {
  const [tenants, setTenants] = useState([]);
  const [form] = Form.useForm();

  useEffect(() => {
    api.get("/api/v1/tenants/").then((res) => setTenants(res.data));
  }, []);

  const handleCreateTenant = (values) => {
    api
      .post("/api/v1/tenants/", null, { params: values })
      .then((res) => {
        message.success("Tenant oluşturuldu");
        setTenants([...tenants, res.data]);
        form.resetFields();
      });
  };

  return (
    <Card title="Tenant Yönetimi">
      <Form layout="inline" onFinish={handleCreateTenant} form={form}>
        <Form.Item name="name" rules={[{ required: true, message: "Tenant adı zorunlu" }]}>
          <Input placeholder="Tenant adı" />
        </Form.Item>
        <Form.Item name="description">
          <Input placeholder="Açıklama" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Ekle
          </Button>
        </Form.Item>
      </Form>
      <Table
        dataSource={tenants}
        columns={[
          { title: "Tenant Adı", dataIndex: "name" },
          { title: "Açıklama", dataIndex: "description" },
          { title: "ID", dataIndex: "id" },
        ]}
        rowKey="id"
        style={{ marginTop: 24 }}
      />
    </Card>
  );
}