import { Stack } from "@mui/material";
import { SideBar } from "./components";

function App() {
  return (
    <Stack direction="row" sx={{ minHeight: "100vh" }}>
      <SideBar />
    </Stack>
  );
}

export default App;
