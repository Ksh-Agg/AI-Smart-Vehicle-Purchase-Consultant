import React from 'react';
import type { UserPreferenceProfile, PowertrainType } from '../../types/agent';
import { Sliders, Shield, Fuel, Gauge, Box, Cpu, DollarSign, Save } from 'lucide-react';
import { Button } from '../ui/button';

interface IntakeProfileDrawerProps {
  profile: UserPreferenceProfile;
  onUpdateProfile: (updated: UserPreferenceProfile) => void;
  onRunConsultationWithProfile?: () => void;
}

const POWERTRAIN_OPTIONS: PowertrainType[] = ['EV', 'Hybrid', 'Plug-in Hybrid', 'Gasoline'];

export const IntakeProfileDrawer: React.FC<IntakeProfileDrawerProps> = ({
  profile,
  onUpdateProfile,
  onRunConsultationWithProfile,
}) => {
  const togglePowertrain = (pt: PowertrainType) => {
    const next = profile.preferredPowertrains.includes(pt)
      ? profile.preferredPowertrains.filter((p) => p !== pt)
      : [...profile.preferredPowertrains, pt];
    onUpdateProfile({ ...profile, preferredPowertrains: next });
  };

  const setPriority = (
    key: keyof UserPreferenceProfile['priorities'],
    level: 'Low' | 'Medium' | 'High'
  ) => {
    onUpdateProfile({
      ...profile,
      priorities: {
        ...profile.priorities,
        [key]: level,
      },
    });
  };

  return (
    <div className="space-y-5 text-xs">
      <div>
        <h3 className="text-sm font-bold text-foreground tracking-tight flex items-center gap-2">
          <Sliders className="w-4 h-4 text-primary" />
          Intake & Preference Weight Tuner
        </h3>
        <p className="text-xs text-muted-foreground">
          Calibrate dynamic bounds used by the Fuzzy Scoring Engine and Multi-Attribute Ranker.
        </p>
      </div>

      {/* Budget Constraints */}
      <div className="p-3.5 rounded-xl border border-border bg-card space-y-3">
        <div className="flex items-center justify-between">
          <label className="font-semibold text-foreground flex items-center gap-1.5">
            <DollarSign className="w-3.5 h-3.5 text-emerald-500" />
            Budget Range Ceiling
          </label>
          <span className="font-mono font-bold text-foreground">
            ${profile.budgetMin.toLocaleString()} - ${profile.budgetMax.toLocaleString()}
          </span>
        </div>

        <input
          type="range"
          min="25000"
          max="90000"
          step="2500"
          value={profile.budgetMax}
          onChange={(e) =>
            onUpdateProfile({ ...profile, budgetMax: Number(e.target.value) })
          }
          className="w-full accent-primary cursor-pointer"
        />
        <div className="flex justify-between text-[10px] text-muted-foreground font-mono">
          <span>$25k (Entry)</span>
          <span>$50k (Mainstream)</span>
          <span>$90k (Premium)</span>
        </div>
      </div>

      {/* Powertrain Preferences */}
      <div className="p-3.5 rounded-xl border border-border bg-card space-y-2.5">
        <label className="font-semibold text-foreground block">
          Acceptable Powertrains
        </label>
        <div className="grid grid-cols-2 gap-2">
          {POWERTRAIN_OPTIONS.map((pt) => {
            const isChecked = profile.preferredPowertrains.includes(pt);
            return (
              <button
                key={pt}
                type="button"
                onClick={() => togglePowertrain(pt)}
                className={`flex items-center justify-between p-2 rounded-lg border text-xs font-medium transition-colors ${
                  isChecked
                    ? 'border-primary bg-primary/10 text-primary'
                    : 'border-border bg-muted/30 text-muted-foreground hover:bg-muted/60'
                }`}
              >
                <span>{pt}</span>
                <span className={`w-2 h-2 rounded-full ${isChecked ? 'bg-primary' : 'bg-border'}`} />
              </button>
            );
          })}
        </div>
      </div>

      {/* Dynamic Fuzzy Priority Weights */}
      <div className="p-3.5 rounded-xl border border-border bg-card space-y-3">
        <label className="font-semibold text-foreground block">
          Fuzzy Scoring Weight Allocation
        </label>

        {/* Safety */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5 text-foreground/90">
            <Shield className="w-3.5 h-3.5 text-purple-500" />
            <span>Safety & Crash Protection</span>
          </div>
          <div className="flex items-center gap-1">
            {(['Low', 'Medium', 'High'] as const).map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setPriority('safety', lvl)}
                className={`px-2 py-0.5 rounded text-[10px] font-medium border transition-colors ${
                  profile.priorities.safety === lvl
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-muted text-muted-foreground border-border hover:bg-muted/80'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>

        {/* Fuel Economy / Efficiency */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5 text-foreground/90">
            <Fuel className="w-3.5 h-3.5 text-blue-500" />
            <span>Fuel Economy & Range</span>
          </div>
          <div className="flex items-center gap-1">
            {(['Low', 'Medium', 'High'] as const).map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setPriority('fuelEconomy', lvl)}
                className={`px-2 py-0.5 rounded text-[10px] font-medium border transition-colors ${
                  profile.priorities.fuelEconomy === lvl
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-muted text-muted-foreground border-border hover:bg-muted/80'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>

        {/* Cargo & Passenger Utility */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5 text-foreground/90">
            <Box className="w-3.5 h-3.5 text-amber-500" />
            <span>Cargo & Family Space</span>
          </div>
          <div className="flex items-center gap-1">
            {(['Low', 'Medium', 'High'] as const).map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setPriority('cargoSpace', lvl)}
                className={`px-2 py-0.5 rounded text-[10px] font-medium border transition-colors ${
                  profile.priorities.cargoSpace === lvl
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-muted text-muted-foreground border-border hover:bg-muted/80'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>

        {/* Performance & Acceleration */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5 text-foreground/90">
            <Gauge className="w-3.5 h-3.5 text-emerald-500" />
            <span>Performance & 0-60</span>
          </div>
          <div className="flex items-center gap-1">
            {(['Low', 'Medium', 'High'] as const).map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setPriority('performance', lvl)}
                className={`px-2 py-0.5 rounded text-[10px] font-medium border transition-colors ${
                  profile.priorities.performance === lvl
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-muted text-muted-foreground border-border hover:bg-muted/80'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>

        {/* Tech & Infotainment */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5 text-foreground/90">
            <Cpu className="w-3.5 h-3.5 text-indigo-500" />
            <span>Tech & Driver Assist</span>
          </div>
          <div className="flex items-center gap-1">
            {(['Low', 'Medium', 'High'] as const).map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setPriority('techFeatures', lvl)}
                className={`px-2 py-0.5 rounded text-[10px] font-medium border transition-colors ${
                  profile.priorities.techFeatures === lvl
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-muted text-muted-foreground border-border hover:bg-muted/80'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>
      </div>

      {onRunConsultationWithProfile && (
        <Button
          size="sm"
          onClick={onRunConsultationWithProfile}
          className="w-full gap-2 text-xs bg-primary text-primary-foreground hover:bg-primary/90"
        >
          <Save className="w-3.5 h-3.5" />
          Re-Score Catalogue with Updated Weights
        </Button>
      )}
    </div>
  );
};
