"use client";
import { X } from "lucide-react";

type ScanResult = {
  token: string;
  userName: string;
};

type ChoiceModalProps = {
  scanResult: ScanResult;
  onSelectAttendance: () => void;
  onSelectBorrow: () => void;
  onSelectReturn: () => void;
  onClose: () => void;
};

export const ChoiceModal = ({
  scanResult,
  onSelectAttendance,
  onSelectBorrow,
  onSelectReturn,
  onClose,
}: ChoiceModalProps) => {
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
          <h2 className="font-medium text-base">
            Hello, {scanResult.userName}
          </h2>
          <button onClick={onClose} className="opacity-60 hover:opacity-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 space-y-4">
          <p className="text-sm opacity-70">What would you like to do?</p>
          <div className="flex flex-col gap-3">
            <button
              onClick={onSelectAttendance}
              className="w-full rounded-md py-2 text-sm font-medium border border-white/10 bg-white/10 hover:bg-white/20"
            >
              Record Attendance
            </button>
            <button
              onClick={onSelectBorrow}
              className="w-full rounded-md py-2 text-sm font-medium border border-white/10 bg-white/10 hover:bg-white/20"
            >
              Borrow Book
            </button>
            <button
              onClick={onSelectReturn}
              className="w-full rounded-md py-2 text-sm font-medium border border-white/10 bg-white/10 hover:bg-white/20"
            >
              Return Book
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
