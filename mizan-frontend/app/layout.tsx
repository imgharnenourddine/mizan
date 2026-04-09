// Root layout — wraps the entire app with global fonts, providers, and metadata
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mizan — ميزان",
  description: "L'agent IA de bien-être étudiant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
