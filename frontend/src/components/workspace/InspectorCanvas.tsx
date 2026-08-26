import React from 'react';
import type { Vehicle, LangGraphNode, UserPreferenceProfile } from '../../types/agent';
import { VehicleCard } from './VehicleCard';
import { ComparisonMatrix } from './ComparisonMatrix';
import { LangGraphWorkflowVisualizer } from './LangGraphWorkflowVisualizer';
import { IntakeProfileDrawer } from './IntakeProfileDrawer';
import { Sparkles, Layers, Cpu, Sliders, ChevronRight, ChevronLeft } from 'lucide-react';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

interface InspectorCanvasProps {
  activeTab: 'recommendations' | 'comparison' | 'workflow' | 'profile';
  setActiveTab: (tab: 'recommendations' | 'comparison' | 'workflow' | 'profile') => void;
  vehicles: Vehicle[];
  shortlistedIds: string[];
  selectedVehicleId: string | null;
  setSelectedVehicleId: (id: string | null) => void;
  onToggleShortlist: (id: string) => void;
  langGraphNodes: LangGraphNode[];
  profile: UserPreferenceProfile;
  onUpdateProfile: (p: UserPreferenceProfile) => void;
  onRunConsultationWithProfile: () => void;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
}

export const InspectorCanvas: React.FC<InspectorCanvasProps> = ({
  activeTab,
  setActiveTab,
  vehicles,
  shortlistedIds,
  selectedVehicleId,
  setSelectedVehicleId,
  onToggleShortlist,
  langGraphNodes,
  profile,
  onUpdateProfile,
  onRunConsultationWithProfile,
  isCollapsed = false,
  onToggleCollapse,
}) => {
  if (isCollapsed) {
    return (
      <div className="flex flex-col items-center justify-between py-4 px-2 w-14 border-l border-border bg-card/60 backdrop-blur-md h-full shrink-0">
        <div className="flex flex-col items-center gap-3">
          <Button
            size="icon-xs"
            variant="ghost"
            onClick={onToggleCollapse}
            title="Expand Canvas"
            className="rounded-lg text-muted-foreground hover:text-foreground"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </Button>

          <div className="w-6 h-px bg-border my-1" />

          <Button
            size="icon-xs"
            variant={activeTab === 'recommendations' ? 'default' : 'ghost'}
            onClick={() => {
              setActiveTab('recommendations');
              onToggleCollapse?.();
            }}
            title="Rankings"
            className="rounded-lg"
          >
            <Sparkles className="w-3.5 h-3.5" />
          </Button>

          <Button
            size="icon-xs"
            variant={activeTab === 'comparison' ? 'default' : 'ghost'}
            onClick={() => {
              setActiveTab('comparison');
              onToggleCollapse?.();
            }}
            title="Compare Matrix"
            className="rounded-lg relative"
          >
            <Layers className="w-3.5 h-3.5" />
            {shortlistedIds.length > 0 && (
              <span className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-primary text-primary-foreground text-[9px] rounded-full flex items-center justify-center font-mono">
                {shortlistedIds.length}
              </span>
            )}
          </Button>

          <Button
            size="icon-xs"
            variant={activeTab === 'workflow' ? 'default' : 'ghost'}
            onClick={() => {
              setActiveTab('workflow');
              onToggleCollapse?.();
            }}
            title="LangGraph Nodes"
            className="rounded-lg"
          >
            <Cpu className="w-3.5 h-3.5" />
          </Button>

          <Button
            size="icon-xs"
            variant={activeTab === 'profile' ? 'default' : 'ghost'}
            onClick={() => {
              setActiveTab('profile');
              onToggleCollapse?.();
            }}
            title="Intake Tuner"
            className="rounded-lg"
          >
            <Sliders className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-card/60 backdrop-blur-md border-l border-border">
      {/* Header Tabs */}
      <div className="flex items-center justify-between px-3 py-2.5 border-b border-border bg-background/80 shrink-0">
        <div className="flex items-center gap-1 overflow-x-auto scrollbar-none">
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'recommendations'
                ? 'bg-primary text-primary-foreground shadow-xs'
                : 'text-muted-foreground hover:text-foreground hover:bg-muted/60'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Rankings ({vehicles.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('comparison')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all relative ${
              activeTab === 'comparison'
                ? 'bg-primary text-primary-foreground shadow-xs'
                : 'text-muted-foreground hover:text-foreground hover:bg-muted/60'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Compare</span>
            {shortlistedIds.length > 0 && (
              <span
                className={`ml-1 px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                  activeTab === 'comparison'
                    ? 'bg-primary-foreground/20 text-primary-foreground'
                    : 'bg-muted text-foreground'
                }`}
              >
                {shortlistedIds.length}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('workflow')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'workflow'
                ? 'bg-primary text-primary-foreground shadow-xs'
                : 'text-muted-foreground hover:text-foreground hover:bg-muted/60'
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>Nodes</span>
          </button>

          <button
            onClick={() => setActiveTab('profile')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'profile'
                ? 'bg-primary text-primary-foreground shadow-xs'
                : 'text-muted-foreground hover:text-foreground hover:bg-muted/60'
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>Tuner</span>
          </button>
        </div>

        {onToggleCollapse && (
          <Button
            size="icon-xs"
            variant="ghost"
            onClick={onToggleCollapse}
            title="Collapse Canvas"
            className="text-muted-foreground hover:text-foreground shrink-0 ml-1"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </Button>
        )}
      </div>

      {/* Main Tab Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeTab === 'recommendations' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-foreground tracking-tight">
                  Scored Vehicle Recommendations
                </h3>
                <p className="text-xs text-muted-foreground">
                  Ranked by Multi-Attribute Fuzzy Engine using current profile constraints.
                </p>
              </div>
              <Badge variant="outline" className="text-[10px] font-mono">
                {shortlistedIds.length} in compare
              </Badge>
            </div>

            <div className="space-y-3.5">
              {vehicles.map((v) => (
                <VehicleCard
                  key={v.id}
                  vehicle={v}
                  isShortlisted={shortlistedIds.includes(v.id)}
                  onToggleShortlist={onToggleShortlist}
                  onSelectVehicle={setSelectedVehicleId}
                  isSelected={selectedVehicleId === v.id}
                />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'comparison' && (
          <ComparisonMatrix
            vehicles={vehicles}
            shortlistedIds={shortlistedIds}
            onToggleShortlist={onToggleShortlist}
          />
        )}

        {activeTab === 'workflow' && (
          <LangGraphWorkflowVisualizer nodes={langGraphNodes} />
        )}

        {activeTab === 'profile' && (
          <IntakeProfileDrawer
            profile={profile}
            onUpdateProfile={onUpdateProfile}
            onRunConsultationWithProfile={onRunConsultationWithProfile}
          />
        )}
      </div>
    </div>
  );
};
