using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using dot_net.Data.Entities;

namespace dot_net.Data;

public partial class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Comment> Comments { get; set; }

    public virtual DbSet<Issue> Issues { get; set; }

    public virtual DbSet<Label> Labels { get; set; }

    public virtual DbSet<Project> Projects { get; set; }

    public virtual DbSet<SchemaMigration> SchemaMigrations { get; set; }

    public virtual DbSet<User> Users { get; set; }

    public virtual DbSet<WebhookSubscription> WebhookSubscriptions { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder
            .HasPostgresEnum("issue_status", new[] { "open", "in-progress", "closed" })
            .HasPostgresEnum("project_status", new[] { "active", "archived" })
            .HasPostgresExtension("pgcrypto");

        modelBuilder.Entity<Comment>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("comments_pkey");

            entity.ToTable("comments");

            entity.HasIndex(e => e.IssueId, "idx_comments_issue_id");

            entity.Property(e => e.Id)
                .HasDefaultValueSql("gen_random_uuid()")
                .HasColumnName("id");
            entity.Property(e => e.AuthorId).HasColumnName("author_id");
            entity.Property(e => e.Body).HasColumnName("body");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("created_at");
            entity.Property(e => e.IssueId).HasColumnName("issue_id");
            entity.Property(e => e.UpdatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("updated_at");

            entity.HasOne(d => d.Author).WithMany(p => p.Comments)
                .HasForeignKey(d => d.AuthorId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("comments_author_id_fkey");

            entity.HasOne(d => d.Issue).WithMany(p => p.Comments)
                .HasForeignKey(d => d.IssueId)
                .HasConstraintName("comments_issue_id_fkey");
        });

        modelBuilder.Entity<Issue>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("issues_pkey");

            entity.ToTable("issues");

            entity.HasIndex(e => e.ProjectId, "idx_issues_project_id");

            entity.Property(e => e.Id)
                .HasDefaultValueSql("gen_random_uuid()")
                .HasColumnName("id");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("created_at");
            entity.Property(e => e.Description).HasColumnName("description");
            entity.Property(e => e.ProjectId).HasColumnName("project_id");
            entity.Property(e => e.Title).HasColumnName("title");
            entity.Property(e => e.UpdatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("updated_at");

            entity.HasOne(d => d.Project).WithMany(p => p.Issues)
                .HasForeignKey(d => d.ProjectId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("issues_project_id_fkey");

            entity.HasMany(d => d.Labels).WithMany(p => p.Issues)
                .UsingEntity<Dictionary<string, object>>(
                    "IssueLabel",
                    r => r.HasOne<Label>().WithMany()
                        .HasForeignKey("LabelId")
                        .HasConstraintName("issue_labels_label_id_fkey"),
                    l => l.HasOne<Issue>().WithMany()
                        .HasForeignKey("IssueId")
                        .HasConstraintName("issue_labels_issue_id_fkey"),
                    j =>
                    {
                        j.HasKey("IssueId", "LabelId").HasName("issue_labels_pkey");
                        j.ToTable("issue_labels");
                        j.IndexerProperty<Guid>("IssueId").HasColumnName("issue_id");
                        j.IndexerProperty<Guid>("LabelId").HasColumnName("label_id");
                    });

            entity.HasMany(d => d.Users).WithMany(p => p.Issues)
                .UsingEntity<Dictionary<string, object>>(
                    "IssueAssignee",
                    r => r.HasOne<User>().WithMany()
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.ClientSetNull)
                        .HasConstraintName("issue_assignees_user_id_fkey"),
                    l => l.HasOne<Issue>().WithMany()
                        .HasForeignKey("IssueId")
                        .HasConstraintName("issue_assignees_issue_id_fkey"),
                    j =>
                    {
                        j.HasKey("IssueId", "UserId").HasName("issue_assignees_pkey");
                        j.ToTable("issue_assignees");
                        j.IndexerProperty<Guid>("IssueId").HasColumnName("issue_id");
                        j.IndexerProperty<Guid>("UserId").HasColumnName("user_id");
                    });
        });

        modelBuilder.Entity<Label>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("labels_pkey");

            entity.ToTable("labels");

            entity.HasIndex(e => e.Name, "labels_name_key").IsUnique();

            entity.Property(e => e.Id)
                .HasDefaultValueSql("gen_random_uuid()")
                .HasColumnName("id");
            entity.Property(e => e.Color).HasColumnName("color");
            entity.Property(e => e.Name).HasColumnName("name");
        });

        modelBuilder.Entity<Project>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("projects_pkey");

            entity.ToTable("projects");

            entity.HasIndex(e => e.Key, "projects_key_key").IsUnique();

            entity.Property(e => e.Id)
                .HasDefaultValueSql("gen_random_uuid()")
                .HasColumnName("id");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("created_at");
            entity.Property(e => e.Description).HasColumnName("description");
            entity.Property(e => e.Key).HasColumnName("key");
            entity.Property(e => e.Name).HasColumnName("name");
            entity.Property(e => e.UpdatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("updated_at");
        });

        modelBuilder.Entity<SchemaMigration>(entity =>
        {
            entity.HasKey(e => e.Version).HasName("schema_migrations_pkey");

            entity.ToTable("schema_migrations");

            entity.Property(e => e.Version)
                .HasColumnType("character varying")
                .HasColumnName("version");
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("users_pkey");

            entity.ToTable("users");

            entity.Property(e => e.Id)
                .HasDefaultValueSql("gen_random_uuid()")
                .HasColumnName("id");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("created_at");
        });

        modelBuilder.Entity<WebhookSubscription>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("webhook_subscriptions_pkey");

            entity.ToTable("webhook_subscriptions");

            entity.HasIndex(e => e.ProjectId, "idx_webhook_subscriptions_project_id");

            entity.Property(e => e.Id)
                .HasDefaultValueSql("gen_random_uuid()")
                .HasColumnName("id");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("now()")
                .HasColumnName("created_at");
            entity.Property(e => e.Events).HasColumnName("events");
            entity.Property(e => e.ProjectId).HasColumnName("project_id");
            entity.Property(e => e.Secret).HasColumnName("secret");
            entity.Property(e => e.Url).HasColumnName("url");

            entity.HasOne(d => d.Project).WithMany(p => p.WebhookSubscriptions)
                .HasForeignKey(d => d.ProjectId)
                .HasConstraintName("webhook_subscriptions_project_id_fkey");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
