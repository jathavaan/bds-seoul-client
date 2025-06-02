export interface AppState {
  activeGameId: number | undefined;
  triggerScrapeFormInput: number | undefined;
  isTriggerScrapeButtonDisabled: boolean;
  activeTab: 1 | 2;
  activeRecommendations: Recommendation[] | undefined;
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
  time_interval: string;
  sum_recommended: number;
  sum_not_recommended: number;
}

export interface GetRecommendationsByGameIdRequest {
  steam_game_id: number;
}

export interface GetRecommendationsByGameIdResponse {
  result: Recommendation[];
}

export interface BarchartProps {
  recommendations: Recommendation[];
}
