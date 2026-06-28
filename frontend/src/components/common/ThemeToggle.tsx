import { Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useAppStore } from "@/store/appStore";

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useAppStore();
  return (
    <Button variant="secondary" size="icon" onClick={toggleTheme} aria-label="Toggle theme">
      {theme === "dark" ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
    </Button>
  );
};
