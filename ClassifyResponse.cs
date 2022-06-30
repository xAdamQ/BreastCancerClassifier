namespace BreastCancerClassifier;

[Serializable]
public class ClassifyResponse
{
    public string Class { set; get; }
    public string Message { set; get; }
}