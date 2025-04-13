
import { useEffect, useState } from "react";
import { api } from "@/services/api";
import { CallRecording } from "@/types";
import { StatusBadge } from "@/components/common/StatusBadge";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { FileAudio, Mic, Layers, Clock, Calendar, MoreHorizontal } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

export const RecordingList = () => {
  const [recordings, setRecordings] = useState<CallRecording[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRecordings = async () => {
      try {
        const data = await api.getRecordings();
        setRecordings(data);
      } catch (err) {
        setError("Failed to fetch recordings");
      } finally {
        setLoading(false);
      }
    };

    fetchRecordings();
  }, []);

  // Format seconds to mm:ss
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Format date string
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    }).format(date);
  };

  if (loading) return <LoadingSpinner />;

  if (error) {
    return (
      <Card className="border-destructive">
        <CardContent className="pt-6">
          <div className="text-center text-destructive">
            <p>{error}</p>
            <Button variant="outline" className="mt-4" onClick={() => window.location.reload()}>
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">Call Recordings</h2>
          <p className="text-muted-foreground">Manage and analyze your call recordings</p>
        </div>
        <Button asChild>
          <Link to="/upload">
            Upload New
          </Link>
        </Button>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Filename</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Created</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recordings.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8">
                    <p className="text-muted-foreground">No recordings found</p>
                    <Button variant="outline" size="sm" className="mt-2" asChild>
                      <Link to="/upload">Upload your first recording</Link>
                    </Button>
                  </TableCell>
                </TableRow>
              ) : (
                recordings.map((recording) => (
                  <TableRow key={recording.id} className="group">
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <FileAudio size={16} className="text-muted-foreground" />
                        <span className="font-medium">{recording.filename}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1 text-muted-foreground">
                        <Clock size={14} />
                        <span>{formatDuration(recording.duration)}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={recording.status} />
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1 text-muted-foreground">
                        <Calendar size={14} />
                        <span>{formatDate(recording.created_at)}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2 justify-end">
                        {recording.status === 'completed' && (
                          <>
                            <Button variant="outline" size="icon" className="h-8 w-8">
                              <FileAudio size={16} className="text-primary" />
                            </Button>
                            <Button variant="outline" size="icon" className="h-8 w-8">
                              <Mic size={16} className="text-secondary" />
                            </Button>
                            <Button variant="outline" size="icon" className="h-8 w-8">
                              <Layers size={16} className="text-amber-500" />
                            </Button>
                          </>
                        )}
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon" className="h-8 w-8">
                              <MoreHorizontal size={16} />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>View Details</DropdownMenuItem>
                            <DropdownMenuItem>Download</DropdownMenuItem>
                            <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};
