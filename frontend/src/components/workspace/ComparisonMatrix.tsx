import React from 'react';
import type { Vehicle } from '../../types/agent';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Check, X, Sparkles, Layers } from 'lucide-react';

interface ComparisonMatrixProps {
  vehicles: Vehicle[];
  shortlistedIds: string[];
  onToggleShortlist: (vehicleId: string) => void;
}

export const ComparisonMatrix: React.FC<ComparisonMatrixProps> = ({
  vehicles,
  shortlistedIds,
  onToggleShortlist,
}) => {
  const comparedVehicles = vehicles.filter((v) => shortlistedIds.includes(v.id));

  if (comparedVehicles.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center border border-dashed border-border rounded-xl bg-card">
        <Layers className="w-8 h-8 text-muted-foreground mb-2" />
        <h4 className="text-sm font-semibold text-foreground">No Vehicles in Comparison Matrix</h4>
        <p className="text-xs text-muted-foreground max-w-sm mt-1 mb-4">
          Click "+ Add to Compare" on any vehicle card from the recommendations tab to analyze specs side-by-side.
        </p>
        <Button
          size="sm"
          variant="outline"
          onClick={() => {
            vehicles.slice(0, 3).forEach((v) => onToggleShortlist(v.id));
          }}
          className="text-xs gap-1.5"
        >
          <Sparkles className="w-3.5 h-3.5" /> Compare Top 3 Recommendations
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-foreground tracking-tight">
            Side-by-Side Comparison Matrix ({comparedVehicles.length} vehicles)
          </h3>
          <p className="text-xs text-muted-foreground">
            Multi-attribute evaluation across powertrain, dimensions, and financial metrics.
          </p>
        </div>

        {comparedVehicles.length < vehicles.length && (
          <Button
            size="xs"
            variant="ghost"
            onClick={() => {
              vehicles.forEach((v) => {
                if (!shortlistedIds.includes(v.id)) onToggleShortlist(v.id);
              });
            }}
            className="text-xs"
          >
            Add All Available
          </Button>
        )}
      </div>

      <div className="overflow-x-auto border border-border rounded-xl bg-card shadow-xs">
        <table className="w-full text-xs text-left border-collapse">
          <thead>
            <tr className="border-b border-border bg-muted/40 font-mono">
              <th className="p-3 font-semibold text-muted-foreground w-40">Attribute</th>
              {comparedVehicles.map((v) => (
                <th key={v.id} className="p-3 min-w-[200px] border-l border-border">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-foreground line-clamp-1">{v.make} {v.model}</span>
                    <button
                      onClick={() => onToggleShortlist(v.id)}
                      className="text-muted-foreground hover:text-destructive p-1 rounded transition-colors"
                      title="Remove from comparison"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  </div>
                  <div className="text-[11px] text-muted-foreground font-normal">{v.trim}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {/* Match Score */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20">Fuzzy Match Score</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border font-bold">
                  <Badge variant="default" className="text-xs">
                    {v.matchScore}% Match
                  </Badge>
                </td>
              ))}
            </tr>

            {/* Base MSRP */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20 font-mono">MSRP</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border font-bold font-mono text-foreground">
                  ${v.price.toLocaleString()}
                </td>
              ))}
            </tr>

            {/* Powertrain */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20">Powertrain</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border">
                  <Badge variant="outline">{v.powertrain}</Badge>
                </td>
              ))}
            </tr>

            {/* Range / Efficiency */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20">EPA Range / Economy</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border font-medium text-foreground">
                  {v.epaMpgOrRange}
                </td>
              ))}
            </tr>

            {/* 0-60 Time */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20">Acceleration (0-60)</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border font-mono">
                  {v.zeroToSixty}
                </td>
              ))}
            </tr>

            {/* Cargo Volume */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20">Cargo Capacity</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border font-medium">
                  {v.cargoVolumeCuFt} cu ft
                </td>
              ))}
            </tr>

            {/* Safety Rating */}
            <tr className="hover:bg-muted/20">
              <td className="p-3 font-medium text-foreground bg-muted/20">Safety Rating</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border text-emerald-600 dark:text-emerald-400 font-semibold">
                  {v.nhtsaOverallScore} ({v.safetyRatingStars}★)
                </td>
              ))}
            </tr>

            {/* 5 Year Estimated Ownership */}
            <tr className="hover:bg-muted/20 bg-muted/10">
              <td className="p-3 font-semibold text-foreground bg-muted/30 font-mono">5-Yr Total Cost</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border font-bold font-mono text-primary">
                  ${v.estimated5YearOwnershipCost.toLocaleString()}
                </td>
              ))}
            </tr>

            {/* Top Strengths */}
            <tr className="hover:bg-muted/20 align-top">
              <td className="p-3 font-medium text-foreground bg-muted/20">Key Strengths</td>
              {comparedVehicles.map((v) => (
                <td key={v.id} className="p-3 border-l border-border">
                  <ul className="space-y-1 text-[11px] text-muted-foreground">
                    {v.pros.map((p, idx) => (
                      <li key={idx} className="flex items-start gap-1">
                        <Check className="w-3 h-3 text-emerald-500 shrink-0 mt-0.5" />
                        <span>{p}</span>
                      </li>
                    ))}
                  </ul>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
