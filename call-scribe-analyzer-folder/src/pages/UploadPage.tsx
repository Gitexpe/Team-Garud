
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { UploadForm } from "@/components/CallRecording/UploadForm";
import { Activity } from "lucide-react";

const UploadPage = () => {
  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold">Upload Call Recording</h1>
        <p className="text-muted-foreground">
          Upload an audio file to analyze silences, overtalk, and get transcription
        </p>
      </div>
      
      <div className="grid md:grid-cols-2 gap-8">
        <UploadForm />
        
        <Card className="bg-muted/50 border border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="text-primary" />
              How it works
            </CardTitle>
            <CardDescription>
              Our analysis process helps you gain insights from your calls
            </CardDescription>
          </CardHeader>
          <div className="px-6 pb-6">
            <ol className="space-y-4">
              <li className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border bg-background text-sm font-medium">
                  1
                </div>
                <div>
                  <p className="font-medium">Upload your recording</p>
                  <p className="text-sm text-muted-foreground">
                    Upload an audio file of your call (MP3, WAV, M4A formats supported)
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border bg-background text-sm font-medium">
                  2
                </div>
                <div>
                  <p className="font-medium">Automatic processing</p>
                  <p className="text-sm text-muted-foreground">
                    Our system analyzes the audio for silence, overtalk, and generates a transcription
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border bg-background text-sm font-medium">
                  3
                </div>
                <div>
                  <p className="font-medium">View insights</p>
                  <p className="text-sm text-muted-foreground">
                    Review detailed analysis to improve call quality and identify areas for improvement
                  </p>
                </div>
              </li>
            </ol>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default UploadPage;
