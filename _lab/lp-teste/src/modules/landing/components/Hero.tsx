import WhatsAppButton from "@/components/ui/WhatsAppButton";

export default function Hero() {
  return (
    <section className="px-6 pb-20 pt-24 text-center md:pt-32">
      <div className="mx-auto max-w-3xl">
        <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-leaf-600">
          Consultoria de nutrição online
        </p>
        <h1 className="text-4xl font-bold leading-tight md:text-6xl">
          Comer bem pode ser <span className="text-leaf-600">leve</span>
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-lg text-leaf-900/80">
          Sem dietas malucas e sem terrorismo nutricional. Um plano alimentar
          feito para a sua rotina, com acompanhamento de verdade.
        </p>
        <div className="mt-10">
          <WhatsAppButton
            label="Falar com a nutricionista"
            message="Olá! Vi o site da NutriLeve e quero saber mais sobre a consultoria."
          />
        </div>
      </div>
    </section>
  );
}
