export interface AppState {
  triggerScrapeFormInput: number | undefined;
  isTriggerScrapeButtonDisabled: boolean;
  games: { [gameId: number]: Game };
}

export interface Game {
  gameId: number;
  isLoading: boolean;
  isExpandedInSidebar: boolean;
  isActiveInTableView: boolean;
  recommendations: Recommendation[];
}

export interface Recommendation {
  timeInterval: string;
  sumRecommended: number;
  sumNotRecommended: number;
}
