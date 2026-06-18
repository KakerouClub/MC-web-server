using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace MinecraftManagementAPI.Controllers
{
    public class ProcessController() : BaseApiController
    {
        [HttpPost("/start_server")]
        public async Task<ActionResult> StartProcess(string path)
        {
            var process = new Process();
            process.StartInfo.FileName = path + "run.bat";
            process.StartInfo.UseShellExecute = true;
            process.StartInfo.CreateNoWindow = false; //false for testing purpose
            process.StartInfo.WorkingDirectory = path;

            var result = process.Start();

            if (!result) return BadRequest("Cannot start process");

            return Ok("Process started with ID: " + process.SessionId);
        }

        [HttpPost("/send_command")]
        public async Task<ActionResult> SendCommand(string command, int id, string? username = null)
        {
            var process = Process.GetProcessById(id);

            if (process == null) return BadRequest("Process could not be found");

            if (username != null) process.StandardInput.Write(command + " " + username + "\n");

            process.StandardInput.Write(command + "\n");
            var result = process.StandardOutput.ReadLine();

            if (result == null) return BadRequest("Cannot read from process output");

            if (!result.StartsWith(DateTime.Now.ToString())) return BadRequest("Cannot send command");

            return Ok(command);

        }

        [HttpPost("/stop_server")]
        public async Task<ActionResult> StopProcess(int id)
        {
            var process = Process.GetProcessById(id);

            if (process == null) return BadRequest("Process could not be found");

            
            process.Kill();
            var result = process.HasExited;

            if (!result) return BadRequest("Process has not been stopped");

            return Ok("Process with id " + id + " has been terminated");
        }
    }
}
