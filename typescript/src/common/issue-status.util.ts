import z from 'zod';
import type { issue_status } from '../generated/prisma/enums.js';

// The API (and DB) value is "in-progress"; Prisma exposes it as the
// identifier `in_progress`, so translate at the API boundary.
export const API_ISSUE_STATUSES = ['open', 'in-progress', 'closed'] as const;
export type ApiIssueStatus = (typeof API_ISSUE_STATUSES)[number];

export function toApiStatus(status: issue_status): ApiIssueStatus {
  return status === 'in_progress' ? 'in-progress' : status;
}

export function toDbStatus(status: ApiIssueStatus): issue_status {
  return status === 'in-progress' ? 'in_progress' : status;
}

export const issueStatusSchema = z
  .enum(API_ISSUE_STATUSES)
  .transform(toDbStatus);
