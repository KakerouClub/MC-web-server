using Microsoft.EntityFrameworkCore;
using MinecraftManagementAPI.Entity;

namespace MinecraftManagementAPI.Data
{
    public class DataContext(DbContextOptions options) : DbContext(options)
    {
        public DbSet<AppUser> Users {  get; set; }
    }
}
