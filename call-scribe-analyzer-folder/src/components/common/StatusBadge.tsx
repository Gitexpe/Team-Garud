
import { Badge } from "@/components/ui/badge";
import { CallRecording } from "@/types";

type StatusBadgeProps = {
  status: CallRecording['status'];
};

export const StatusBadge = ({ status }: StatusBadgeProps) => {
  const variants = {
    pending: "bg-amber-500/20 text-amber-500 hover:bg-amber-500/30",
    processing: "bg-blue-500/20 text-blue-500 hover:bg-blue-500/30 animate-pulse-opacity",
    completed: "bg-green-500/20 text-green-500 hover:bg-green-500/30",
    failed: "bg-red-500/20 text-red-500 hover:bg-red-500/30"
  };

  const statusLabels = {
    pending: "Pending",
    processing: "Processing",
    completed: "Completed",
    failed: "Failed"
  };

  return (
    <Badge className={variants[status]} variant="outline">
      {statusLabels[status]}
    </Badge>
  );
};
