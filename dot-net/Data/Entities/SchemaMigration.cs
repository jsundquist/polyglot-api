using System;
using System.Collections.Generic;

namespace dot_net.Data.Entities;

public partial class SchemaMigration
{
    public string Version { get; set; } = null!;
}
