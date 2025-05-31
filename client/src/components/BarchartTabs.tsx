import { CircularProgress, Tab, Tabs, Typography } from "@mui/material";
import { HorizontalBarchart } from "./HorizontalBarchart.tsx";
import { useBarchart } from "../hooks";
import { VerticalBarchart } from "./VerticalBarchart.tsx";

export const BarchartTabs = () => {
  const { isLoading, gameId, activeTabId, onTabClick } = useBarchart();
  return (
    <section
      style={{
        width: "100%",
        minHeight: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {!gameId ? (
        <Typography variant="h3" sx={{ fontSize: "1rem", textAlign: "center" }}>
          No game selected, please select a game in the tab to the left.
        </Typography>
      ) : !isLoading ? (
        <>
          <Tabs
            value={activeTabId}
            indicatorColor="primary"
            onChange={(_e, newValue) => onTabClick(newValue)}
            sx={(theme) => ({
              width: "100%",
              textTransform: "none",
              "& .Mui.selected": {
                color: theme.palette.primary.contrastText,
              },
              "& .MuiTabs-indicator": {
                backgroundColor: theme.palette.primary.contrastText,
              },
            })}
          >
            <Tab
              label="Recommendations (Normalized)"
              value={1}
              sx={(theme) => ({
                textTransform: "none",
                padding: theme.spacing(3),
                color: theme.palette.primary.contrastText,
                "&.Mui-selected": {
                  color: theme.palette.primary.contrastText,
                },
                "&:hover": {
                  backgroundColor: theme.palette.primary.light,
                },
              })}
            />
            <Tab
              label="Recommendations (Sum)"
              value={2}
              sx={(theme) => ({
                textTransform: "none",
                padding: theme.spacing(3),
                color: theme.palette.primary.contrastText,
                "&.Mui-selected": {
                  color: theme.palette.primary.contrastText,
                },
                "&:hover": {
                  backgroundColor: theme.palette.primary.light,
                },
              })}
            />
          </Tabs>

          <section
            style={{
              height: "100%",
              width: "100%",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {activeTabId === 1 && <HorizontalBarchart />}
            {activeTabId === 2 && <VerticalBarchart />}
          </section>
        </>
      ) : (
        <CircularProgress
          sx={(theme) => ({ color: theme.palette.primary.contrastText })}
        />
      )}
    </section>
  );
};
