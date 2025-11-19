export const CheckQrCodeFormat = (qrCode: string) => {
  return /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]{43}$/.test(qrCode);
};
