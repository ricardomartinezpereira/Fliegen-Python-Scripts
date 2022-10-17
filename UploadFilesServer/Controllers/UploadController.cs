
using Microsoft.AspNetCore.Mvc;

namespace UploadFilesServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UploadController : ControllerBase
{

    [HttpPost("UploadFiles")]
    public IActionResult UploadFiles()
    {

        var http = HttpContext.Request.Form.Files;

        http.ToList().ForEach(async (file) =>
        {
            try
            {
                System.Console.WriteLine(file.FileName);
                var filestream = new FileStream(Path.Combine("Files", file.FileName), FileMode.Create);
                await file.CopyToAsync(filestream);
                filestream.Close();
            }
            catch (System.ObjectDisposedException ex)
            {
                System.Console.WriteLine(ex.Message);
            }

        });

        return Ok("Files Copied");
    }
}
