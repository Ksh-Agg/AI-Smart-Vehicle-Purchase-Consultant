import React from 'react';
import type { ConsultationSession, UserPreferenceProfile } from '../../types/agent';
import {
  Plus,
  Car,
  DollarSign,
  Fuel,
  Shield,
  Sun,
  Moon,
  ChevronLeft,
  ChevronRight,
  Sliders,
} from 'lucide-react';
import { Button } from '../ui/button';

interface SidebarProps {
  sessions: ConsultationSession[];
  activeSessionId: string;
  onSelectSession: (id: string) => void;
  onNewSession: () => void;
  profile: UserPreferenceProfile;
  onOpenProfileTuner: () => void;
  isDark: boolean;
  onToggleTheme: () => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewSession,
  profile,
  onOpenProfileTuner,
  isDark,
  onToggleTheme,
  isCollapsed,
  onToggleCollapse,
}) => {
  if (isCollapsed) {
    return (
      <div className="flex flex-col items-center justify-between py-4 px-2 w-14 border-r border-border bg-card/50 h-full shrink-0">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary text-primary-foreground flex items-center justify-center font-bold">
            <Car className="w-4 h-4" />
          </div>
          <Button
            size="icon-xs"
            variant="outline"
            onClick={onNewSession}
            title="New Consultation"
            className="rounded-lg"
          >
            <Plus className="w-3.5 h-3.5" />
          </Button>
          <Button
            size="icon-xs"
            variant="ghost"
            onClick={onOpenProfileTuner}
            title="Intake Tuner"
            className="rounded-lg"
          >
            <Sliders className="w-3.5 h-3.5" />
          </Button>
        </div>

        <div className="flex flex-col items-center gap-2">
          <Button
            size="icon-xs"
            variant="ghost"
            onClick={onToggleTheme}
            title="Toggle theme (Hotkey: D)"
          >
            {isDark ? <Sun className="w-3.5 h-3.5" /> : <Moon className="w-3.5 h-3.5" />}
          </Button>
          <Button
            size="icon-xs"
            variant="ghost"
            onClick={onToggleCollapse}
            title="Expand sidebar"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col justify-between w-64 border-r border-border bg-card/60 backdrop-blur-md h-full shrink-0 text-xs">
      {/* Brand & New Consultation Header */}
      <div className="p-3.5 border-b border-border space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-primary text-primary-foreground flex items-center justify-center font-extrabold text-xs shadow-xs">
              <Car className="w-3.5 h-3.5" />
            </div>
            <div>
              <h1 className="font-bold text-foreground tracking-tight text-xs">SVPC Workspace</h1>
              <p className="text-[10px] text-muted-foreground font-mono">Agent v2.4 • LangGraph</p>
            </div>
          </div>

          <Button
            size="icon-xs"
            variant="ghost"
            onClick={onToggleCollapse}
            className="text-muted-foreground hover:text-foreground"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </Button>
        </div>

        <Button
          size="sm"
          onClick={onNewSession}
          className="w-full gap-1.5 text-xs bg-primary text-primary-foreground hover:bg-primary/90 rounded-lg shadow-xs"
        >
          <Plus className="w-3.5 h-3.5" />
          New Consultation
        </Button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        <div className="px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground font-mono">
          Consultation Sessions
        </div>

        {sessions.map((sess) => {
          const isActive = sess.id === activeSessionId;
          return (
            <button
              key={sess.id}
              type="button"
              onClick={() => onSelectSession(sess.id)}
              className={`w-full text-left p-2 rounded-lg transition-all border flex flex-col gap-1 ${
                isActive
                  ? 'bg-primary/10 border-primary/30 text-foreground font-medium shadow-2xs'
                  : 'border-transparent text-muted-foreground hover:bg-muted/60 hover:text-foreground'
              }`}
            >
              <div className="flex items-center justify-between w-full">
                <span className="truncate font-semibold text-xs text-foreground">
                  {sess.title}
                </span>
                <span className="text-[10px] font-mono text-muted-foreground">{sess.date}</span>
              </div>
              <p className="text-[11px] text-muted-foreground line-clamp-1">
                {sess.lastMessageSnippet}
              </p>
            </button>
          );
        })}
      </div>

      {/* Live User Profile Snippet */}
      <div className="p-3 border-t border-border bg-muted/20 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground font-mono">
            Active Profile
          </span>
          <button
            onClick={onOpenProfileTuner}
            className="text-[10px] text-primary hover:underline flex items-center gap-0.5"
          >
            <span>Edit</span>
          </button>
        </div>

        <div className="p-2 rounded-lg bg-card border border-border/70 space-y-1.5 text-[11px]">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="flex items-center gap-1">
              <DollarSign className="w-3 h-3 text-emerald-500" /> Ceiling:
            </span>
            <span className="font-mono font-semibold text-foreground">
              ${profile.budgetMax.toLocaleString()}
            </span>
          </div>

          <div className="flex items-center justify-between text-muted-foreground">
            <span className="flex items-center gap-1">
              <Fuel className="w-3 h-3 text-blue-500" /> Powertrain:
            </span>
            <span className="font-semibold text-foreground truncate max-w-[100px]">
              {profile.preferredPowertrains.join(', ')}
            </span>
          </div>

          <div className="flex items-center justify-between text-muted-foreground">
            <span className="flex items-center gap-1">
              <Shield className="w-3 h-3 text-purple-500" /> Priority:
            </span>
            <span className="font-semibold text-foreground">Safety (High)</span>
          </div>
        </div>
      </div>

      {/* Theme Switcher & Footer */}
      <div className="p-3 border-t border-border flex items-center justify-between bg-card">
        <button
          onClick={onToggleTheme}
          className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
          title="Toggle theme (Hotkey: D)"
        >
          {isDark ? <Sun className="w-3.5 h-3.5 text-amber-400" /> : <Moon className="w-3.5 h-3.5 text-blue-500" />}
          <span className="text-[11px] font-medium">{isDark ? 'Light' : 'Dark'}</span>
          <kbd className="px-1.5 py-0.2 rounded bg-muted text-[10px] font-mono border border-border/80 text-muted-foreground">
            D
          </kbd>
        </button>

        <span className="text-[10px] font-mono text-muted-foreground">SVPC Monorepo</span>
      </div>
    </div>
  );
};
