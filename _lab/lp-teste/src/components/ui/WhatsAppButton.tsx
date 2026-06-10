import { whatsappUrl } from "@/utils/whatsapp";

interface WhatsAppButtonProps {
  label: string;
  message: string;
  variant?: "solid" | "outline";
}

export default function WhatsAppButton({ label, message, variant = "solid" }: WhatsAppButtonProps) {
  const base =
    "inline-flex items-center gap-2 rounded-full px-6 py-3 text-base font-semibold transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-leaf-700";
  const styles =
    variant === "solid"
      ? "bg-leaf-600 text-white hover:bg-leaf-700"
      : "border-2 border-leaf-600 text-leaf-700 hover:bg-leaf-100";

  return (
    <a href={whatsappUrl(message)} target="_blank" rel="noopener noreferrer" className={`${base} ${styles}`}>
      <span aria-hidden="true">💬</span>
      {label}
    </a>
  );
}
