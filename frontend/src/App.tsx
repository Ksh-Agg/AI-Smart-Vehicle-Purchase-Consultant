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
      `Re-score catalogue vehicles for budget ceiling $${profile.budgetMax.toLocaleString()} with ${profile.preferredPowertrains.join(
        ' & '
      )} powertrains prioritizing Safety (${profile.priorities.safety}), Cargo (${profile.priorities.cargoSpace}), and Efficiency (${profile.priorities.fuelEconomy}).`
    );
    setActiveTab('recommendations');
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
        onOpenProfileTuner={() => setActiveTab('profile')}
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
          onViewRecommendationsTab={() => setActiveTab('recommendations')}
        />
      </div>

      {/* Right Canvas: Recommendations / Compare Matrix / LangGraph Workflow / Intake Tuner */}
      <div className="w-[420px] lg:w-[480px] xl:w-[520px] h-full hidden md:flex flex-col shrink-0">
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
        />
      </div>
    </div>
  );
}