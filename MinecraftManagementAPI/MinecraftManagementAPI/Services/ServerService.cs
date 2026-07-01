using System.Diagnostics;

namespace MinecraftManagementAPI.Services
{
    public class ServerService
    {
        private Process? _ServerProcess;


        public bool StartProcess(string path)
        {
            _ServerProcess = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = path + "run.bat",
                    UseShellExecute = false,
                    CreateNoWindow = false,
                    WorkingDirectory = path,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true
                }
            };
            bool result = _ServerProcess.Start();

            return result;
        }

        public bool StopProcess()
        {
            if (_ServerProcess == null || _ServerProcess.HasExited) return true;

            try
            {
                _ServerProcess.StandardInput.WriteLine("stop");
                _ServerProcess.StandardInput.Flush();

                if (!_ServerProcess.WaitForExit(30000))
                    _ServerProcess.Kill();
            }
            finally
            {
                _ServerProcess = null;
            }
            return true;
        }
    }
}
