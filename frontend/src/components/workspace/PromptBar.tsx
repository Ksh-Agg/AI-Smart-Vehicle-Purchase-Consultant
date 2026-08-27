import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Sparkles, SlidersHorizontal, Car, Shield, IndianRupee } from 'lucide-react';
import { Button } from '../ui/button';

interface PromptBarProps {
  onSubmit: (prompt: string) => void;
  isStreaming: boolean;
}

const QUICK_SUGGESTIONS = [
  {
    icon: <Car className="w-3 h-3 text-amber-500" />,
    label: 'Family car in Pune',
    prompt: 'Recommend a safe Maruti family car in Pune under ₹12 lakh on-road with good boot space.',
  },
  {
    icon: <Car className="w-3 h-3 text-blue-500" />,
    label: 'Baleno vs Swift',
    prompt: 'Compare the current Maruti Baleno and Swift variants for city use, safety, efficiency, and five-year ownership cost in Delhi.',
  },
  {
    icon: <IndianRupee className="w-3 h-3 text-emerald-500" />,
    label: '5-Year Cost of Ownership',
    prompt: 'Calculate the five-year ownership cost for my shortlist, showing fuel, maintenance, insurance, finance, and resale evidence gaps.',
  },
  {
    icon: <Shield className="w-3 h-3 text-purple-500" />,
    label: 'Safety-first shortlist',
    prompt: 'Recommend Maruti variants under ₹15 lakh on-road in Bengaluru, prioritizing verified Bharat NCAP applicability and safety equipment.',
  },
];

export const PromptBar: React.FC<PromptBarProps> = ({ onSubmit, isStreaming }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [input]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || isStreaming) return;
    onSubmit(input);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full space-y-2">
      {/* Quick Suggestion Pills */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
        <span className="text-[11px] text-muted-foreground font-medium flex items-center gap-1 shrink-0">
          <Sparkles className="w-3 h-3 text-primary" /> Suggestions:
        </span>
        {QUICK_SUGGESTIONS.map((item, i) => (
          <button
            key={i}
            type="button"
            onClick={() => onSubmit(item.prompt)}
            disabled={isStreaming}
            className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-muted/60 hover:bg-muted text-foreground/80 hover:text-foreground text-[11px] font-medium transition-colors border border-border/50 shrink-0 disabled:opacity-50"
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      {/* Main Composer Box */}
      <div className="relative rounded-2xl border border-border bg-card/90 shadow-sm focus-within:ring-2 focus-within:ring-ring/40 focus-within:border-primary transition-all p-2.5">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Tell me your city, on-road budget, usage, and priorities..."
          rows={1}
          disabled={isStreaming}
          className="w-full resize-none bg-transparent text-sm text-foreground placeholder:text-muted-foreground/70 focus:outline-hidden max-h-32 leading-relaxed px-1 py-0.5"
        />

        <div className="flex items-center justify-between pt-2 mt-1 border-t border-border/40">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-muted text-[11px] font-mono text-muted-foreground border border-border/60">
              <SlidersHorizontal className="w-3 h-3 text-primary" />
              <span>SVPC AutoAgent v2 (LangGraph)</span>
            </span>
            <span className="text-[11px] text-muted-foreground hidden sm:inline">
              Shift + Enter for new line
            </span>
          </div>

          <Button
            type="button"
            size="icon-sm"
            onClick={() => handleSubmit()}
            disabled={!input.trim() || isStreaming}
            className="rounded-full h-7 w-7 bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-30 transition-transform active:scale-95"
          >
            {isStreaming ? (
              <span className="w-3.5 h-3.5 rounded-full border-2 border-primary-foreground/30 border-t-primary-foreground animate-spin" />
            ) : (
              <ArrowUp className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};
