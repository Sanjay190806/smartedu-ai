export const PageShell = ({ title, description, children }: { title: string; description: string; children: React.ReactNode }) => (
  <main className="mx-auto w-full max-w-7xl px-4 py-6 lg:px-8">
    <div className="mb-6">
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-primary">SmartEdu AI</p>
      <h2 className="mt-2 text-3xl font-bold tracking-tight">{title}</h2>
      <p className="mt-2 max-w-3xl text-muted-foreground">{description}</p>
    </div>
    {children}
  </main>
);
