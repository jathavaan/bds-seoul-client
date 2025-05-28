import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#2E2E2E",
      contrastText: "#fff",
    },
    secondary: {
      main: "#4F8FCB",
      light: "#6AAEEF",
      dark: "#3A6DA3",
      contrastText: "#fff",
    },
  },
  shape: {
    borderRadius: 6.4, // 0.4rem
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: "0.4rem",
          textTransform: "none",
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        variant: "filled",
      },
    },
    MuiFilledInput: {
      styleOverrides: {
        root: () => ({
          borderRadius: "0.4rem",
        }),
        underline: {
          "&:before, &:after": {
            display: "none",
          },
        },
        input: {
          paddingTop: "12px",
          paddingBottom: "12px",
          "&::placeholder": {
            opacity: 1,
            color: "rgba(255,255,255,0.6)",
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: () => ({
          borderRadius: "0.4rem",
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "transparent",
          },
        }),
      },
    },
  },
});
