import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import WebformEditor from "akvo-react-form-editor";
import "akvo-react-form-editor/dist/index.css"; /* REQUIRED */
import { api } from "../../lib";
import { GlobalStore } from "../../store";
import { Spin, notification } from "antd";

const Editor = () => {
  const { formId } = useParams();
  const history = useNavigate();
  const [formDef, setFormDef] = useState({});
  const { loading, settingCascadeURL } = GlobalStore.useState((s) => s);

  useEffect(() => {
    if (!Object.keys(formDef).length) {
      api.get(`form/${formId}`).then((res) => {
        setFormDef(res.data);
      });
    }
  }, [formId, formDef]);

  const onSave = (data) => {
    api
      .put(`form`, data)
      .then(() => {
        notification.success({
          message: "Success",
          description: "Form saved successfully.",
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
      {loading ? (
        <div className="loading-container">
          <Spin />
        </div>
      ) : (
        <WebformEditor
          initialValue={formDef}
          onSave={onSave}
          settingCascadeURL={settingCascadeURL}
        />
      )}
    </div>
  );
};

export default Editor;
