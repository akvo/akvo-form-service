import React, { useEffect, useState, useMemo } from "react";
import { Webform } from "akvo-react-form";
import { api } from "../../lib";
import { useParams } from "react-router-dom";
import { Spin, notification } from "antd";

const Form = () => {
  const { formId } = useParams();
  const [formDef, setFormDef] = useState({});

  useEffect(() => {
    if (!Object.keys(formDef).length) {
      api.get(`form/${formId}`).then((res) => {
        setFormDef(res.data);
      });
    }
  }, [formId, formDef]);

  const questions = useMemo(() => {
    if (!Object.keys(formDef).length) {
      return [];
    }
    return formDef.question_group.flatMap((qg) => qg.question);
  }, [formDef]);

  const onChange = ({ progress }) => {
    console.info(progress);
  };

  const onFinish = (values, refreshForm) => {
    let payload = { data: { ...values.datapoint, submitter: "Akvo" } };
    const answers = Object.keys(values)
      .map((key) => {
        if (key === "datapoint") {
          return false;
        }
        // remap answer by question type
        const qid = parseInt(key);
        const question = questions.find((q) => q.id === qid);
        let value = values[key];
        if (question.type === "option") {
          value = [value];
        }
        return {
          question: qid,
          value: value,
        };
      })
      .filter((x) => x);
    payload = { ...payload, answer: answers };
    api
      .post(`data/${formId}`, payload)
      .then(() => {
        refreshForm();
        notification.success({
          message: "Success",
          description: "Submission submitted successfully.",
        });
      })
      .catch((e) => {
        console.error(e);
        notification.error({
          message: "Error",
          description: "Something went wrong.",
        });
      });
  };

  return (
    <div>
      {Object.keys(formDef).length > 0 ? (
        <Webform forms={formDef} onChange={onChange} onFinish={onFinish} />
      ) : (
        <div className="loading-container">
          <Spin />
        </div>
      )}
    </div>
  );
};

export default Form;
