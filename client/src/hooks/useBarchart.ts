import { useDispatch, useSelector } from "react-redux";
import {
  selectActiveGameId,
  selectActiveRecommendations,
  selectActiveTab,
  selectIsAwaitingResultFromScrape,
  setActiveTab,
} from "../shared";
import type { AppDispatch, RootState } from "../shared/store.ts";

export const useBarchart = () => {
  const dispatch = useDispatch<AppDispatch>();
  const gameId = useSelector(selectActiveGameId);
  const activeTabId = useSelector(selectActiveTab);
  const recommendations = useSelector(selectActiveRecommendations);

  const isLoading =
    useSelector((state: RootState) =>
      selectIsAwaitingResultFromScrape(state, gameId!),
    ) && gameId !== undefined;

  const onTabClick = (tabId: number) => {
    dispatch(setActiveTab(tabId));
  };

  return { isLoading, gameId, activeTabId, recommendations, onTabClick };
};
