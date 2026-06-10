const DEPOIMENTOS = [
  {
    nome: "Mariana S.",
    texto:
      "Em dois meses perdi 6 kg sem passar fome. O plano cabia na minha rotina de mãe e CLT."
  },
  {
    nome: "Ricardo L.",
    texto:
      "Parei de viver de dieta maluca. Hoje como melhor, treino com energia e não tenho culpa no domingo."
  },
  {
    nome: "Camila F.",
    texto:
      "O acompanhamento pelo WhatsApp fez diferença. Quando travava, recebia ajuste no mesmo dia."
  }
];

export default function Depoimentos() {
  return (
    <section className="bg-leaf-50 px-6 py-20" aria-labelledby="depoimentos-titulo">
      <div className="mx-auto max-w-5xl">
        <h2
          id="depoimentos-titulo"
          className="text-center text-3xl font-bold text-leaf-900 md:text-4xl"
        >
          O que dizem nossos clientes
        </h2>
        <div className="mt-12 grid gap-8 md:grid-cols-3">
          {DEPOIMENTOS.map((d) => (
            <article
              key={d.nome}
              className="rounded-2xl border border-leaf-200 bg-white p-8 shadow-sm"
            >
              <p className="text-leaf-900/85 leading-relaxed">&ldquo;{d.texto}&rdquo;</p>
              <p className="mt-4 font-semibold text-leaf-700">{d.nome}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
