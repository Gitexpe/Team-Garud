
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Menu, Search, Upload, Bell, Settings } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { SidebarTrigger } from "@/components/ui/sidebar";

export const Header = () => {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <header className="fixed top-0 left-0 right-0 bg-card border-b h-16 z-50 flex items-center px-4">
      <div className="flex items-center md:w-64">
        <SidebarTrigger>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        </SidebarTrigger>
        <Link to="/" className="hidden md:block">
          <h1 className="text-xl font-bold text-primary">
            CallScribe Analyzer
          </h1>
        </Link>
      </div>

      <div className="flex-1 px-4">
        <div className="relative max-w-md">
          <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search recordings..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-8 bg-muted"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          asChild
          className="hidden sm:flex items-center gap-1"
        >
          <Link to="/upload">
            <Upload className="h-4 w-4" />
            <span>Upload</span>
          </Link>
        </Button>
        <Button variant="ghost" size="icon">
          <Bell className="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon">
          <Settings className="h-5 w-5" />
        </Button>
      </div>
    </header>
  );
};
