import React from 'react';
import { HelpCircle, Check, X, Edit3, ShieldAlert, Sparkles } from 'lucide-react';
import type { ApprovalRequest } from '../../types/agent';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';

interface ApprovalCardProps {
  approval: ApprovalRequest;
  onAction: (approvalId: string, action: 'approved' | 'modified' | 'rejected') => void;
}

export const ApprovalCard: React.FC<ApprovalCardProps> = ({ approval, onAction }) => {
  const isPending = approval.status === 'pending';

  return (
    <div className="my-3 border-2 border-primary/20 bg-card rounded-xl p-4 shadow-sm transition-all text-card-foreground">
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-primary/10 text-primary">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-semibold tracking-tight text-foreground">
              {approval.title}
            </h4>
            <span className="text-[11px] text-muted-foreground">
              Human-in-the-loop (HITL) Decision Required
            </span>
          </div>
        </div>

        <div>
          {approval.status === 'pending' && (
            <Badge variant="outline" className="text-[10px] border-amber-500/40 text-amber-600 dark:text-amber-400 bg-amber-500/10 animate-pulse">
              Awaiting Approval
            </Badge>
          )}
          {approval.status === 'approved' && (
            <Badge variant="default" className="text-[10px] bg-emerald-600 text-white">
              Approved
            </Badge>
          )}
          {approval.status === 'modified' && (
            <Badge variant="secondary" className="text-[10px]">
              Modified
            </Badge>
          )}
          {approval.status === 'rejected' && (
            <Badge variant="destructive" className="text-[10px]">
              Declined
            </Badge>
          )}
        </div>
      </div>

      <p className="text-xs text-muted-foreground leading-relaxed mb-3">
        {approval.description}
      </p>

      {approval.payload.tradeoffSummary && (
        <div className="mb-3 p-2.5 rounded-lg bg-muted/40 border border-border/60 text-xs">
          <div className="flex items-center gap-1.5 font-medium text-foreground/90 mb-1">
            <HelpCircle className="w-3.5 h-3.5 text-primary" />
            <span>Agent Trade-Off Impact:</span>
          </div>
          <p className="text-muted-foreground text-[11px]">
            {approval.payload.tradeoffSummary}
          </p>
        </div>
      )}

      {isPending ? (
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <Button
            size="sm"
            onClick={() => onAction(approval.id, 'approved')}
            className="gap-1.5 text-xs bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <Check className="w-3.5 h-3.5" />
            Approve Adjustment
          </Button>

          <Button
            size="sm"
            variant="outline"
            onClick={() => onAction(approval.id, 'modified')}
            className="gap-1.5 text-xs"
          >
            <Edit3 className="w-3.5 h-3.5" />
            Keep Unsubsidized
          </Button>

          <Button
            size="sm"
            variant="ghost"
            onClick={() => onAction(approval.id, 'rejected')}
            className="gap-1.5 text-xs text-destructive hover:bg-destructive/10"
          >
            <X className="w-3.5 h-3.5" />
            Decline
          </Button>
        </div>
      ) : (
        <div className="text-[11px] text-muted-foreground italic flex items-center gap-1.5 pt-1 border-t border-border/50">
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>Decision recorded at {approval.resolvedAt || 'earlier in session'}. Workflow continued.</span>
        </div>
      )}
    </div>
  );
};
