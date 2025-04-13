
import { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { Upload, AlertCircle, CheckCircle2 } from "lucide-react";
import { api } from "@/services/api";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

export const UploadForm = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first");
      return;
    }

    try {
      setIsUploading(true);
      setError(null);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 95) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 5;
        });
      }, 200);

      // Upload the file
      await api.uploadRecording(selectedFile);
      
      // Ensure 100% at the end
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      toast({
        title: "Upload Complete",
        description: `${selectedFile.name} has been uploaded successfully.`,
      });

      // Navigate back to recordings list after a short delay
      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (err) {
      setError("Failed to upload file. Please try again.");
      setUploadProgress(0);
      toast({
        title: "Upload Failed",
        description: "There was an error uploading your file.",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Upload Call Recording</CardTitle>
        <CardDescription>
          Upload an audio file of a call to analyze silence, overtalk, and get transcription.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid w-full items-center gap-1.5">
            <Label htmlFor="recording">Audio File</Label>
            <div
              className={`border-2 border-dashed rounded-md p-6 flex flex-col items-center justify-center ${
                error ? "border-destructive" : "border-muted-foreground/20"
              }`}
            >
              <Input
                id="recording"
                type="file"
                accept="audio/*"
                className="hidden"
                onChange={handleFileChange}
                disabled={isUploading}
              />
              <Label
                htmlFor="recording"
                className="flex flex-col items-center justify-center gap-2 cursor-pointer w-full h-full"
              >
                <Upload size={36} className="text-muted-foreground" />
                <span className="text-sm text-muted-foreground">
                  {selectedFile ? selectedFile.name : "Click to upload or drag and drop"}
                </span>
                <span className="text-xs text-muted-foreground/70">
                  MP3, WAV, M4A up to 100MB
                </span>
              </Label>
            </div>
            {error && (
              <div className="flex items-center gap-1 text-destructive text-sm mt-1">
                <AlertCircle size={14} />
                <span>{error}</span>
              </div>
            )}
          </div>

          {selectedFile && !isUploading && !error && (
            <div className="flex items-center gap-2 text-sm text-primary">
              <CheckCircle2 size={16} />
              <span>File selected: {selectedFile.name}</span>
            </div>
          )}

          {isUploading && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm">Uploading...</span>
                <span className="text-sm">{uploadProgress}%</span>
              </div>
              <Progress value={uploadProgress} className="h-2" />
            </div>
          )}
        </div>
      </CardContent>
      <CardFooter>
        <Button
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
          className="w-full"
        >
          {isUploading ? "Uploading..." : "Upload & Analyze"}
        </Button>
      </CardFooter>
    </Card>
  );
};
