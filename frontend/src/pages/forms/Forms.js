import React, { useEffect, useState } from "react";
import { api } from "../../lib";
import { Table, Button, Divider } from "antd";
import { Link } from "react-router-dom";

const Forms = () => {
  const [loading, setLoading] = useState(false);
  const [forms, setForms] = useState([]);

  useEffect(() => {
    setLoading(true);
    api
      .get("forms")
      .then((res) => {
        setForms(res.data);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const columns = [
    {
      title: "Form",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Version",
      dataIndex: "version",
      key: "version",
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Action",
      render: (form) => {
        return (
          <Link to={`/form/${form.id}`}>
            <Button type="primary" size="small">
              Go to Webform
            </Button>
          </Link>
        );
      },
    },
  ];

  return (
    <div>
      <h1>Form</h1>
      <Divider />
      <Table dataSource={forms} columns={columns} loading={loading} />
    </div>
  );
};

export default Forms;
