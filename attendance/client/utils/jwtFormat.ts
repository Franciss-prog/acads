import { jwtDecoder } from "./jwtDecoder";
import { toast } from "sonner";
import { CheckQrCodeFormat } from "./qrCodeFormat";

export const jwtFormat = (token: string): boolean => {
  if (!token || !CheckQrCodeFormat(token)) {
    toast.error("Invalid token");
    return false;
  }

  const decoded = jwtDecoder(token);

  // deconstruct with optional chaining
  const fullname = decoded?.fullname;
  const type = decoded?.type;
  const srcode = decoded?.srcode;

  // validate the decoded payload
  if (
    !decoded ||
    typeof fullname !== "string" ||
    typeof type !== "string" ||
    typeof srcode !== "string"
  ) {
    toast.error("Invalid Qr Code");
    return false;
  }

  return true;
};
