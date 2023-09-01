import "./App.scss";
import { Routes, Route } from "react-router-dom";
import { Home } from "./pages/home";
import { Forms, Form } from "./pages/forms";
import { Data } from "./pages/data";
import { PageLayout } from "./layouts";

const App = () => {
  return (
    <PageLayout>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/form/:formId" element={<Form />} />
        <Route exact path="/forms" element={<Forms />} />
        <Route exact path="/data" element={<Data />} />
      </Routes>
    </PageLayout>
  );
};

export default App;
