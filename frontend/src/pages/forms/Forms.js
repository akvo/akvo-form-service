import React, { useEffect } from "react";
import { Row, Col, Table, Button, Divider } from "antd";
import { Link } from "react-router-dom";
import { FormOutlined, ProfileOutlined, PlusOutlined } from "@ant-design/icons";
import { GlobalStore } from "../../store";
import { api } from "../../lib";

const Forms = () => {
  const { loading, forms } = GlobalStore.useState((s) => s);

  useEffect(() => {
    GlobalStore.update((s) => {
      s.loading = true;
    });
    api
      .get("forms")
      .then((res) => {
        GlobalStore.update((s) => {
          s.forms = res.data;
        });
      })
      .finally(() => {
        GlobalStore.update((s) => {
          s.loading = false;
        });
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
      title: "Actions",
      width: 300,
      render: (form) => {
        return (
          <Row>
            <Col span={16}>
              <Link to={`/form/${form.id}`}>
                <Button icon={<ProfileOutlined />} size="small" type="ghost">
                  New Submission
                </Button>
              </Link>
            </Col>
            <Col span={8}>
              <Link to={`/forms/edit/${form.id}`}>
                <Button icon={<FormOutlined />} size="small" type="ghost">
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
      <Row align="middle" justify="center" gutter={[12, 12]}>
        <Col span={20}>
          <h1>Form</h1>
        </Col>
        <Col span={4} align="end">
          <Link to="/new-form">
            <Button type="primary" icon={<PlusOutlined />}>
              Add New
            </Button>
          </Link>
        </Col>
      </Row>
      <Divider />
      <Table dataSource={forms} columns={columns} loading={loading} />
    </div>
  );
};

export default Forms;
