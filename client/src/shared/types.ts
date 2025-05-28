export interface AppState {
  triggerScrapeFormInput: number | undefined;
  isTriggerScrapeButtonDisabled: boolean;
  games: Record<number, Game>;
}

export interface Game {
  gameId: number;
  isAwaitingResultFromScrape: boolean;
  isExpandedInSidebar: boolean;
  isActiveInTableView: boolean;
  recommendations: Recommendation[];
}

export interface Recommendation {
  timeInterval: string;
  sumRecommended: number;
  sumNotRecommended: number;
}
