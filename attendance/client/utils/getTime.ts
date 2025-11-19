import { toast } from "sonner";

export const isTheLibraryOpen = (): boolean => {
  const now = new Date();
  const currentTime = now.getHours() * 100 + now.getMinutes(); // e.g., 12:30 -> 1230

  const openingTime = 800; // 08:00
  const closingTime = 1700; // 17:00
  const lunchStart = 1200; // 12:00
  const lunchEnd = 1300; // 13:00

  if (currentTime < openingTime) {
    toast.warning("Library is not opened yet.");
    return false;
  }

  if (currentTime >= closingTime) {
    toast.warning("Library is closed.");
    return false;
  }

  if (currentTime >= lunchStart && currentTime < lunchEnd) {
    toast.warning("Library is closed for lunch.");
    return false;
  }

  return true;
};
