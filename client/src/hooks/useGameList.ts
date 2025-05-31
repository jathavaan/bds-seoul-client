import { useDispatch, useSelector } from "react-redux";
import {
  selectActiveGameId,
  selectGames,
  selectIsAwaitingResultFromScrape,
  selectIsExpandedInSidebar,
  setActiveGame,
  toggleGameInSidebar,
} from "../shared";
import type { AppDispatch, RootState } from "../shared/store.ts";

export const useGameList = () => {
  const games = useSelector(selectGames);
  return { games };
};

export const useGameListItem = (gameId: number) => {
  const dispatch = useDispatch<AppDispatch>();
  const isExpanded = useSelector((state: RootState) =>
    selectIsExpandedInSidebar(state, gameId),
  );

  const isActiveGame = useSelector(selectActiveGameId) == gameId;

  const isLoading = useSelector((state: RootState) =>
    selectIsAwaitingResultFromScrape(state, gameId),
  );

  const handleSetActiveGameClick = () => {
    dispatch(setActiveGame(gameId));
  };

  const handleExpandGameClick = () => {
    dispatch(toggleGameInSidebar(gameId));
  };

  return {
    isExpanded,
    isLoading,
    isActiveGame,
    handleSetActiveGameClick,
    handleExpandGameClick,
  };
};
