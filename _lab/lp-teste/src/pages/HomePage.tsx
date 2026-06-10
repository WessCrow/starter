import Hero from "@/modules/landing/components/Hero";
import Beneficios from "@/modules/landing/components/Beneficios";
import ComoFunciona from "@/modules/landing/components/ComoFunciona";
import Depoimentos from "@/modules/landing/components/Depoimentos";
import CtaFinal from "@/modules/landing/components/CtaFinal";
import Footer from "@/modules/landing/components/Footer";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-leaf-50 text-leaf-900">
      <Hero />
      <Beneficios />
      <ComoFunciona />
      <Depoimentos />
      <CtaFinal />
      <Footer />
    </main>
  );
}
