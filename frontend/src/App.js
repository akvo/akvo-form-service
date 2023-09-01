import "./App.scss";
import { Routes, Route } from "react-router-dom";
import { Home } from "./pages/home";
import { Forms, Form } from "./pages/forms";
import { PageLayout } from "./layouts";

const App = () => {
  return (
    <PageLayout>
      <Routes>
        <Route exact path="/form/:formId" element={<Form />} />
        <Route exact path="/forms" element={<Forms />} />
        <Route exact path="/" element={<Home />} />
      </Routes>
    </PageLayout>
  );
};

export default App;
