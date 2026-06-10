export default function Footer() {
  return (
    <footer className="bg-leaf-900 px-6 py-8 text-center text-sm text-leaf-100">
      <p>NutriLeve © {new Date().getFullYear()} — Consultoria de nutrição online.</p>
      <p className="mt-1 text-leaf-300">Conteúdo informativo. Não substitui avaliação individual.</p>
    </footer>
  );
}
