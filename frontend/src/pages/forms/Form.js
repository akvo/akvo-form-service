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

  const onChange = ({ current, values, progress }) => {
    console.log(progress);
  };

  const onFinish = (values, refreshForm) => {
    let payload = { data: { ...values.datapoint, submitter: 'Akvo'}}
    const answers = Object.keys(values).map(key => {
      if (key === "datapoint") {
        return false;
      }
      const value = values[key]
      return {
        question: parseInt(key),
        value: value
      }
    }).filter(x => x)
    payload = {...payload, answer: answers}
    console.log(payload);
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
