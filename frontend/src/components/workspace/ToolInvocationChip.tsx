import React from 'react';
import { Database, Sliders, ShieldCheck, CheckCircle2, Loader2, Terminal } from 'lucide-react';
import type { ToolCallItem } from '../../types/agent';

interface ToolInvocationChipProps {
  tool: ToolCallItem;
}

export const ToolInvocationChip: React.FC<ToolInvocationChipProps> = ({ tool }) => {
  const getToolIcon = (name: string) => {
    if (name.includes('catalogue') || name.includes('query')) return <Database className="w-3.5 h-3.5 text-blue-500" />;
    if (name.includes('fuzzy') || name.includes('score')) return <Sliders className="w-3.5 h-3.5 text-purple-500" />;
    if (name.includes('safety')) return <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />;
    return <Terminal className="w-3.5 h-3.5 text-amber-500" />;
  };

  return (
    <div className="my-1.5 border border-border/70 rounded-md bg-card text-card-foreground text-xs shadow-xs overflow-hidden">
      <div className="flex items-center justify-between px-2.5 py-1.5">
        <div className="flex items-center gap-2">
          {getToolIcon(tool.toolName)}
          <span className="font-mono font-medium text-foreground/90">{tool.toolName}</span>
          <span className="text-muted-foreground text-[11px] hidden sm:inline truncate max-w-[200px]">
            {tool.label}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {tool.status === 'running' ? (
            <span className="inline-flex items-center gap-1 text-[10px] text-primary px-1.5 py-0.5 rounded bg-primary/10 font-medium">
              <Loader2 className="w-3 h-3 animate-spin" />
              Executing
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 text-[10px] text-emerald-600 dark:text-emerald-400 px-1.5 py-0.5 rounded bg-emerald-500/10 font-medium">
              <CheckCircle2 className="w-3 h-3" />
              {tool.executionTimeMs ? `${tool.executionTimeMs}ms` : 'Completed'}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
