import React, { useEffect } from "react";
import "./App.scss";
import { Routes, Route } from "react-router-dom";
import { Home } from "./pages/home";
import { Forms, Form, Editor } from "./pages/forms";
import { Data } from "./pages/data";
import { PageLayout } from "./layouts";
import { api } from "./lib";
import { GlobalStore } from "./store";

const App = () => {
  useEffect(() => {
    GlobalStore.update((s) => {
      s.loading = true;
    });
    Promise.all([api.get("forms"), api.get("node")])
      .then(([resForms, resNode]) => {
        GlobalStore.update((s) => {
          s.forms = resForms.data;
          s.settingCascadeURL = resNode.data;
        });
      })
      .finally(() => {
        GlobalStore.update((s) => {
          s.loading = false;
        });
      });
  }, []);

  return (
    <PageLayout>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/form/:formId" element={<Form />} />
        <Route exact path="/forms" element={<Forms />} />
        <Route exact path="/forms/edit/:formId" element={<Editor />} />
        <Route exact path="/data" element={<Data />} />
      </Routes>
    </PageLayout>
  );
};

export default App;
