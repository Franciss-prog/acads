"use client";
import { useRouter } from "next/router";
import { useParams } from "next/navigation";
import { CheckQrCodeFormat } from "@/utils/qrCodeFormat";
import { toast } from "sonner";
import { jwtDecoder } from "@/utils/jwtDecoder";
import { useState, useEffect } from "react";
// !make sure that only teacher can access this page
const page = () => {
  // params handler
  const router = useRouter();
  const params = useParams();
  const teacher = params.teacher as string;

  // trigger this when open the page
  useEffect(() => {}, [params]);
  // states to store the temp Data
  const [fullName, setFullName] = useState<string | null>("");
  console.log(fullName);
  // validate the token is valid
  if (!CheckQrCodeFormat(teacher)) {
    toast.error("Invalid token");
    setTimeout(() => router.push("/"), 1200);
    return;
  }

  //decode the token based on params given
  const decode = jwtDecoder(teacher);

  // check if the token type is teacher
  if (decode?.type !== "teacher") {
    toast.error("You are not a Librarian");
    setTimeout(() => router.push("/qr"), 1200);
    return;
  }
  // set the states defined earlier
  setFullName(decode?.fullname as string);

  //
  return <div></div>;
};

export default page;
