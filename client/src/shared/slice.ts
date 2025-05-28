import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { AppState } from "./types.ts";
import type { RootState } from "./store.ts";

const initialState: AppState = {
  games: {},
};

const appSlice = createSlice({
  name: "app",
  initialState,
  reducers: {
    toggleGameInSidebar: (state, action: PayloadAction<number>) => {
      const gameId = action.payload;
      state.games[gameId].isExpandedInSidebar =
        !state.games[gameId].isExpandedInSidebar;
    },
  },
});

export const { toggleGameInSidebar } = appSlice.actions;

export const selectIsExpandedInSidebar = (state: RootState, gameId: number) =>
  state.games[gameId]?.isExpandedInSidebar;

export const appReducer = appSlice.reducer;
