const PASSOS = [
  { numero: "1", titulo: "Conversa inicial", descricao: "Você conta sua rotina, objetivos e dificuldades pelo WhatsApp." },
  { numero: "2", titulo: "Plano personalizado", descricao: "Em até 3 dias úteis você recebe seu plano alimentar completo." },
  { numero: "3", titulo: "Acompanhamento", descricao: "Consultas online quinzenais para ajustar o plano e manter o ritmo." }
];

export default function ComoFunciona() {
  return (
    <section className="px-6 py-20">
      <div className="mx-auto max-w-4xl">
        <h2 className="text-center text-3xl font-bold md:text-4xl">Como funciona</h2>
        <ol className="mt-12 space-y-8">
          {PASSOS.map((p) => (
            <li key={p.numero} className="flex items-start gap-6">
              <span
                aria-hidden="true"
                className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-leaf-600 text-xl font-bold text-white"
              >
                {p.numero}
              </span>
              <div>
                <h3 className="text-xl font-semibold">{p.titulo}</h3>
                <p className="mt-1 text-leaf-900/80">{p.descricao}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
