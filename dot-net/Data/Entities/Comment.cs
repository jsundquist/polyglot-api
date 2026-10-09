using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class Comment
{
    public Guid Id { get; set; }

    public Guid IssueId { get; set; }

    public Guid AuthorId { get; set; }

    public string Body { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual User Author { get; set; } = null!;

    public virtual Issue Issue { get; set; } = null!;
}
