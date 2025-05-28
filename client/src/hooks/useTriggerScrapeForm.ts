import { useDispatch, useSelector } from "react-redux";
import {
  selectIsTriggerScrapeFormButtonDisabled,
  selectTriggerScrapeFormInput,
  setTriggerScrapeFormInput,
} from "../shared";
import type { AppDispatch } from "../shared/store.ts";

export const useTriggerScrapeForm = () => {
  const dispatch = useDispatch<AppDispatch>();
  const formValue = useSelector(selectTriggerScrapeFormInput);
  const isButtonDisabled = useSelector(selectIsTriggerScrapeFormButtonDisabled);

  const handleScrapeFormUpdate = (gameId: string) => {
    dispatch(setTriggerScrapeFormInput(gameId));
  };

  const onButtonClick = () => {};

  return { formValue, isButtonDisabled, handleScrapeFormUpdate, onButtonClick };
};
