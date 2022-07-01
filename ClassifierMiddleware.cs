namespace BreastCancerClassifier;

using System.Diagnostics;

public static class ClassifierMiddleware
{
    const string script = "classify.py";

    const string runner = "/usr/bin/python3";
    // const string runner = "/home/leer/python37Env/bin/python";

    public static ClassifyResponse Classify(IFormFile image)
    {
        var imagePath = SaveImage(image);


        var psi = new ProcessStartInfo
        {
            FileName = runner,
            Arguments = $"\"{Path.GetFullPath(script)}\" \"{imagePath}\"",
            UseShellExecute = false,
            CreateNoWindow = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        };


        var errors = string.Empty;
        var res = string.Empty;

        using var process = Process.Start(psi);

        errors = process.StandardError.ReadToEnd();
        res = process.StandardOutput.ReadToEnd();

        Console.WriteLine("RES");
        Console.WriteLine(res);
        Console.WriteLine("ERR");
        Console.WriteLine(errors);

        var lines = res.Split("\n");
        var resClass = lines[Array.IndexOf(lines, "class") + 1].Trim();

        return new ClassifyResponse
        {
            Class = resClass,
            Message = "error are disabled temporarily",
        };
    }

    private static string SaveImage(IFormFile image)
    {
        var uploadsFolder = Path.GetFullPath("images");
        var uniqueFileName = Guid.NewGuid() + "_" + image.FileName;
        var filePath = Path.Combine(uploadsFolder, uniqueFileName);
        using var fileStream = new FileStream(filePath, FileMode.Create);
        image.CopyTo(fileStream);

        return Path.Combine(uploadsFolder, uniqueFileName);
    }
}