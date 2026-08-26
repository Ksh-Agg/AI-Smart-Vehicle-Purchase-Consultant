import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Sparkles, Brain } from 'lucide-react';
import type { ThinkingState } from '../../types/agent';

interface ThinkingBlockProps {
  thinking: ThinkingState;
}

export const ThinkingBlock: React.FC<ThinkingBlockProps> = ({ thinking }) => {
  const [isOpen, setIsOpen] = useState(thinking.isThinking);

  return (
    <div className="my-2 border border-border/80 rounded-lg bg-muted/30 overflow-hidden transition-all">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3 py-2 text-xs text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          {thinking.isThinking ? (
            <div className="relative flex items-center justify-center">
              <span className="animate-ping absolute inline-flex h-2.5 w-2.5 rounded-full bg-primary opacity-75" />
              <Brain className="w-3.5 h-3.5 text-primary animate-pulse relative" />
            </div>
          ) : (
            <Sparkles className="w-3.5 h-3.5 text-muted-foreground" />
          )}
          <span className="font-medium tracking-tight">
            {thinking.isThinking ? 'Agent Deliberating & Reasoning...' : 'Reasoning Process'}
          </span>
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground border border-border/60">
            {thinking.thoughts.length} step{thinking.thoughts.length !== 1 ? 's' : ''}
            {thinking.durationSeconds > 0 ? ` • ${thinking.durationSeconds}s` : ''}
          </span>
        </div>
        <div className="flex items-center gap-1 text-[11px]">
          <span>{isOpen ? 'Hide' : 'Inspect'}</span>
          {isOpen ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
        </div>
      </button>

      {isOpen && (
        <div className="px-3 pb-3 pt-1 border-t border-border/50 bg-background/50 space-y-1.5 text-xs font-mono">
          {thinking.thoughts.map((thought, idx) => (
            <div key={idx} className="flex items-start gap-2 text-muted-foreground leading-relaxed">
              <span className="text-primary/70 font-semibold select-none">[{idx + 1}]</span>
              <span className="text-foreground/80">{thought}</span>
            </div>
          ))}
          {thinking.isThinking && (
            <div className="flex items-center gap-2 text-primary text-[11px] pt-1">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-primary animate-ping" />
              <span>Evaluating multi-attribute trade-offs & fuzzy constraints...</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
