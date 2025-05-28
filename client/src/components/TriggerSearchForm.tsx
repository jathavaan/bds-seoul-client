import { Button, FormControl, TextField } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

export const TriggerSearchForm = () => {
  return (
    <FormControl
      sx={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        width: "100%",
        minWidth: "400px",
      }}
    >
      <TextField
        variant="filled"
        fullWidth
        placeholder="Steam Game ID (e.g. 703)..."
        sx={(theme) => ({
          marginRight: theme.spacing(2),
        })}
      />
      <Button
        variant="contained"
        endIcon={<SearchIcon />}
        sx={(theme) => ({
          backgroundColor: theme.palette.secondary.main,
          "&:hover": {
            backgroundColor: theme.palette.secondary.dark,
          },
        })}
      >
        Search
      </Button>
    </FormControl>
  );
};
