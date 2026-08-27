export type FuelType = 'petrol' | 'cng' | 'hybrid' | 'electric';
export type TransmissionType = 'manual' | 'automatic' | 'amt' | 'torque_converter' | 'e_cvt';
export type Priority = 'low' | 'medium' | 'high';

export interface OwnershipCost {
  years: number;
  purchase_price: number;
  fuel_energy_cost?: number | null;
  maintenance_cost?: number | null;
  insurance_cost?: number | null;
  finance_cost?: number | null;
  resale_value?: number | null;
  total_cost: number;
  assumptions: string[];
  confidence: number;
}

export interface Vehicle {
  id: string;
  catalogueId: string;
  make: string;
  model: string;
  year: number;
  trim: string;
  variantName: string;
  city: string;
  price: number;
  priceBasis: 'on_road' | 'provisional_ex_showroom';
  fuelType: FuelType;
  transmissionType: TransmissionType;
  efficiency: string;
  powerBhp?: number | null;
  bootspaceLitres?: number | null;
  seatingCapacity?: number | null;
  airbagCount?: number | null;
  matchScore: number;
  confidence: number;
  scoreBreakdown: Record<string, number>;
  pros: string[];
  cons: string[];
  keyFeatures: string[];
  ownershipCost: OwnershipCost;
  evidenceUrls: string[];
}

export interface UserPreferenceProfile {
  city: string;
  minBudget?: number;
  maxBudget: number;
  preferredFuels: FuelType[];
  preferredTransmissions: TransmissionType[];
  mandatorySeats?: number;
  primaryUse: string;
  annualDistanceKm: number;
  ownershipYears: number;
  priorities: {
    safety: Priority;
    efficiency: Priority;
    space: Priority;
    performance: Priority;
    features: Priority;
  };
}

export type ToolStatus = 'running' | 'completed' | 'failed';

export interface ToolCallItem {
  id: string;
  toolName: string;
  label: string;
  status: ToolStatus;
  executionTimeMs?: number;
}

export interface ApprovalRequest {
  id: string;
  title: string;
  description: string;
  type: 'criteria_relaxation';
  payload: { suggestedBudget?: number; tradeoffSummary?: string };
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
