import { useState, useEffect } from 'react';
import { useAgentWorkspace } from './hooks/useAgentWorkspace';
import { Sidebar } from './components/workspace/Sidebar';
import { ChatArea } from './components/workspace/ChatArea';
import { InspectorCanvas } from './components/workspace/InspectorCanvas';

export default function App() {
  const [isDark, setIsDark] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return (
        localStorage.getItem('svpc-theme') === 'dark' ||
        (!localStorage.getItem('svpc-theme') &&
          window.matchMedia('(prefers-color-scheme: dark)').matches)
      );
    }
    return false;
  });

  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isCanvasCollapsed, setIsCanvasCollapsed] = useState(false);

  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      localStorage.setItem('svpc-theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('svpc-theme', 'light');
    }
  }, [isDark]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const activeTag = (document.activeElement?.tagName || '').toLowerCase();
      const isEditable =
        activeTag === 'input' ||
        activeTag === 'textarea' ||
        (document.activeElement as HTMLElement)?.isContentEditable;

      if (!isEditable && (e.key === 'd' || e.key === 'D') && !e.metaKey && !e.ctrlKey && !e.altKey) {
        e.preventDefault();
        setIsDark((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const {
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
  } = useAgentWorkspace();

  const handleRunConsultationWithProfile = () => {
    submitPrompt(
      `Recommend Maruti Suzuki cars in ${profile.city} within a hard on-road budget of ₹${profile.maxBudget.toLocaleString('en-IN')}. ` +
      `Preferred fuels: ${profile.preferredFuels.join(', ') || 'any'}; transmissions: ${profile.preferredTransmissions.join(', ') || 'any'}. ` +
      `Annual driving is ${profile.annualDistanceKm.toLocaleString('en-IN')} km for ${profile.ownershipYears} years.`
    );
    setActiveTab('recommendations');
    if (isCanvasCollapsed) setIsCanvasCollapsed(false);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground font-sans antialiased select-none">
      {/* Left Sidebar */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={setActiveSessionId}
        onNewSession={resetSession}
        profile={profile}
        onOpenProfileTuner={() => {
          setActiveTab('profile');
          if (isCanvasCollapsed) setIsCanvasCollapsed(false);
        }}
        isDark={isDark}
        onToggleTheme={() => setIsDark(!isDark)}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
      />

      {/* Center Chat Stream & Workspace Interaction */}
      <div className="flex-1 flex flex-col min-w-0 h-full">
        <ChatArea
          messages={messages}
          isStreaming={isStreaming}
          onSubmitPrompt={submitPrompt}
          onApprovalAction={handleApprovalAction}
          onToggleCanvas={() => setIsCanvasCollapsed(!isCanvasCollapsed)}
          isCanvasCollapsed={isCanvasCollapsed}
        />
      </div>

      {/* Right Canvas: Recommendations / Compare Matrix / LangGraph Workflow / Intake Tuner */}
      <div
        className={`h-full hidden md:flex flex-col shrink-0 transition-all duration-200 ${
          isCanvasCollapsed
            ? 'w-14'
            : 'w-[420px] lg:w-[480px] xl:w-[520px]'
        }`}
      >
        <InspectorCanvas
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          vehicles={vehicles}
          shortlistedIds={shortlistedVehicleIds}
          selectedVehicleId={selectedVehicleId}
          setSelectedVehicleId={setSelectedVehicleId}
          onToggleShortlist={toggleShortlist}
          langGraphNodes={langGraphNodes}
          profile={profile}
          onUpdateProfile={setProfile}
          onRunConsultationWithProfile={handleRunConsultationWithProfile}
          isCollapsed={isCanvasCollapsed}
          onToggleCollapse={() => setIsCanvasCollapsed(!isCanvasCollapsed)}
        />
      </div>
    </div>
  );
}
