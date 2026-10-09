using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class Issue
{
    public Guid Id { get; set; }

    public Guid ProjectId { get; set; }

    public string Title { get; set; } = null!;

    public string? Description { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual ICollection<Comment> Comments { get; set; } = new List<Comment>();

    public virtual Project Project { get; set; } = null!;

    public virtual ICollection<Label> Labels { get; set; } = new List<Label>();

    public virtual ICollection<User> Users { get; set; } = new List<User>();
}
