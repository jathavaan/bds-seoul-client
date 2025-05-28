export interface AppState {
  activeGameId: number | undefined;
  triggerScrapeFormInput: number | undefined;
  isTriggerScrapeButtonDisabled: boolean;
  activeTab: 1 | 2;
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
