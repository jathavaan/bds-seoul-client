import { useDispatch, useSelector } from "react-redux";
import {
  addGameToDictionary,
  addRecommendations,
  selectIsTriggerScrapeFormButtonDisabled,
  selectTriggerScrapeFormInput,
  setGameToLoadingState,
  setTriggerScrapeFormInput,
} from "../shared";
import type { AppDispatch } from "../shared/store.ts";
import { fetch } from "../services/api.ts";
import type {
  GetRecommendationsByGameIdRequest,
  GetRecommendationsByGameIdResponse,
} from "../shared/types.ts";

export const useTriggerScrapeForm = () => {
  const dispatch = useDispatch<AppDispatch>();
  const formValue = useSelector(selectTriggerScrapeFormInput);
  const isButtonDisabled = useSelector(selectIsTriggerScrapeFormButtonDisabled);

  const handleScrapeFormUpdate = (gameId: string) => {
    dispatch(setTriggerScrapeFormInput(gameId));
  };

  const onButtonClick = async () => {
    if (!formValue) return;

    dispatch(addGameToDictionary(formValue));
    dispatch(setGameToLoadingState(formValue));
    const queryParameters: GetRecommendationsByGameIdRequest = {
      steam_game_id: formValue,
      max_review_count: 500,
    };

    const response = await fetch<
      GetRecommendationsByGameIdRequest,
      GetRecommendationsByGameIdResponse
    >("/recommendations", queryParameters);

    dispatch(
      addRecommendations({
        gameId: formValue,
        recommendations: response.result,
      }),
    );
  };

  return { formValue, isButtonDisabled, handleScrapeFormUpdate, onButtonClick };
};
