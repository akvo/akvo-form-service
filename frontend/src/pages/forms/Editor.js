import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import WebformEditor from "akvo-react-form-editor";
import "akvo-react-form-editor/dist/index.css"; /* REQUIRED */
import { api } from "../../lib";

const Editor = () => {
  const { formId } = useParams();
  const history = useNavigate();
  const [formDef, setFormDef] = useState({});

  useEffect(() => {
    if (!Object.keys(formDef).length) {
      api.get(`form/${formId}`).then((res) => {
        setFormDef(res.data);
      });
    }
  }, [formId, formDef]);

  const onSave = (data) => {
    console.info(data);
  };
  return (
    <div>
      <h1>
        <a
          onClick={() => {
            history("/forms");
          }}
        >
          {" "}
          Form
        </a>{" "}
        / Edit / {formId}
      </h1>
      <WebformEditor initialValue={formDef} onSave={onSave} />
    </div>
  );
};

export default Editor;
