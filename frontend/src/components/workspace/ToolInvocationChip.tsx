import React, { useState } from 'react';
import { Database, Sliders, ShieldCheck, CheckCircle2, Loader2, ChevronDown, ChevronRight, Terminal } from 'lucide-react';
import type { ToolCallItem } from '../../types/agent';

interface ToolInvocationChipProps {
  tool: ToolCallItem;
}

export const ToolInvocationChip: React.FC<ToolInvocationChipProps> = ({ tool }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getToolIcon = (name: string) => {
    if (name.includes('catalogue') || name.includes('query')) return <Database className="w-3.5 h-3.5 text-blue-500" />;
    if (name.includes('fuzzy') || name.includes('score')) return <Sliders className="w-3.5 h-3.5 text-purple-500" />;
    if (name.includes('safety')) return <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />;
    return <Terminal className="w-3.5 h-3.5 text-amber-500" />;
  };

  return (
    <div className="my-1.5 border border-border/70 rounded-md bg-card text-card-foreground text-xs shadow-xs overflow-hidden">
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between px-2.5 py-1.5 cursor-pointer hover:bg-muted/40 transition-colors select-none"
      >
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
          {isExpanded ? <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" /> : <ChevronRight className="w-3.5 h-3.5 text-muted-foreground" />}
        </div>
      </div>

      {isExpanded && (
        <div className="p-2.5 bg-muted/20 border-t border-border/50 text-[11px] font-mono space-y-2">
          {tool.inputParams && (
            <div>
              <div className="text-muted-foreground text-[10px] uppercase font-semibold mb-0.5">Parameters:</div>
              <pre className="bg-background/80 p-2 rounded border border-border/40 overflow-x-auto text-foreground/80">
                {JSON.stringify(tool.inputParams, null, 2)}
              </pre>
            </div>
          )}

          {tool.outputResult && (
            <div>
              <div className="text-muted-foreground text-[10px] uppercase font-semibold mb-0.5">Result Payload:</div>
              <pre className="bg-background/80 p-2 rounded border border-border/40 overflow-x-auto text-emerald-600 dark:text-emerald-400">
                {typeof tool.outputResult === 'string'
                  ? tool.outputResult
                  : JSON.stringify(tool.outputResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
