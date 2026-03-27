namespace MinecraftManagementAPI.Entity
{
    public class AppUser
    {
        public int Id { get; set; }

        public required string Username { get; set; }

        public byte[] PassHash { get; set; } = [];

        public byte[] PassSalt { get; set; } = [];

    }
}
