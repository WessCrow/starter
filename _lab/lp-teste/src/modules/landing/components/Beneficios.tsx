const BENEFICIOS = [
  {
    titulo: "Plano sob medida",
    descricao: "Nada de cardápio genérico: o plano considera sua rotina, preferências e orçamento."
  },
  {
    titulo: "Acompanhamento contínuo",
    descricao: "Ajustes quinzenais e suporte direto pelo WhatsApp durante todo o processo."
  },
  {
    titulo: "Sem proibições",
    descricao: "Reeducação alimentar com equilíbrio — a pizza de domingo continua existindo."
  }
];

export default function Beneficios() {
  return (
    <section className="bg-white px-6 py-20">
      <div className="mx-auto max-w-5xl">
        <h2 className="text-center text-3xl font-bold md:text-4xl">Por que a NutriLeve?</h2>
        <div className="mt-12 grid gap-8 md:grid-cols-3">
          {BENEFICIOS.map((b) => (
            <article key={b.titulo} className="rounded-2xl bg-leaf-50 p-8">
              <h3 className="text-xl font-semibold text-leaf-700">{b.titulo}</h3>
              <p className="mt-3 text-leaf-900/80">{b.descricao}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
