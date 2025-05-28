import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { AppState } from "./types.ts";
import type { RootState } from "./store.ts";

const initialState: AppState = {
  triggerScrapeFormInput: undefined,
  isTriggerScrapeButtonDisabled: true,
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
      if (gameId! > 0) {
        state.triggerScrapeFormInput = gameId;
        state.isTriggerScrapeButtonDisabled = false;
      } else {
        state.triggerScrapeFormInput = undefined;
        state.isTriggerScrapeButtonDisabled = true;
      }
    },
    toggleGameInSidebar: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.games[gameId].isExpandedInSidebar =
        !state.games[gameId].isExpandedInSidebar;
    },
  },
});

export const { setTriggerScrapeFormInput, toggleGameInSidebar } =
  appSlice.actions;

export const selectTriggerScrapeFormInput = (state: RootState) =>
  state.appReducer.triggerScrapeFormInput;
export const selectIsTriggerScrapeFormButtonDisabled = (state: RootState) =>
  state.appReducer.isTriggerScrapeButtonDisabled;
export const selectIsExpandedInSidebar = (state: RootState, gameId: number) =>
  state.appReducer.games[gameId]?.isExpandedInSidebar;

export const appReducer = appSlice.reducer;
