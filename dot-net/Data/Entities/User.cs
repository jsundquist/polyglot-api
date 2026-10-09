using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class User
{
    public Guid Id { get; set; }

    public DateTime CreatedAt { get; set; }

    public virtual ICollection<Comment> Comments { get; set; } = new List<Comment>();

    public virtual ICollection<Issue> Issues { get; set; } = new List<Issue>();
}
