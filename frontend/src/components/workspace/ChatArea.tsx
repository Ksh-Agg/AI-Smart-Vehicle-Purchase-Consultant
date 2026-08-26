import React, { useRef, useEffect } from 'react';
import type { ChatMessage } from '../../types/agent';
import { ThinkingBlock } from './ThinkingBlock';
import { ToolInvocationChip } from './ToolInvocationChip';
import { ApprovalCard } from './ApprovalCard';
import { PromptBar } from './PromptBar';
import { Bot, User, Car, Sparkles } from 'lucide-react';
import { Badge } from '../ui/badge';

interface ChatAreaProps {
  messages: ChatMessage[];
  isStreaming: boolean;
  onSubmitPrompt: (prompt: string) => void;
  onApprovalAction: (approvalId: string, action: 'approved' | 'modified' | 'rejected') => void;
  onViewRecommendationsTab: () => void;
}

export const ChatArea: React.FC<ChatAreaProps> = ({
  messages,
  isStreaming,
  onSubmitPrompt,
  onApprovalAction,
  onViewRecommendationsTab,
}) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isStreaming]);

  return (
    <div className="flex flex-col h-full bg-background relative overflow-hidden">
      {/* Top Chat Header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-border bg-background/80 backdrop-blur-md shrink-0 z-10">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
            <Car className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h2 className="text-sm font-bold text-foreground tracking-tight">
                AI Purchase Consultant Workspace
              </h2>
              <Badge variant="outline" className="text-[10px] py-0 px-1.5 border-emerald-500/40 text-emerald-600 dark:text-emerald-400 bg-emerald-500/10">
                Live StateGraph
              </Badge>
            </div>
            <p className="text-[11px] text-muted-foreground">
              Connected to PostgreSQL master catalogue & fuzzy recommendation scoring pipeline
            </p>
          </div>
        </div>

        <button
          onClick={onViewRecommendationsTab}
          className="text-xs font-medium text-muted-foreground hover:text-foreground flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-border/80 bg-muted/40 hover:bg-muted transition-colors"
        >
          <Sparkles className="w-3.5 h-3.5 text-primary" />
          <span>Inspect Canvas</span>
        </button>
      </div>

      {/* Message Feed */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-6 space-y-6">
        {messages.map((msg) => {
          if (msg.role === 'system') {
            return (
              <div key={msg.id} className="flex justify-center my-2">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-muted/60 text-muted-foreground border border-border/60 text-[11px]">
                  <Sparkles className="w-3 h-3 text-primary" />
                  <span>{msg.content}</span>
                </div>
              </div>
            );
          }

          const isUser = msg.role === 'user';

          return (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
            >
              {/* Avatar */}
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 border ${
                  isUser
                    ? 'bg-foreground text-background border-foreground'
                    : 'bg-primary/10 text-primary border-primary/20'
                }`}
              >
                {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>

              {/* Message Content Bubble */}
              <div className={`space-y-2 max-w-[88%] ${isUser ? 'text-right' : 'text-left'}`}>
                <div className="flex items-center gap-2 text-[11px] text-muted-foreground px-1">
                  <span className="font-semibold">{isUser ? 'You' : 'SVPC AutoAgent'}</span>
                  <span>•</span>
                  <span>{msg.timestamp}</span>
                </div>

                {/* Thinking Block if present */}
                {msg.thinking && <ThinkingBlock thinking={msg.thinking} />}

                {/* Tool Invocations */}
                {msg.toolCalls && msg.toolCalls.length > 0 && (
                  <div className="space-y-1 my-1.5">
                    {msg.toolCalls.map((tool) => (
                      <ToolInvocationChip key={tool.id} tool={tool} />
                    ))}
                  </div>
                )}

                {/* Approval Card if present */}
                {msg.approvalRequest && (
                  <ApprovalCard approval={msg.approvalRequest} onAction={onApprovalAction} />
                )}

                {/* Body Content */}
                {msg.content && (
                  <div
                    className={`rounded-2xl px-4 py-3 text-xs leading-relaxed transition-all shadow-xs ${
                      isUser
                        ? 'bg-primary text-primary-foreground rounded-tr-xs'
                        : 'bg-card border border-border text-card-foreground rounded-tl-xs'
                    }`}
                  >
                    <div className="whitespace-pre-wrap font-sans">{msg.content}</div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Floating / Docked Prompt Composer Bar */}
      <div className="p-4 border-t border-border bg-background/90 backdrop-blur-md shrink-0">
        <PromptBar onSubmit={onSubmitPrompt} isStreaming={isStreaming} />
      </div>
    </div>
  );
};
