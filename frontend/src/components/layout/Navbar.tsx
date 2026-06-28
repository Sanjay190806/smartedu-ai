import { Link } from "react-router-dom";
import { BrainCircuit, ExternalLink } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/common/ThemeToggle";

export const Navbar = () => (
  <header className="fixed inset-x-0 top-0 z-40 border-b border-white/10 bg-background/70 backdrop-blur-xl">
    <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <Link to="/" className="flex items-center gap-3 font-bold">
        <span className="grid h-9 w-9 place-items-center rounded-xl bg-primary text-primary-foreground">
          <BrainCircuit className="h-5 w-5" />
        </span>
        SmartEdu AI
      </Link>
      <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
        <Link to="/about" className="hover:text-foreground">About</Link>
        <Link to="/privacy" className="hover:text-foreground">Privacy</Link>
        <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 hover:text-foreground">
          API Docs <ExternalLink className="h-3 w-3" />
        </a>
      </nav>
      <div className="flex items-center gap-2">
        <ThemeToggle />
        <Button asChild>
          <Link to="/login">Get Started</Link>
        </Button>
      </div>
    </div>
  </header>
);
