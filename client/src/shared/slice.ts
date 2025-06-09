import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type {
  AppState,
  ProcessStatus,
  ProcessType,
  Recommendation,
} from "./types.ts";
import type { RootState } from "./store.ts";

const initialState: AppState = {
  triggerScrapeFormInput: undefined,
  isTriggerScrapeButtonDisabled: true,
  activeGameId: undefined,
  activeRecommendations: undefined,
  activeTab: 1,
  games: {},
};

const appSlice = createSlice({
  name: "app",
  initialState,
  reducers: {
    setTriggerScrapeFormInput: (state, action: PayloadAction<string>) => {
      if (!action.payload || action.payload.trim() === "") {
        state.triggerScrapeFormInput = undefined;
        state.isTriggerScrapeButtonDisabled = true;
      }

      const gameId = Number(action.payload);
      if (gameId > 0) {
        state.triggerScrapeFormInput = gameId;
        state.isTriggerScrapeButtonDisabled = false;
      } else {
        state.triggerScrapeFormInput = undefined;
        state.isTriggerScrapeButtonDisabled = true;
      }
    },
    setActiveGame: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.activeGameId = gameId;
      state.activeRecommendations = state.games[gameId].recommendations;
    },
    toggleGameInSidebar: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.games[gameId].isExpandedInSidebar =
        !state.games[gameId].isExpandedInSidebar;
    },
    addGameToDictionary: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.games[gameId] = {
        gameId: gameId,
        isAwaitingResultFromScrape: true,
        isExpandedInSidebar: true,
        isActiveInTableView: true,
        recommendations: [],
        processStatuses: {
          cache_check: "in_progress",
          scrape: "queued",
          mapreduce: "queued",
          cache_result: "queued",
        },
      };
    },
    setActiveTab: (state, action: PayloadAction<number>) => {
      const tabId = action.payload;
      if (tabId === 1 || tabId === 2) {
        state.activeTab = tabId;
      }
    },
    addRecommendations: (
      state,
      action: PayloadAction<{
        gameId: number;
        recommendations: Recommendation[];
      }>,
    ) => {
      const { gameId, recommendations } = action.payload;
      if (state.games[gameId]) {
        state.games[gameId].recommendations = recommendations;
        state.games[gameId].isAwaitingResultFromScrape = false;
      }
    },
    setGameToLoadingState: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      if (state.games[gameId]) {
        state.games[gameId].isAwaitingResultFromScrape = true;
      }
    },
    updateGameProcessStatus: (
      state,
      action: PayloadAction<{
        gameId: number;
        type: ProcessType;
        status: ProcessStatus;
      }>,
    ) => {
      const { gameId, type, status } = action.payload;
      if (state.games[gameId]) {
        state.games[gameId].processStatuses[type] = status;
      }
    },
  },
});

export const {
  setTriggerScrapeFormInput,
  toggleGameInSidebar,
  addGameToDictionary,
  setActiveGame,
  setActiveTab,
  addRecommendations,
  setGameToLoadingState,
  updateGameProcessStatus,
} = appSlice.actions;

export const selectTriggerScrapeFormInput = (state: RootState) =>
  state.appReducer.triggerScrapeFormInput;
export const selectIsTriggerScrapeFormButtonDisabled = (state: RootState) =>
  state.appReducer.isTriggerScrapeButtonDisabled;
export const selectIsExpandedInSidebar = (state: RootState, gameId: number) =>
  state.appReducer.games[gameId]?.isExpandedInSidebar;
export const selectIsAwaitingResultFromScrape = (
  state: RootState,
  gameId: number,
) => state.appReducer.games[gameId]?.isAwaitingResultFromScrape;
export const selectGames = (state: RootState) => state.appReducer.games;
export const selectActiveGameId = (state: RootState) =>
  state.appReducer.activeGameId;
export const selectActiveTab = (state: RootState) => state.appReducer.activeTab;
export const selectActiveRecommendations = (state: RootState) =>
  state.appReducer.activeRecommendations;
export const selectGameProcessStatuses = (state: RootState, gameId: number) =>
  state.appReducer.games[gameId]?.processStatuses;

export const appReducer = appSlice.reducer;
