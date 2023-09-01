import React, { useEffect, useState } from "react";
import "akvo-react-form/dist/index.css"; /* REQUIRED */
import { Webform } from "akvo-react-form";
import { api } from "../../lib";
import { useParams } from "react-router-dom";

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

  const onChange = ({ progress }) => {
    console.info(progress);
  };

  const onFinish = (values) => {
    let payload = { data: { ...values.datapoint, submitter: "Akvo" } };
    const answers = Object.keys(values)
      .map((key) => {
        if (key === "datapoint") {
          return false;
        }
        const value = values[key];
        return {
          question: parseInt(key),
          value: value,
        };
      })
      .filter((x) => x);
    payload = { ...payload, answer: answers };
    console.info(payload);
  };

  return (
    <div>
      {Object.keys(formDef).length > 0 ? (
        <Webform forms={formDef} onChange={onChange} onFinish={onFinish} />
      ) : (
        <h1>Form</h1>
      )}
    </div>
  );
};

export default Form;
