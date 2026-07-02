using Microsoft.AspNetCore.SignalR;
using MinecraftManagementAPI.SignalR;
using System.Diagnostics;

namespace MinecraftManagementAPI.Services
{
    public class ServerService(IHubContext<ConsoleHub> hubContext)
    {
        private Process? _serverProcess;
        private readonly Queue<string> _output = new();
        private readonly int _maxLines = 200;
        private object _lock = new object();

        public bool StartProcess(string path)
        {
            _serverProcess = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = path + "run.bat",
                    UseShellExecute = false,
                    CreateNoWindow = false,
                    WorkingDirectory = path,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                }
            };
            bool result = _serverProcess.Start();

            Task.Run(() => ReadStreamAsync(_serverProcess.StandardOutput));
            Task.Run(() => ReadStreamAsync(_serverProcess.StandardError));

            return result;
        }

        public bool StopProcess()
        {
            if (_serverProcess == null || _serverProcess.HasExited) return true;

            try
            {
                _serverProcess.StandardInput.WriteLine("stop");
                _serverProcess.StandardInput.Flush();

                if (!_serverProcess.WaitForExit(30000))
                    _serverProcess.Kill();
            }
            finally
            {
                _serverProcess = null;
            }
            return true;
        }

        private async Task ReadStreamAsync(TextReader reader)
        {
            try
            {
                while (true)
                {
                    var line = await reader.ReadLineAsync();
                    if (line == null) break;

                    lock (_lock)
                    {
                        _output.Enqueue(line);
                        if (_output.Count > _maxLines)
                            _output.Dequeue();
                    }
                    await hubContext.Clients.All.SendAsync("ReceiveOutput", line);
                }
            }
            catch (Exception ex)
            {

            }
            finally
            {
                _serverProcess = null;
            }
        }

        public IEnumerable<string> GetRecentOutput()
        {
            lock (_lock)
            {
                return _output.ToArray();
            }
        }
    }
}
