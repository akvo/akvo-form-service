import React, { useState, useEffect, useMemo, useCallback } from "react";
import { api } from "../../lib";
import { GlobalStore } from "../../store";
import { Select, Divider, Table } from "antd";

const Data = () => {
  const forms = GlobalStore.useState((s) => s.forms);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [selectedForm, setSelectedForm] = useState(null);
  const [page, setPage] = useState({
    current: 1,
    total_page: 1,
    total: 0,
  });
  const current = page.current;

  const formsDropdown = useMemo(() => {
    return forms.map((f) => ({
      label: f.name,
      value: f.id,
    }));
  }, [forms]);

  const fetchData = useCallback(() => {
    setLoading(true);
    api
      .get(`data/${selectedForm}?page=${current}`)
      .then((res) => {
        const { current, total_page, data: resData, total } = res.data;
        setData(resData);
        setPage({
          current,
          total_page,
          total,
        });
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedForm, current]);

  useEffect(() => {
    if (selectedForm) {
      fetchData();
    }
  }, [selectedForm, current, fetchData]);

  const handleOnSelectForm = (value) => {
    setSelectedForm(value);
  };

  const handleTableChange = (pagination) => {
    const { current } = pagination;
    setPage({
      ...page,
      current: current,
    });
  };

  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Submitter",
      dataIndex: "submitter",
      key: "submitter",
    },
    {
      title: "Created",
      dataIndex: "created",
      key: "created",
    },
  ];

  return (
    <div>
      <h1>Data</h1>
      <Divider />
      {/* Forms dropdown */}
      <Select
        showSearch
        placeholder="Select a form"
        optionFilterProp="children"
        style={{ width: 300 }}
        onChange={handleOnSelectForm}
        filterOption={(input, option) =>
          (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
        }
        options={formsDropdown}
      />
      <br />
      <br />
      {/* Table */}
      <Table
        rowKey="id"
        dataSource={data}
        columns={columns}
        loading={loading}
        onChange={handleTableChange}
        pagination={{
          current: page.current,
          total: page.total,
        }}
      />
    </div>
  );
};

export default Data;
