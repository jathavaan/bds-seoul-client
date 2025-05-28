import { Container, Stack } from "@mui/material";
import { SideBar } from "./components";

function App() {
  return (
    <Container maxWidth="lg">
      <Stack direction="row">
        <SideBar />
      </Stack>
    </Container>
  );
}

export default App;
