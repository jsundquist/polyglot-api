using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class WebhookSubscription
{
    public Guid Id { get; set; }

    public Guid ProjectId { get; set; }

    public string Url { get; set; } = null!;

    public List<string> Events { get; set; } = null!;

    public string Secret { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public virtual Project Project { get; set; } = null!;
}
