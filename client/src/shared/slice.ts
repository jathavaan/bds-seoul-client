import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { AppState } from "./types.ts";
import type { RootState } from "./store.ts";

const initialState: AppState = {
  triggerScrapeFormInput: undefined,
  isTriggerScrapeButtonDisabled: true,
  activeGameId: undefined,
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
    toggleGameInSidebar: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.activeGameId = gameId;
      state.games[gameId].isExpandedInSidebar =
        !state.games[gameId].isExpandedInSidebar;
    },
    addGameToDictionary: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.games[gameId] = {
        gameId: gameId,
        isAwaitingResultFromScrape: false,
        isExpandedInSidebar: true,
        isActiveInTableView: true,
        recommendations: [],
      };
    },
    setActiveTab: (state, action: PayloadAction<number>) => {
      const tabId = action.payload;
      if (tabId === 1 || tabId === 2) {
        state.activeTab = tabId;
      }
    },
  },
});

export const {
  setTriggerScrapeFormInput,
  toggleGameInSidebar,
  addGameToDictionary,
  setActiveTab,
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

export const appReducer = appSlice.reducer;
