import { useCallback, useEffect, useRef, useState } from 'react';
import type {
  ApprovalRequest,
  ChatMessage,
  ConsultationSession,
  LangGraphNode,
  UserPreferenceProfile,
  Vehicle,
} from '../types/agent';

const API = import.meta.env.VITE_API_BASE_URL || '/api/v1';
const now = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const INITIAL_PROFILE: UserPreferenceProfile = {
  city: '',
  maxBudget: 0,
  preferredFuels: [],
  preferredTransmissions: [],
  primaryUse: 'Daily commute',
  annualDistanceKm: 10_000,
  ownershipYears: 5,
  priorities: { safety: 'high', efficiency: 'medium', space: 'medium', performance: 'low', features: 'medium' },
};

const NODE_DEFINITIONS: LangGraphNode[] = [
  ['parse_request', 'Understand request', 'Extract and validate the purchase profile.'],
  ['clarify_preferences', 'Clarify preferences', 'Pause for required city or budget.'],
  ['query_catalogue', 'SQL catalogue agent', 'Generate, check, and execute a read-only query.'],
  ['validate_candidates', 'Validate candidates', 'Re-fetch facts and enforce hard constraints.'],
  ['score_catalogue_fit', 'Catalogue scoring', 'Calculate deterministic suitability scores.'],
  ['retrieve_official_documents', 'Official-document RAG', 'Retrieve applicable manuals and policies.'],
  ['research_current_costs', 'Current cost research', 'Ground ownership evidence with Google Search.'],
  ['calculate_ownership_cost', 'Ownership cost', 'Calculate auditable ownership components.'],
  ['final_rank', 'Final ranking', 'Combine fit and ownership cost deterministically.'],
  ['request_relaxation', 'Criteria approval', 'Pause before relaxing a hard constraint.'],
  ['synthesize', 'Recommendation', 'Explain the fixed ranking and evidence gaps.'],
].map(([name, label, description]) => ({ id: name, name, label, description, state: 'idle' }));

type ApiEvent = Record<string, unknown> & { type: string };
type Raw = Record<string, any>;

function apiProfile(profile: UserPreferenceProfile) {
  return {
    city: profile.city || null,
    min_budget: profile.minBudget,
    max_budget: profile.maxBudget || null,
    preferred_fuels: profile.preferredFuels,
    preferred_transmissions: profile.preferredTransmissions,
    mandatory_seats: profile.mandatorySeats,
    primary_use: profile.primaryUse,
    annual_distance_km: profile.annualDistanceKm,
    ownership_years: profile.ownershipYears,
    priorities: profile.priorities,
  };
}

function uiProfile(raw: Raw): UserPreferenceProfile {
  return {
    city: raw.city || '',
    minBudget: raw.min_budget,
    maxBudget: raw.max_budget || 0,
    preferredFuels: raw.preferred_fuels || [],
    preferredTransmissions: raw.preferred_transmissions || [],
    mandatorySeats: raw.mandatory_seats,
    primaryUse: raw.primary_use || INITIAL_PROFILE.primaryUse,
    annualDistanceKm: raw.annual_distance_km || 10_000,
    ownershipYears: raw.ownership_years || 5,
    priorities: { ...INITIAL_PROFILE.priorities, ...(raw.priorities || {}) },
  };
}

function uiVehicle(raw: Raw): Vehicle {
  const efficiency = raw.mileage_arai_kmpl
    ? `${raw.mileage_arai_kmpl} km/l`
    : raw.mileage_arai_kmkg
      ? `${raw.mileage_arai_kmkg} km/kg`
      : raw.driving_range_km
        ? `${raw.driving_range_km} km range`
        : 'Not reported';
  return {
    id: String(raw.variant_id), catalogueId: raw.catalogue_id, make: raw.brand,
    model: raw.model, year: raw.model_year, trim: raw.trim, variantName: raw.variant_name,
    city: raw.city, price: raw.price, priceBasis: raw.price_basis,
    fuelType: raw.fuel_type || 'petrol', transmissionType: raw.transmission_type || 'manual',
    efficiency, powerBhp: raw.max_power_bhp, bootspaceLitres: raw.bootspace_litres,
    seatingCapacity: raw.seating_capacity, airbagCount: raw.airbag_count,
    matchScore: raw.score, confidence: raw.confidence, scoreBreakdown: raw.score_breakdown || {},
    pros: raw.pros || [], cons: raw.cons || [], keyFeatures: raw.key_features || [],
    ownershipCost: raw.ownership_cost, evidenceUrls: raw.evidence_urls || [],
  };
}

async function readSse(response: Response, onEvent: (event: ApiEvent) => void) {
  if (!response.ok || !response.body) throw new Error(`Request failed (${response.status})`);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { value, done } = await reader.read();
    buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
    const blocks = buffer.split(/\r?\n\r?\n/);
    buffer = blocks.pop() || '';
    for (const block of blocks) {
      const data = block.split(/\r?\n/).filter((line) => line.startsWith('data:')).map((line) => line.slice(5).trim()).join('\n');
      if (data) onEvent(JSON.parse(data));
    }
    if (done) break;
  }
}

export function useAgentWorkspace() {
  const [sessions, setSessions] = useState<ConsultationSession[]>([]);
  const [activeSessionId, setActiveSessionIdState] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeTab, setActiveTab] = useState<'recommendations' | 'comparison' | 'workflow' | 'profile'>('recommendations');
  const [shortlistedVehicleIds, setShortlistedVehicleIds] = useState<string[]>([]);
  const [selectedVehicleId, setSelectedVehicleId] = useState<string | null>(null);
  const [profile, setProfile] = useState<UserPreferenceProfile>(INITIAL_PROFILE);
  const [langGraphNodes, setLangGraphNodes] = useState<LangGraphNode[]>(NODE_DEFINITIONS);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const pendingInterrupt = useRef<'missing_preferences' | 'criteria_relaxation' | null>(null);

  const loadSessions = useCallback(async () => {
    const response = await fetch(`${API}/consultations`, { credentials: 'include' });
    if (!response.ok) return;
    const data = await response.json();
    setSessions(data.map((item: Raw) => ({
      id: item.thread_id, title: item.title, date: new Date(item.updated_at).toLocaleDateString(),
      vehicleCount: item.vehicle_count, status: item.status, lastMessageSnippet: item.last_message_summary,
    })));
  }, []);

  const selectSession = useCallback(async (id: string) => {
    const response = await fetch(`${API}/consultations/${id}`, { credentials: 'include' });
    if (!response.ok) return;
    const data = await response.json();
    setActiveSessionIdState(id);
    setMessages(data.messages.map((item: Raw, index: number) => ({ ...item, id: `${id}-${index}`, timestamp: '' })));
    setVehicles(data.recommendations.map(uiVehicle));
    setShortlistedVehicleIds(data.shortlisted_variant_ids.map(String));
    setProfile(uiProfile(data.profile));
    setSelectedVehicleId(data.recommendations[0] ? String(data.recommendations[0].variant_id) : null);
    setLangGraphNodes(NODE_DEFINITIONS);
    pendingInterrupt.current = null;
  }, []);

  useEffect(() => { void loadSessions(); }, [loadSessions]);

  const createSession = useCallback(async () => {
    const response = await fetch(`${API}/consultations`, {
      method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'New consultation', profile: apiProfile(profile) }),
    });
    if (!response.ok) throw new Error('Unable to create consultation');
    const data = await response.json();
    setActiveSessionIdState(data.thread_id);
    return data.thread_id as string;
  }, [profile]);

  const runStream = useCallback(async (url: string, body: object, assistantId: string) => {
    const response = await fetch(url, {
      method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    });
    await readSse(response, (event) => {
      if (event.type === 'node_start') {
        const node = String(event.node);
        setLangGraphNodes((current) => current.map((item) => item.name === node ? { ...item, state: 'running' } : item));
        setMessages((current) => current.map((item) => item.id === assistantId && item.thinking
          ? { ...item, thinking: { ...item.thinking, thoughts: [...item.thinking.thoughts, `Started ${node.replaceAll('_', ' ')}`] } }
          : item));
      } else if (event.type === 'node_end') {
        const node = String(event.node);
        setLangGraphNodes((current) => current.map((item) => item.name === node
          ? { ...item, state: 'completed', durationMs: Number(event.duration_ms) } : item));
      } else if (event.type === 'tool_start') {
        setMessages((current) => current.map((item) => item.id === assistantId
          ? { ...item, toolCalls: [...(item.toolCalls || []), { id: String(event.run_id), toolName: String(event.tool), label: 'Grounded tool execution', status: 'running' }] } : item));
      } else if (event.type === 'tool_end') {
        setMessages((current) => current.map((item) => item.id === assistantId
          ? { ...item, toolCalls: (item.toolCalls || []).map((tool) => tool.id === event.run_id ? { ...tool, status: 'completed', executionTimeMs: Number(event.duration_ms) } : tool) } : item));
      } else if (event.type === 'interrupt') {
        const payload = event.payload as Raw;
        pendingInterrupt.current = payload.type;
        if (payload.type === 'criteria_relaxation') {
          const approval: ApprovalRequest = {
            id: `approval-${Date.now()}`, title: payload.title, description: payload.description,
            type: 'criteria_relaxation', payload: {
              suggestedBudget: payload.suggested_budget,
              tradeoffSummary: `Current ₹${Number(payload.current_budget).toLocaleString('en-IN')} → suggested ₹${Number(payload.suggested_budget).toLocaleString('en-IN')}`,
            }, status: 'pending',
          };
          setMessages((current) => current.map((item) => item.id === assistantId ? { ...item, approvalRequest: approval, thinking: item.thinking && { ...item.thinking, isThinking: false } } : item));
        } else {
          setMessages((current) => current.map((item) => item.id === assistantId ? { ...item, content: `${payload.description}\nMissing: ${(payload.missing_fields || []).join(', ')}`, thinking: item.thinking && { ...item.thinking, isThinking: false } } : item));
        }
      } else if (event.type === 'final') {
        pendingInterrupt.current = null;
        const recommendations = ((event.recommendations as Raw[]) || []).map(uiVehicle);
        setVehicles(recommendations);
        setSelectedVehicleId(recommendations[0]?.id || null);
        if (event.profile) setProfile(uiProfile(event.profile as Raw));
        setMessages((current) => current.map((item) => item.id === assistantId ? {
          ...item, content: String(event.answer || ''), recommendationIds: recommendations.map((vehicle) => vehicle.id),
          thinking: item.thinking && { ...item.thinking, isThinking: false },
        } : item));
      }
    });
  }, []);

  const submitPrompt = useCallback(async (promptText: string) => {
    if (!promptText.trim() || isStreaming) return;
    setIsStreaming(true);
    const assistantId = `assistant-${Date.now()}`;
    setMessages((current) => [...current,
      { id: `user-${Date.now()}`, role: 'user', content: promptText, timestamp: now() },
      { id: assistantId, role: 'assistant', content: '', timestamp: now(), thinking: { isThinking: true, thoughts: ['Workflow started'], durationSeconds: 0 }, toolCalls: [] },
    ]);
    setLangGraphNodes(NODE_DEFINITIONS);
    try {
      const threadId = activeSessionId || await createSession();
      const interruptType = pendingInterrupt.current;
      if (interruptType) {
        await runStream(`${API}/consultations/${threadId}/resume`, interruptType === 'criteria_relaxation'
          ? { decision: 'modified', message: promptText } : { message: promptText }, assistantId);
      } else {
        await runStream(`${API}/consultations/${threadId}/messages`, { message: promptText }, assistantId);
      }
      await loadSessions();
    } catch (error) {
      setMessages((current) => current.map((item) => item.id === assistantId ? {
        ...item, content: error instanceof Error ? error.message : 'Request failed',
        thinking: item.thinking && { ...item.thinking, isThinking: false },
      } : item));
    } finally { setIsStreaming(false); }
  }, [activeSessionId, createSession, isStreaming, loadSessions, runStream]);

  const handleApprovalAction = useCallback(async (approvalId: string, action: 'approved' | 'modified' | 'rejected') => {
    if (action === 'modified') {
      setMessages((current) => [...current, { id: `modify-${Date.now()}`, role: 'assistant', content: 'Describe the budget or hard-constraint change you want.', timestamp: now() }]);
      return;
    }
    const assistantId = `resume-${Date.now()}`;
    setMessages((current) => [...current, { id: assistantId, role: 'assistant', content: '', timestamp: now(), thinking: { isThinking: true, thoughts: ['Resuming approved workflow'], durationSeconds: 0 } }]);
    setIsStreaming(true);
    try {
      await runStream(`${API}/consultations/${activeSessionId}/resume`, { decision: action }, assistantId);
      setMessages((current) => current.map((item) => item.approvalRequest?.id === approvalId
        ? { ...item, approvalRequest: { ...item.approvalRequest, status: action, resolvedAt: now() } } : item));
      await loadSessions();
    } finally { setIsStreaming(false); }
  }, [activeSessionId, loadSessions, runStream]);

  const resetSession = useCallback(async () => {
    const id = await createSession();
    setMessages([{ id: `welcome-${Date.now()}`, role: 'assistant', content: 'What city, maximum on-road budget, and intended use should I consider?', timestamp: now() }]);
    setVehicles([]); setShortlistedVehicleIds([]); setSelectedVehicleId(null);
    setLangGraphNodes(NODE_DEFINITIONS); pendingInterrupt.current = null;
    await loadSessions();
    return id;
  }, [createSession, loadSessions]);

  const toggleShortlist = useCallback(async (vehicleId: string) => {
    if (!activeSessionId) return;
    const removing = shortlistedVehicleIds.includes(vehicleId);
    setShortlistedVehicleIds((current) => removing ? current.filter((id) => id !== vehicleId) : [...current, vehicleId]);
    const response = await fetch(`${API}/consultations/${activeSessionId}/shortlist/${vehicleId}`, { method: removing ? 'DELETE' : 'PUT', credentials: 'include' });
    if (!response.ok) setShortlistedVehicleIds((current) => removing ? [...current, vehicleId] : current.filter((id) => id !== vehicleId));
  }, [activeSessionId, shortlistedVehicleIds]);

  return {
    sessions, activeSessionId, setActiveSessionId: selectSession, messages, isStreaming,
    activeTab, setActiveTab, vehicles, shortlistedVehicleIds, selectedVehicleId,
    setSelectedVehicleId, toggleShortlist, profile, setProfile, langGraphNodes,
    submitPrompt, handleApprovalAction, resetSession,
  };
}
