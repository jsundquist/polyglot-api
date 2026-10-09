using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class Label
{
    public Guid Id { get; set; }

    public string Name { get; set; } = null!;

    public string Color { get; set; } = null!;

    public virtual ICollection<Issue> Issues { get; set; } = new List<Issue>();
}
