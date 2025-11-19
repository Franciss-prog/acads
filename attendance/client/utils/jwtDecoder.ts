import { jwtDecode } from "jwt-decode";
// Define your actual token shape
export interface MyToken {
  srcode: string;
  fullname: string;
  type: string;
  exp?: number;
  iat?: number;
}
export const jwtDecoder = (token: string): MyToken | null => {
  try {
    return jwtDecode<MyToken>(token);
  } catch (e) {
    console.error("Invalid token:", e);
    return null;
  }
};
