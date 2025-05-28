export type ProcessStatus =
  | "queued"
  | "in_progress"
  | "skipped"
  | "completed"
  | "failed";

export interface GameListProps {
  steamGameId: number;
  isLoading: boolean;
  isExpanded: boolean;
}

export interface ProcessStatusProps {
  statusText: string;
  status: ProcessStatus;
}
