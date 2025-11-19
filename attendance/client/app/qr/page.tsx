"use client";
import { useEffect, useRef, useState, useCallback } from "react";
import jsQR from "jsqr";
import { Camera, Loader2 } from "lucide-react";
import { jwtDecoder } from "@/utils/jwtDecoder";
import { toast } from "sonner";
import { jwtFormat } from "@/utils/jwtFormat";
import { ChoiceModal } from "@/components/ChoiceModal";
import { AttendanceModal } from "@/components/AttendanceModal";
import { useRouter } from "next/navigation";
import { useToken } from "@/context/TokenContext";

type ScanResult = {
  token: string;
  userName: string;
};

const Page = () => {
  const router = useRouter();
  const { setToken } = useToken();
  const [scanning, setScanning] = useState(false);
  const [showChoiceModal, setShowChoiceModal] = useState(false);
  const [showAttendanceModal, setShowAttendanceModal] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [cameraReady, setCameraReady] = useState(false);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const intervalRef = useRef<number | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const stopCamera = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) videoRef.current.srcObject = null;
    setCameraReady(false);
  }, []);

  const tick = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || scanning) return;

    const context = canvas.getContext("2d");
    if (!context || video.readyState !== video.HAVE_ENOUGH_DATA) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height);
    if (!code || !code.data) return;

    setScanning(true);
    clearInterval(intervalRef.current || undefined);
    video.pause();

    try {
      if (!jwtFormat(code.data)) {
        toast.warning("Invalid token: missing user info.", { duration: 1200 });
        setScanning(false);
        video.play().catch(() => {});
        return;
      }

      const decodedToken = jwtDecoder(code.data);
      if (!decodedToken?.fullname) {
        toast.warning("Invalid token: missing user info.", {
          duration: 1200,
        });
        setScanning(false);
        video.play().catch(() => {});
        return;
      }

      // ✅ teacher detection: set token in memory and redirect
      if (decodedToken.type === "TEACHER") {
        toast.success(`Greetings ${decodedToken.fullname}`, { duration: 1200 });
        setToken(code.data); // store token in memory context
        router.push(`/admin/`);
        return;
      }

      // student flow
      setScanResult({ token: code.data, userName: decodedToken.fullname });
      setShowChoiceModal(true);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to decode QR code";
      toast.error(message, { duration: 1200 });
      video.play().catch(() => {});
      setTimeout(() => setScanning(false), 1201);
    }
  }, [scanning, setToken, router]);

  const startCamera = useCallback(async () => {
    try {
      setCameraError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current?.play();
          setCameraReady(true);
          intervalRef.current = window.setInterval(tick, 200);
        };
      }
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Cannot access camera";
      console.error("Camera error:", error);
      setCameraError(message);
    }
  }, [tick]);

  useEffect(() => {
    startCamera();
    return stopCamera;
  }, [startCamera, stopCamera]);

  const handleRetryCamera = () => {
    stopCamera();
    startCamera();
  };

  const handleChoiceClose = () => {
    setShowChoiceModal(false);
    setScanResult(null);
    setScanning(false);
    if (videoRef.current) {
      videoRef.current.play().catch(() => {});
      intervalRef.current = window.setInterval(tick, 200);
    }
  };

  return (
    <section
      className="min-h-screen flex flex-col items-center justify-center px-4 py-8"
      style={{
        backgroundColor: "var(--color-dark)",
        color: "var(--color-light)",
      }}
    >
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Camera className="w-10 h-10 mx-auto mb-3 opacity-70" />
          <h1 className="text-2xl font-semibold mb-1">Library Attendance</h1>
          <p className="opacity-50 text-sm">
            Scan a QR code to record attendance
          </p>
        </div>

        <div
          className="relative w-full aspect-[4/3] rounded-lg overflow-hidden border"
          style={{
            borderColor: "rgba(255,255,255,0.1)",
            backgroundColor: "rgba(255,255,255,0.03)",
          }}
        >
          {cameraError ? (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6">
              <p className="mb-4 opacity-80">{cameraError}</p>
              <button
                onClick={handleRetryCamera}
                className="px-5 py-2 rounded-md text-sm font-medium border"
                style={{
                  borderColor: "rgba(255,255,255,0.2)",
                  backgroundColor: "transparent",
                }}
              >
                Retry Camera
              </button>
            </div>
          ) : (
            <>
              <video
                ref={videoRef}
                playsInline
                muted
                className="w-full h-full object-cover transform -scale-x-110"
              />
              <canvas ref={canvasRef} className="hidden" />
              {!cameraReady && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <Loader2 className="w-6 h-6 animate-spin opacity-60" />
                </div>
              )}
              {scanning && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                  <Loader2 className="w-5 h-5 animate-spin opacity-80" />
                </div>
              )}
            </>
          )}
        </div>

        {cameraReady && !scanning && (
          <div className="text-center mt-4 opacity-70 text-sm">
            Ready to scan
          </div>
        )}
      </div>

      {/* Choice Modal */}
      {showChoiceModal && scanResult && (
        <ChoiceModal
          onSelectReturn={() => {
            window.location.href = `/return/${scanResult.token}`;
          }}
          scanResult={scanResult}
          onSelectAttendance={() => {
            setShowChoiceModal(false);
            setShowAttendanceModal(true);
          }}
          onSelectBorrow={() => {
            window.location.href = `/borrow/${scanResult.token}`;
          }}
          onClose={handleChoiceClose}
        />
      )}

      {/* Attendance Modal */}
      {showAttendanceModal && scanResult && (
        <AttendanceModal
          scanResult={scanResult}
          onClose={() => setShowAttendanceModal(false)}
          onComplete={() => setScanning(false)}
        />
      )}
    </section>
  );
};

export default Page;
