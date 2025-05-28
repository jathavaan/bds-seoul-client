import { Button, FormControl, TextField } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { useTriggerScrapeForm } from "../hooks";

export const TriggerScrapeForm = () => {
  const { formValue, isButtonDisabled, handleScrapeFormUpdate, onButtonClick } =
    useTriggerScrapeForm();
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
        type="number"
        value={formValue}
        sx={(theme) => ({
          marginRight: theme.spacing(2),
        })}
        onChange={(e) => handleScrapeFormUpdate(e.target.value)}
      />
      <Button
        variant="contained"
        endIcon={<SearchIcon />}
        disabled={isButtonDisabled}
        onClick={() => onButtonClick()}
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
