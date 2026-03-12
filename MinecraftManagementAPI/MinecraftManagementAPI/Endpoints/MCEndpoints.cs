using Microsoft.AspNetCore.Http.HttpResults;
using System.Diagnostics;
using MinecraftManagementAPI.Data;

namespace MinecraftManagementAPI.Endpoints
{
    public static class MCEndpoints
    {
        public static void RegisterEndpoints(this WebApplication app)
        {
            app.MapGet("/login", Login);
            app.MapPost("/start", StartServer);
            app.MapPost("/stop", StopServer);
            app.MapPost("/command", ExecuteCommand);
            app.MapGet("/output", GetOutput);
        }

        static async Task<Results<Ok, NotFound>> StartServer()
        {
            Process process = new Process();
            process.StartInfo.FileName = "F:\\Servers\\SevTech\\ServerStart.bat";
            bool status = process.Start();
            if (status)
            {
                return TypedResults.Ok();
            }
            else
            {
                return TypedResults.NotFound();

            }
        }

        static async Task<Results<Ok, NotFound>> StopServer()
        {
            Process process = Process.GetProcessesByName("server")[0];
            if (process != null)
            {
                process.Kill();
                return TypedResults.Ok();
            }
            else
            {
                return TypedResults.NotFound();
            }
        }

        static async Task<Results<Ok<Command>, NotFound>> ExecuteCommand()
        {
            Command cmd = new Command("");
            Process process = Process.GetProcessesByName("server")[0];
            if (process != null)
            {
                process.StandardInput.WriteLine(cmd);
                return TypedResults.Ok(cmd);
            }
            else
            {
                return TypedResults.NotFound();
            }
        }


        static async Task<Results<Ok<Output>, NotFound>> GetOutput()
        {
            Process process = Process.GetProcessesByName("server")[0];
            if (process != null)
            {
                Output output = new Output();
                output.output = process.StandardOutput.ReadToEnd();
                return TypedResults.Ok(output);
            }
            else
            {
                return TypedResults.NotFound();
            }
        }

        static async Task<Results<Ok<User>, NotFound>> Login()
        {
            User user = new User();
            user.Username = "admin";
            user.Password = "password";
            return TypedResults.Ok(user);
        }

    }
}
