const DEFAULT_NUMBER = "5511999999999";

export function whatsappUrl(message: string): string {
  const number = import.meta.env.VITE_WHATSAPP_NUMBER ?? DEFAULT_NUMBER;
  return `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
}
