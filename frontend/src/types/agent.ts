export type PowertrainType = 'EV' | 'Hybrid' | 'Plug-in Hybrid' | 'Gasoline';

export interface Vehicle {
  id: string;
  make: string;
  model: string;
  year: number;
  trim: string;
  price: number;
  powertrain: PowertrainType;
  epaMpgOrRange: string; // e.g. "330 mi range" or "40 MPG combined"
  zeroToSixty: string; // e.g. "4.8s"
  cargoVolumeCuFt: number; // e.g. 76 cu ft
  safetyRatingStars: number; // 1-5
  nhtsaOverallScore: string; // "5-Star Safety Rating"
  matchScore: number; // 0-100%
  imageUrl: string;
  fuzzyMatchBreakdown: {
    budgetScore: number;
    efficiencyScore: number;
    spaceScore: number;
    performanceScore: number;
    safetyScore: number;
  };
  pros: string[];
  cons: string[];
  keyFeatures: string[];
  estimated5YearOwnershipCost: number;
}

export interface UserPreferenceProfile {
  budgetMin: number;
  budgetMax: number;
  preferredPowertrains: PowertrainType[];
  seatingCapacity: number;
  primaryUse: 'Daily Commute' | 'Family Roadtrips' | 'City Runabout' | 'Utility & Hauling';
  priorities: {
    safety: 'Low' | 'Medium' | 'High';
    fuelEconomy: 'Low' | 'Medium' | 'High';
    performance: 'Low' | 'Medium' | 'High';
    cargoSpace: 'Low' | 'Medium' | 'High';
    techFeatures: 'Low' | 'Medium' | 'High';
  };
}

export type ToolStatus = 'running' | 'completed' | 'failed';

export interface ToolCallItem {
  id: string;
  toolName: string;
  label: string;
  status: ToolStatus;
  inputParams?: Record<string, unknown>;
  outputResult?: Record<string, unknown> | string;
  executionTimeMs?: number;
}

export interface ApprovalRequest {
  id: string;
  title: string;
  description: string;
  type: 'budget_increase' | 'criteria_relaxation' | 'schedule_test_drive';
  payload: {
    suggestedBudgetDelta?: number;
    relaxedConstraint?: string;
    tradeoffSummary?: string;
  };
  status: 'pending' | 'approved' | 'modified' | 'rejected';
  resolvedAt?: string;
}

export interface ThinkingState {
  isThinking: boolean;
  thoughts: string[];
  durationSeconds: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  thinking?: ThinkingState;
  toolCalls?: ToolCallItem[];
  approvalRequest?: ApprovalRequest;
  recommendationIds?: string[];
}

export type LangGraphNodeState = 'idle' | 'running' | 'completed' | 'error';

export interface LangGraphNode {
  id: string;
  name: string;
  label: string;
  state: LangGraphNodeState;
  description: string;
  durationMs?: number;
  outputSummary?: string;
}

export interface ConsultationSession {
  id: string;
  title: string;
  date: string;
  vehicleCount: number;
  status: 'active' | 'completed' | 'saved';
  lastMessageSnippet: string;
}
