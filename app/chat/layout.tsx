'use client';

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppSidebar } from "./components/sidebar/app-sidebar";
import { ThemeProvider } from "next-themes";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { ThemeSwitcher } from '@/components/theme-switcher';
import AuthButton from '@/components/header-auth';

export default function ChatLayout({ children }: Readonly<{
  children: React.ReactNode;
}>) {
  const [queryClient] = useState(() => new QueryClient());
  
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
              <header className="flex justify-between items-center h-16 shrink-0 px-4">
                <SidebarTrigger className="-ml-1" />
                <div className="flex items-center gap-3 pr-4">
                  <ThemeSwitcher />
                  <AuthButton />
                </div>
              </header>
              <div className="flex h-[calc(100vh-4rem)] w-full overflow-hidden">
                <div className="flex-1 h-full w-full overflow-hidden">
                  {children}
                </div>
              </div>
            </SidebarInset>
        </SidebarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
