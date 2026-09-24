-- migrate:up

create table users (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now()
);

create type project_status as enum ('active', 'archived');

create table projects (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  key text not null unique,
  description text,
  status project_status not null default 'active',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create type issue_status as enum ('open', 'in-progress', 'closed');

create table issues (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id),
  title text not null,
  description text,
  status issue_status not null default 'open',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index idx_issues_project_id on issues(project_id);
create index idx_issues_status on issues(status);

create table labels (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  color text not null
);

create table issue_labels (
  issue_id uuid not null references issues(id) on delete cascade,
  label_id uuid not null references labels(id) on delete cascade,
  primary key (issue_id, label_id)
);

create table issue_assignees (
  issue_id uuid not null references issues(id) on delete cascade,
  user_id uuid not null references users(id),
  primary key (issue_id, user_id)
);

create table comments (
  id uuid primary key default gen_random_uuid(),
  issue_id uuid not null references issues(id) on delete cascade,
  author_id uuid not null references users(id),
  body text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index idx_comments_issue_id on comments(issue_id);

create table webhook_subscriptions (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  url text not null,
  events text[] not null,
  secret text not null,
  created_at timestamptz not null default now()
);
create index idx_webhook_subscriptions_project_id on webhook_subscriptions(project_id);

-- migrate:down

drop table webhook_subscriptions;
drop table comments;
drop table issue_assignees;
drop table issue_labels;
drop table labels;
drop table issues;
drop type issue_status;
drop table projects;
drop type project_status;
drop table users;
