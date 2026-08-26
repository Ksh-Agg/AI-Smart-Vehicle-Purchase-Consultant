import { useState, useCallback, useRef } from 'react';
import type {
  ChatMessage,
  Vehicle,
  UserPreferenceProfile,
  LangGraphNode,
  ConsultationSession,
  ApprovalRequest,
  ToolCallItem,
} from '../types/agent';
import {
  INITIAL_VEHICLES,
  INITIAL_PREFERENCE_PROFILE,
  INITIAL_LANGGRAPH_NODES,
  simulateLangGraphConsultationStream,
} from '../lib/mock-langgraph-stream';

export function useAgentWorkspace() {
  const [sessions, setSessions] = useState<ConsultationSession[]>([
    {
      id: 'sess-1',
      title: 'Family EV / Hybrid SUV under $50k',
      date: 'Just now',
      vehicleCount: 5,
      status: 'active',
      lastMessageSnippet: 'Ranked Model Y, Ioniq 5, RAV4 Hybrid based on safety & cargo',
    },
    {
      id: 'sess-2',
      title: 'Commuter Sedan with High MPG',
      date: 'Yesterday',
      vehicleCount: 3,
      status: 'saved',
      lastMessageSnippet: 'Shortlisted Civic Hybrid & Prius Prime',
    },
    {
      id: 'sess-3',
      title: 'Luxury Electric Coupe Audit',
      date: 'Aug 24, 2026',
      vehicleCount: 2,
      status: 'completed',
      lastMessageSnippet: 'Evaluated BMW i4 vs Polestar 2 depreciation',
    }
  ]);

  const [activeSessionId, setActiveSessionId] = useState<string>('sess-1');
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeTab, setActiveTab] = useState<'recommendations' | 'comparison' | 'workflow' | 'profile'>('recommendations');
  const [shortlistedVehicleIds, setShortlistedVehicleIds] = useState<string[]>(['veh-1', 'veh-2', 'veh-3']);
  const [selectedVehicleId, setSelectedVehicleId] = useState<string | null>('veh-1');
  const [profile, setProfile] = useState<UserPreferenceProfile>(INITIAL_PREFERENCE_PROFILE);
  const [langGraphNodes, setLangGraphNodes] = useState<LangGraphNode[]>(INITIAL_LANGGRAPH_NODES);
  const [vehicles, setVehicles] = useState<Vehicle[]>(INITIAL_VEHICLES);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg-init-system',
      role: 'system',
      content: 'Welcome to the Smart Vehicle Purchase Consultant Agent Workspace. I am connected to the Master Vehicle Catalogue and the Multi-Attribute Fuzzy Scoring Pipeline.',
      timestamp: '10:00 AM',
    },
    {
      id: 'msg-init-assistant',
      role: 'assistant',
      content: 'Hello! I am your AI Vehicle Purchase Consultant. I analyze vehicle performance, real-world ownership costs, safety certifications, and cargo dimensions to find your ideal match.\n\nTell me about your lifestyle, commute, budget, or specific models you are considering.',
      timestamp: '10:01 AM',
      recommendationIds: ['veh-1', 'veh-2', 'veh-3'],
    }
  ]);

  const streamAbortControllerRef = useRef<boolean>(false);

  const toggleShortlist = useCallback((vehicleId: string) => {
    setShortlistedVehicleIds((prev) =>
      prev.includes(vehicleId)
        ? prev.filter((id) => id !== vehicleId)
        : [...prev, vehicleId]
    );
  }, []);

  const handleApprovalAction = useCallback((approvalId: string, action: 'approved' | 'modified' | 'rejected') => {
    setMessages((prev) =>
      prev.map((msg) => {
        if (msg.approvalRequest && msg.approvalRequest.id === approvalId) {
          return {
            ...msg,
            approvalRequest: {
              ...msg.approvalRequest,
              status: action,
              resolvedAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            },
          };
        }
        return msg;
      })
    );

    const followUpMsg: ChatMessage = {
      id: `msg-approval-${Date.now()}`,
      role: 'assistant',
      content:
        action === 'approved'
          ? '✅ **Federal EV Tax Credit Included:** Adjusted net purchase price calculations. Tesla Model Y effective price updated to **$40,490**, improving its 5-year total ownership rank!'
          : action === 'modified'
          ? '✏️ **Criteria Modified:** Retaining standard MSRP without tax incentives for conservative budgeting.'
          : '❌ **Proposal Declined:** Proceeding with original strict budget ceiling and unsubsidized price baseline.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, followUpMsg]);
  }, []);

  const submitPrompt = useCallback(async (promptText: string) => {
    if (!promptText.trim() || isStreaming) return;

    const userMessageId = `msg-user-${Date.now()}`;
    const assistantMessageId = `msg-agent-${Date.now()}`;
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const userMsg: ChatMessage = {
      id: userMessageId,
      role: 'user',
      content: promptText,
      timestamp,
    };

    const assistantMsg: ChatMessage = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp,
      thinking: {
        isThinking: true,
        thoughts: ['Initializing LangGraph Agent Workflow...', 'Loading user intake constraints...'],
        durationSeconds: 0,
      },
      toolCalls: [],
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setIsStreaming(true);

    setLangGraphNodes((prev) =>
      prev.map((n, i) => (i === 0 ? { ...n, state: 'running' } : { ...n, state: 'idle' }))
    );

    const startTime = Date.now();
    const thoughtTimer = setInterval(() => {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId && msg.thinking?.isThinking
            ? {
                ...msg,
                thinking: {
                  ...msg.thinking,
                  durationSeconds: Math.floor((Date.now() - startTime) / 1000),
                },
              }
            : msg
        )
      );
    }, 1000);

    try {
      const stream = simulateLangGraphConsultationStream(promptText);

      for await (const event of stream) {
        if (streamAbortControllerRef.current) break;

        if (event.type === 'on_chain_start') {
          setLangGraphNodes((prev) =>
            prev.map((n) => (n.id === event.nodeId ? { ...n, state: 'running' } : n))
          );
          if (event.thought) {
            const thoughtStr = event.thought;
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantMessageId && m.thinking
                  ? { ...m, thinking: { ...m.thinking, thoughts: [...m.thinking.thoughts, thoughtStr] } }
                  : m
              )
            );
          }
        } else if (event.type === 'on_thinking_step') {
          if (event.thought) {
            const thoughtStr = event.thought;
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantMessageId && m.thinking
                  ? { ...m, thinking: { ...m.thinking, thoughts: [...m.thinking.thoughts, thoughtStr] } }
                  : m
              )
            );
          }
        } else if (event.type === 'on_tool_start') {
          const tool = event.tool as ToolCallItem;
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMessageId
                ? { ...m, toolCalls: [...(m.toolCalls || []), tool] }
                : m
            )
          );
        } else if (event.type === 'on_tool_end') {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMessageId
                ? {
                    ...m,
                    toolCalls: (m.toolCalls || []).map((t) =>
                      t.id === event.toolId
                        ? {
                            ...t,
                            status: 'completed',
                            outputResult: event.outputResult,
                            executionTimeMs: event.executionTimeMs,
                          }
                        : t
                    ),
                  }
                : m
            )
          );
        } else if (event.type === 'on_interrupt') {
          const approval = event.approval as ApprovalRequest;
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMessageId
                ? { ...m, approvalRequest: approval }
                : m
            )
          );
        } else if (event.type === 'on_chat_model_stream') {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMessageId
                ? {
                    ...m,
                    content: m.content + event.token,
                    recommendationIds: event.vehicles?.map((v) => v.id) || m.recommendationIds,
                    thinking: m.thinking ? { ...m.thinking, isThinking: false } : undefined,
                  }
                : m
            )
          );
          if (event.vehicles) {
            setVehicles(event.vehicles);
          }
        } else if (event.type === 'on_chain_end') {
          setLangGraphNodes((prev) =>
            prev.map((n) => ({ ...n, state: 'completed' }))
          );
        }
      }
    } catch (err) {
      console.error('Stream processing error:', err);
    } finally {
      clearInterval(thoughtTimer);
      setIsStreaming(false);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMessageId && m.thinking?.isThinking
            ? { ...m, thinking: { ...m.thinking, isThinking: false } }
            : m
        )
      );
    }
  }, [isStreaming]);

  const resetSession = useCallback(() => {
    const newId = `sess-${Date.now()}`;
    const newSession: ConsultationSession = {
      id: newId,
      title: 'New Consultation Session',
      date: 'Just now',
      vehicleCount: 0,
      status: 'active',
      lastMessageSnippet: 'Session started...',
    };
    setSessions((prev) => [newSession, ...prev]);
    setActiveSessionId(newId);
    setMessages([
      {
        id: `msg-${Date.now()}`,
        role: 'assistant',
        content: 'Started a fresh consultation session! What vehicle segment, budget, or key features would you like to explore today?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
    ]);
    setActiveTab('recommendations');
  }, []);

  return {
    sessions,
    activeSessionId,
    setActiveSessionId,
    messages,
    isStreaming,
    activeTab,
    setActiveTab,
    vehicles,
    shortlistedVehicleIds,
    selectedVehicleId,
    setSelectedVehicleId,
    toggleShortlist,
    profile,
    setProfile,
    langGraphNodes,
    submitPrompt,
    handleApprovalAction,
    resetSession,
  };
}
