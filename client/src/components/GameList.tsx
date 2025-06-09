import {
  CircularProgress,
  Collapse,
  IconButton,
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
import { useGameList, useGameListItem, useKafkaWebsocket } from "../hooks";
import type { GameListProps, ProcessStatusProps } from "../shared/types.ts";

export const GameList = () => {
  const { games } = useGameList();
  useKafkaWebsocket();
  return (
    <List>
      {Object.keys(games).length === 0 ? (
        <ListItem>
          <ListItemText primary="No games available." />
        </ListItem>
      ) : (
        Object.keys(games).map((key) => (
          <GameListItem key={key} steamGameId={Number(key)} />
        ))
      )}
    </List>
  );
};

const GameListItem = (props: GameListProps) => {
  const {
    isExpanded,
    isLoading,
    isActiveGame,
    gameStatuses,
    handleSetActiveGameClick,
    handleExpandGameClick,
  } = useGameListItem(props.steamGameId);

  return (
    <>
      <ListItemButton
        onClick={handleSetActiveGameClick}
        sx={(theme) => ({
          backgroundColor: isActiveGame
            ? theme.palette.primary.dark
            : "transparent",
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
            <CheckIcon color="success" />
          )}
        </ListItemIcon>
        <ListItemIcon>
          <IconButton
            onClick={(e) => {
              e.stopPropagation();
              handleExpandGameClick();
            }}
          >
            {isExpanded ? <ArrowDropUpIcon /> : <ArrowDropDownIcon />}
          </IconButton>
        </ListItemIcon>
      </ListItemButton>
      <Collapse in={isExpanded} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ProcessStatusItem
            statusText="Checking cache"
            status={gameStatuses["cache_check"]}
          />
          <ProcessStatusItem
            statusText="Scraping Steam reviews"
            status={gameStatuses["scrape"]}
          />
          <ProcessStatusItem
            statusText="Running MapReduce job"
            status={gameStatuses["mapreduce"]}
          />
          <ProcessStatusItem
            statusText="Caching result"
            status={gameStatuses["cache_result"]}
          />
        </List>
      </Collapse>
    </>
  );
};

const ProcessStatusItem = (props: ProcessStatusProps) => {
  return (
    <ListItem sx={() => ({})}>
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
              return <CheckIcon sx={{ color: "white" }} />;
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
