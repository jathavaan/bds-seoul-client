import { Stack } from "@mui/material";
import { BarchartTabs, SideBar } from "./components";

function App() {
  return (
    <Stack direction="row" sx={{ minHeight: "100vh", width: "100vw" }}>
      <SideBar />
      <BarchartTabs />
    </Stack>
  );
}

export default App;
