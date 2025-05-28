import {
  CircularProgress,
  Collapse,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import ScheduleIcon from "@mui/icons-material/Schedule";
import SkipNextIcon from "@mui/icons-material/SkipNext";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import CrisisAlertIcon from "@mui/icons-material/CrisisAlert";
import type { GameListProps, ProcessStatusProps } from "./component.types.ts";
import { useGameList, useGameListItem } from "../hooks";

export const GameList = () => {
  const { games } = useGameList();
  return (
    <List>
      {Object.keys(games).map((key) => (
        <GameListItem key={key} steamGameId={Number(key)} />
      ))}
    </List>
  );
};

const GameListItem = (props: GameListProps) => {
  const { isExpanded, isLoading, handleClick } = useGameListItem(
    props.steamGameId,
  );
  return (
    <>
      <ListItemButton
        onClick={handleClick}
        sx={(theme) => ({
          "&:hover": { backgroundColor: theme.palette.primary.light },
        })}
      >
        <ListItemText primary={props.steamGameId} />
        <ListItemIcon>
          {isLoading ? (
            <CircularProgress
              size={20}
              sx={(theme) => ({
                color: theme.palette.primary.contrastText,
              })}
            />
          ) : (
            <CheckIcon />
          )}
        </ListItemIcon>
        <ListItemIcon>
          {isExpanded ? <ArrowDropUpIcon /> : <ArrowDropDownIcon />}
        </ListItemIcon>
      </ListItemButton>
      <Collapse in={isExpanded} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ProcessStatusItem statusText="Checking cache" status="completed" />
          <ProcessStatusItem
            statusText="Scraping Steam reviews"
            status="completed"
          />
          <ProcessStatusItem
            statusText="Running MapReduce job"
            status="in_progress"
          />
          <ProcessStatusItem statusText="Caching result" status="queued" />
          <ProcessStatusItem
            statusText="Waiting for response"
            status="queued"
          />
        </List>
      </Collapse>
    </>
  );
};

const ProcessStatusItem = (props: ProcessStatusProps) => {
  return (
    <ListItem
      sx={(theme) => ({
        "&:hover": {
          backgroundColor: theme.palette.primary.light,
        },
      })}
    >
      <ListItemText
        primary={props.statusText}
        sx={(theme) => ({
          pl: theme.spacing(2),
        })}
      />
      <ListItemIcon>
        {(() => {
          switch (props.status) {
            case "queued":
              return (
                <ScheduleIcon
                  sx={(theme) => ({
                    color: theme.palette.primary.contrastText,
                  })}
                />
              );
            case "in_progress":
              return (
                <CircularProgress
                  size={20}
                  sx={(theme) => ({
                    color: theme.palette.primary.contrastText,
                  })}
                />
              );
            case "skipped":
              return <SkipNextIcon sx={{ color: "gray" }} />;
            case "completed":
              return <CheckIcon sx={{ color: "green" }} />;
            case "failed":
              return <ErrorOutlineIcon sx={{ color: "red" }} />;
            default:
              return <CrisisAlertIcon sx={{ color: "red" }} />;
          }
        })()}
      </ListItemIcon>
    </ListItem>
  );
};
