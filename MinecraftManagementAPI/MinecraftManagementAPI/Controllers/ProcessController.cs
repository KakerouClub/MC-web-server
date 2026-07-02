using Microsoft.AspNetCore.Mvc;
using MinecraftManagementAPI.Services;
using System.Diagnostics;

namespace MinecraftManagementAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ProcessController(ServerService serverService) : BaseApiController
    {

        [HttpPost("/start_server")]
        public async Task<ActionResult> StartProcess(string path)
        {
            bool result = serverService.StartProcess(path);

            if (!result) return BadRequest("Process failed to start");

            return Ok("Process started successfully");
        }

        [HttpPost("/stop_server")]
        public async Task<ActionResult> StopProcess()
        {
            if (!serverService.StopProcess()) return BadRequest("Process could not be stopped");

            return Ok("Process has been terminated");
        }

        [HttpGet("/get_output")]
        public async Task<ActionResult> GetConsoleOutput()
        {
            return Ok(serverService.GetRecentOutput());
        }

        [HttpPost("/send_command")]
        public async Task<ActionResult> SendCommand(string command, int id, string? username = null)
        {
            throw new NotImplementedException();
        }
    }
}
