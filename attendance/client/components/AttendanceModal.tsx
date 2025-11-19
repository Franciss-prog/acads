"use client";
import { X, Loader2 } from "lucide-react";
import { useState } from "react";
import { postAttendance } from "@/actions/qrCodeActions";
import { toast } from "sonner";
import axios from "axios";

type ScanResult = {
  token: string;
  userName: string;
};

type AttendanceModalProps = {
  scanResult: ScanResult;
  onClose: () => void;
  onComplete?: () => void;
};

export const AttendanceModal = ({
  scanResult,
  onClose,
  onComplete,
}: AttendanceModalProps) => {
  const [hours, setHours] = useState<number | "">("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!hours) {
      toast.warning("Select the number of hours before submitting.");
      return;
    }

    setIsSubmitting(true);
    try {
      await postAttendance(scanResult.token, hours);
      onClose();
      if (onComplete) onComplete();
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 429) {
        return;
      } else {
        toast.error("Something went wrong. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div
        className="rounded-lg w-full max-w-sm border shadow-md"
        style={{
          backgroundColor: "var(--color-dark)",
          borderColor: "rgba(255,255,255,0.1)",
          color: "var(--color-light)",
        }}
      >
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          <h2 className="font-medium text-base">Record Attendance</h2>
          <button
            onClick={onClose}
            disabled={isSubmitting}
            className="opacity-60 hover:opacity-100"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 space-y-3">
          <div>
            <p className="text-xs opacity-60 mb-1">Student Name</p>
            <p className="border border-white/10 rounded-md p-2 text-sm">
              {scanResult.userName}
            </p>
          </div>

          <div>
            <p className="text-xs opacity-60 mb-1">Hours Attended *</p>
            <select
              value={hours}
              onChange={(e) =>
                setHours(e.target.value ? Number(e.target.value) : "")
              }
              disabled={isSubmitting}
              className="w-full bg-transparent border border-white/10 rounded-md p-2 text-sm outline-none"
            >
              <option value="">Select hours</option>
              {Array.from({ length: 8 }, (_, i) => i + 1).map((h) => (
                <option key={h} value={h} className="bg-[var(--color-dark)]">
                  {h} {h === 1 ? "hour" : "hours"}
                </option>
              ))}
            </select>
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={onClose}
              disabled={isSubmitting}
              className="flex-1 border border-white/10 rounded-md py-2 text-sm opacity-80 hover:opacity-100"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              disabled={isSubmitting || !hours}
              className="flex-1 rounded-md py-2 text-sm font-medium border border-white/20 bg-white/10 hover:bg-white/20 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Submitting
                </>
              ) : (
                "Submit"
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
