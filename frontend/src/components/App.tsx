import * as React from "react";
import { hot } from "react-hot-loader";
import "./../assets/scss/App.scss";
import { Container } from "@mui/material";
import Selector from "../features/selector/Selector";

function App() {
  return (
    <Container fixed>
      <Selector />
    </Container>
  );
}

declare let module: Record<string, unknown>;

export default hot(module)(App);
