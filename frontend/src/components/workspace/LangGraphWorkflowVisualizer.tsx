import React from 'react';
import type { LangGraphNode } from '../../types/agent';
import { CheckCircle2, Loader2, Activity, Clock, Database, Sliders, Cpu, Sparkles } from 'lucide-react';
import { Badge } from '../ui/badge';

interface LangGraphWorkflowVisualizerProps {
  nodes: LangGraphNode[];
}

export const LangGraphWorkflowVisualizer: React.FC<LangGraphWorkflowVisualizerProps> = ({ nodes }) => {
  const getNodeIcon = (nodeName: string) => {
    if (nodeName.includes('intake')) return <Activity className="w-4 h-4 text-blue-500" />;
    if (nodeName.includes('catalogue')) return <Database className="w-4 h-4 text-emerald-500" />;
    if (nodeName.includes('fuzzy')) return <Sliders className="w-4 h-4 text-purple-500" />;
    if (nodeName.includes('ranker')) return <Cpu className="w-4 h-4 text-amber-500" />;
    return <Sparkles className="w-4 h-4 text-primary" />;
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-foreground tracking-tight flex items-center gap-2">
            <Cpu className="w-4 h-4 text-primary" />
            LangGraph Multi-Agent Workflow State
          </h3>
          <p className="text-xs text-muted-foreground">
            Dynamic StateGraph execution pipeline with typed channel projections.
          </p>
        </div>
        <Badge variant="outline" className="font-mono text-[10px] gap-1">
          <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse" />
          LangGraph v1.2+ SSE
        </Badge>
      </div>

      <div className="relative pl-6 space-y-4 before:absolute before:left-3 before:top-3 before:bottom-3 before:w-0.5 before:bg-border">
        {nodes.map((node) => {
          const isRunning = node.state === 'running';
          const isCompleted = node.state === 'completed';
          const isIdle = node.state === 'idle';

          return (
            <div
              key={node.id}
              className={`relative rounded-xl border p-3.5 transition-all text-xs ${
                isRunning
                  ? 'border-primary bg-primary/5 ring-1 ring-primary shadow-sm'
                  : isCompleted
                  ? 'border-border bg-card'
                  : 'border-border/60 bg-muted/20 opacity-60'
              }`}
            >
              {/* Node state point marker on timeline */}
              <div
                className={`absolute -left-6 top-4 w-4 h-4 rounded-full border-2 flex items-center justify-center -translate-x-1/2 bg-background ${
                  isRunning
                    ? 'border-primary text-primary'
                    : isCompleted
                    ? 'border-emerald-500 bg-emerald-500 text-white'
                    : 'border-muted-foreground/40 bg-muted'
                }`}
              >
                {isRunning && <Loader2 className="w-2.5 h-2.5 animate-spin" />}
                {isCompleted && <CheckCircle2 className="w-2.5 h-2.5" />}
              </div>

              {/* Node Header */}
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  {getNodeIcon(node.name)}
                  <span className="font-semibold text-foreground text-xs">{node.label}</span>
                  <span className="font-mono text-[10px] text-muted-foreground">({node.name})</span>
                </div>

                <div className="flex items-center gap-2">
                  {node.durationMs && (
                    <span className="font-mono text-[10px] text-muted-foreground flex items-center gap-0.5">
                      <Clock className="w-2.5 h-2.5" />
                      {node.durationMs}ms
                    </span>
                  )}
                  {isRunning && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-primary/20 text-primary font-medium flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-primary animate-ping" />
                      Executing
                    </span>
                  )}
                  {isCompleted && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-medium">
                      Completed
                    </span>
                  )}
                  {isIdle && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
                      Pending
                    </span>
                  )}
                </div>
              </div>

              {/* Description */}
              <p className="text-muted-foreground text-[11px] leading-relaxed mb-2">
                {node.description}
              </p>

              {/* Output Summary */}
              {node.outputSummary && (
                <div className="p-2 rounded-lg bg-muted/40 border border-border/50 font-mono text-[10px] text-foreground/80">
                  <span className="text-muted-foreground font-semibold uppercase">Channel Output: </span>
                  {node.outputSummary}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
