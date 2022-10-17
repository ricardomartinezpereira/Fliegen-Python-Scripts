
using Microsoft.AspNetCore.Mvc;

namespace UploadFilesServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UploadVideoController : ControllerBase
{

    [HttpPost("UploadFiles")]
    public IActionResult UploadFiles(string name)
    {

        if(!Directory.Exists($"./Files/{name}"))
            Directory.CreateDirectory($"./Files/{name}");
        

        var files = Request.Form.Files;

        files.ToList().ForEach((file) =>
        {
            try
            {
                System.Console.WriteLine(file.FileName);
                var filestream = new FileStream(Path.Combine($"Files/{name}", file.FileName), FileMode.Create);
                file.CopyTo(filestream);
                filestream.Close();
            }
            catch (System.ObjectDisposedException ex)
            {
                System.Console.WriteLine(ex.Message);
            }

        });

        return Ok("Done");
    }

}
