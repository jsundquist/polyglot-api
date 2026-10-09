using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class Project
{
    public Guid Id { get; set; }

    public string Name { get; set; } = null!;

    public string Key { get; set; } = null!;

    public string? Description { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual ICollection<Issue> Issues { get; set; } = new List<Issue>();

    public virtual ICollection<WebhookSubscription> WebhookSubscriptions { get; set; } = new List<WebhookSubscription>();
}
