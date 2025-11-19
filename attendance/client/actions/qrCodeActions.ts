import { toast } from "sonner";
import axios from "axios";

interface AttendanceData {
  token: string;
  hours: number;
}
export const postAttendance = async (token: string, hours: number) => {
  if (!token) {
    toast.warning("Missing QR token.");
    return;
  }

  const attendanceData: AttendanceData = { token, hours };

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/attendance",
      attendanceData,
    );

    toast.success(response.data.message || "Attendance recorded successfully.");
    return response.data;
  } catch (err: any) {
    if (axios.isAxiosError(err) && err.response) {
      // Extract detail if it exists
      const detail = err.response.data?.detail || err.response.data;
      toast.warning(detail);
      console.log("Error response:", err.response.data);
    } else {
      toast.error("Something went wrong. Please try again.");
      console.error(err);
    }
  }
};
