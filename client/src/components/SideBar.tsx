import { Divider, Stack } from "@mui/material";
import { TriggerScrapeForm } from "./TriggerScrapeForm.tsx";
import { GameList } from "./GameList.tsx";

export const SideBar = () => {
  return (
    <Stack
      direction="column"
      spacing={2}
      divider={<Divider />}
      sx={(theme) => ({
        backgroundColor: theme.palette.primary.main,
        padding: theme.spacing(2),
      })}
    >
      <TriggerScrapeForm />
      <GameList />
    </Stack>
  );
};
