import { Stack } from "@mui/material";
import { HorizontalBarchart, SideBar } from "./components";

function App() {
  return (
    <Stack direction="row" sx={{ minHeight: "100vh", width: "100vw" }}>
      <SideBar />
      <HorizontalBarchart />
    </Stack>
  );
}

export default App;
