import React, { useEffect, useState } from "react";
import { Card, List } from "antd";
import api from "../api";

export default function AuditLogView() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    api.get("/api/v1/audit/").then((res) => setLogs(res.data));
  }, []);
  return (
    <Card title="Audit Logları">
      <List
        size="small"
        bordered
        dataSource={logs}
        renderItem={(item) => <List.Item>{item}</List.Item>}
      />
    </Card>
  );
}