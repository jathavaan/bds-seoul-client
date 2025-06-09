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
  processStatuses: Record<ProcessType, ProcessStatus>;
}

export interface Recommendation {
  time_interval: string;
  sum_recommended: number;
  sum_not_recommended: number;
}

export interface GetRecommendationsByGameIdRequest {
  steam_game_id: number;
  max_review_count: number;
}

export interface GetRecommendationsByGameIdResponse {
  result: Recommendation[];
}

export interface BarchartProps {
  recommendations: Recommendation[];
}

export type ProcessType =
  | "cache_check"
  | "scrape"
  | "mapreduce"
  | "cache_result";

export type ProcessStatus =
  | "queued"
  | "in_progress"
  | "skipped"
  | "completed"
  | "failed";

export interface GameListProps {
  steamGameId: number;
}

export interface ProcessStatusProps {
  statusText: string;
  status: ProcessStatus;
}
