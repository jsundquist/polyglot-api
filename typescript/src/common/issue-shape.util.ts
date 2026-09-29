import { Prisma } from '../generated/prisma/client.js';

export const ISSUE_INCLUDE = {
  issue_labels: { select: { label_id: true } },
  issue_assignees: { select: { user_id: true } },
} satisfies Prisma.issuesInclude;

export type IssueWithRelations = Prisma.issuesGetPayload<{
  include: typeof ISSUE_INCLUDE;
}>;

export function toIssue(row: IssueWithRelations) {
  const { issue_labels, issue_assignees, ...rest } = row;
  return {
    ...rest,
    label_ids: issue_labels.map((l) => l.label_id),
    assignee_ids: issue_assignees.map((a) => a.user_id),
  };
}
