import React from "react";
import { Card, Table, Button, message } from "antd";
import { useEffect, useState } from "react";
import api from "../api";

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get("/api/v1/users/").then((res) => setUsers(res.data));
  }, []);

  const handleRoleChange = (userId, role) => {
    api
      .post(`/api/v1/users/${userId}/role`, null, { params: { role } })
      .then(() => {
        message.success("Rol güncellendi");
        setUsers(users.map(u => u.id === userId ? {...u, role} : u));
      });
  };

  const columns = [
    { title: "Kullanıcı Adı", dataIndex: "username", key: "username" },
    { title: "E-posta", dataIndex: "email", key: "email" },
    { title: "Rol", dataIndex: "role", key: "role" },
    {
      title: "İşlem",
      render: (_, record) => (
        <>
          <Button onClick={() => handleRoleChange(record.id, "admin")}>Admin</Button>
          <Button onClick={() => handleRoleChange(record.id, "user")}>User</Button>
        </>
      ),
    },
  ];

  return (
    <Card title="Admin Dashboard">
      <Table dataSource={users} columns={columns} rowKey="id" />
    </Card>
  );
}