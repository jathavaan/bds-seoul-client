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
