import WhatsAppButton from "@/components/ui/WhatsAppButton";

export default function CtaFinal() {
  return (
    <section className="bg-leaf-700 px-6 py-20 text-center text-white">
      <div className="mx-auto max-w-2xl">
        <h2 className="text-3xl font-bold md:text-4xl">Pronta(o) para começar?</h2>
        <p className="mt-4 text-lg text-leaf-100">
          A primeira conversa é gratuita e sem compromisso. Me chama no WhatsApp
          e vamos montar um plano que cabe na sua vida.
        </p>
        <div className="mt-8">
          <WhatsAppButton
            label="Começar agora"
            message="Olá! Quero agendar minha conversa gratuita com a NutriLeve."
          />
        </div>
      </div>
    </section>
  );
}
