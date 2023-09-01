import React from "react";
import { Row, Col, Table, Button, Divider } from "antd";
import { Link } from "react-router-dom";
import { FormOutlined, ProfileOutlined } from "@ant-design/icons";
import { GlobalStore } from "../../store";

const Forms = () => {
  const { loading, forms } = GlobalStore.useState((s) => s);

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
      title: "Actions",
      width: 300,
      render: (form) => {
        return (
          <Row>
            <Col span={16}>
              <Link to={`/form/${form.id}`}>
                <Button icon={<ProfileOutlined />} type="primary" size="small">
                  New Submission
                </Button>
              </Link>
            </Col>
            <Col span={8}>
              <Link to={`/forms/edit/${form.id}`}>
                <Button icon={<FormOutlined />} type="primary" size="small">
                  Editor
                </Button>
              </Link>
            </Col>
          </Row>
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
