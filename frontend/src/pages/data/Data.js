import React, { useState, useEffect, useMemo, useCallback } from "react";
import { api } from "../../lib";
import { GlobalStore } from "../../store";
import { Select, Divider, Table, Spin } from "antd";
import { orderBy, groupBy } from "lodash";

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
  const [expandLoading, setExpandLoading] = useState(false);
  const [formDef, setFormDef] = useState({});
  const [answers, setAnswers] = useState([]);
  const current = page.current;

  const formsDropdown = useMemo(() => {
    return forms.map((f) => ({
      label: f.name,
      value: f.id,
    }));
  }, [forms]);

  const fetchFormDefinition = (formId) => {
    api.get(`form/${formId}`).then((res) => {
      setFormDef(res.data);
    });
  };

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
    fetchFormDefinition(value);
    setSelectedForm(value);
  };

  const handleTableChange = (pagination) => {
    const { current } = pagination;
    setPage({
      ...page,
      current: current,
    });
  };

  const getAnswers = (dataId) => {
    setExpandLoading(true);
    api
      .get(`answers/${dataId}`)
      .then((res) => {
        const questions = formDef.question_group.flatMap((qg) =>
          qg.question.map((q) => ({
            ...q,
            qgId: qg.id,
            qgName: qg.name,
            qgOrder: qg.order,
          }))
        );
        const transformAnswers = res.data.map((d) => {
          const q = questions.find((q) => q.id === d.question);
          return {
            qgId: q.qgId,
            qgName: q.qgName,
            qgOrder: q.qgOrder,
            qId: q.id,
            qName: q.name,
            qOrder: q.order,
            qType: q.type,
            answer: d.value,
          };
        });
        setAnswers(orderBy(transformAnswers, ["qgOrder", "qOrder"]));
      })
      .finally(() => {
        setExpandLoading(false);
      });
  };

  const answerDetail = useMemo(() => {
    const groups = groupBy(answers, "qgName");
    return Object.keys(groups).map((key) => {
      const listSource = groups[key];
      return (
        <>
          <h4>{key}</h4>
          <Table
            size="small"
            columns={[
              { title: "Question", dataIndex: "qName", width: "50%" },
              { title: "Answer", dataIndex: "answer" },
            ]}
            dataSource={listSource}
            pagination={false}
          />
        </>
      );
    });
  }, [answers]);

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
        expandable={{
          expandIconColumnIndex: columns.length,
          expandedRowRender: () => (
            <>
              {expandLoading ? (
                <div className="loading-wrapper">
                  <Spin />
                </div>
              ) : (
                answerDetail
              )}
            </>
          ),
        }}
        onExpand={(expanded, record) => {
          if (expanded) {
            getAnswers(record?.id);
          }
        }}
      />
    </div>
  );
};

export default Data;
