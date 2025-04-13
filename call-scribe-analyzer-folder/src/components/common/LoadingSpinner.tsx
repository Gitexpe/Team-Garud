
import { Loader2 } from "lucide-react";

type LoadingSpinnerProps = {
  size?: number;
  className?: string;
};

export const LoadingSpinner = ({ size = 24, className = "" }: LoadingSpinnerProps) => {
  return (
    <div className="flex justify-center items-center w-full py-4">
      <Loader2 className={`animate-spin text-primary ${className}`} size={size} />
    </div>
  );
};
