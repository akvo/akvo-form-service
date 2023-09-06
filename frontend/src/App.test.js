import { render, waitFor } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import App from "./App";

jest.mock("axios");
jest.mock("./store", () => ({
  GlobalStore: {
    update: jest.fn(),
  },
}));

test("it renders correctly", async () => {
  // mock router path to be /
  window.history.pushState({}, "Home page", "/");
  const { getByTestId } = render(
    <Router>
      <App />
    </Router>
  );
  waitFor(() => {
    expect(getByTestId("landing-page")).toBeInTheDocument();
  });
});
