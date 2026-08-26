import React from 'react';
import { ShieldCheck, BatteryCharging, Gauge, Box, Check, Plus, Star, Sparkles } from 'lucide-react';
import type { Vehicle } from '../../types/agent';
import { Button } from '../ui/button';

interface VehicleCardProps {
  vehicle: Vehicle;
  isShortlisted: boolean;
  onToggleShortlist: (vehicleId: string) => void;
  onSelectVehicle?: (vehicleId: string) => void;
  isSelected?: boolean;
}

export const VehicleCard: React.FC<VehicleCardProps> = ({
  vehicle,
  isShortlisted,
  onToggleShortlist,
  onSelectVehicle,
  isSelected = false,
}) => {
  const getScoreBadgeColor = (score: number) => {
    if (score >= 90) return 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30';
    if (score >= 80) return 'bg-blue-500/15 text-blue-600 dark:text-blue-400 border-blue-500/30';
    return 'bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30';
  };

  return (
    <div
      onClick={() => onSelectVehicle?.(vehicle.id)}
      className={`relative rounded-xl border bg-card text-card-foreground shadow-sm transition-all overflow-hidden cursor-pointer hover:border-primary/50 hover:shadow-md ${
        isSelected ? 'ring-2 ring-primary border-primary' : 'border-border'
      }`}
    >
      {/* Header Banner with Image & Badges */}
      <div className="relative h-44 w-full bg-muted/60 overflow-hidden">
        <img
          src={vehicle.imageUrl}
          alt={`${vehicle.year} ${vehicle.make} ${vehicle.model}`}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/20 to-transparent" />

        {/* Top Badges */}
        <div className="absolute top-2.5 left-2.5 flex items-center gap-1.5">
          <span className="px-2 py-0.5 rounded-full bg-background/85 backdrop-blur-xs text-[11px] font-semibold text-foreground border border-border/60">
            {vehicle.powertrain}
          </span>
          <span className="px-2 py-0.5 rounded-full bg-background/85 backdrop-blur-xs text-[11px] font-medium text-muted-foreground border border-border/60">
            {vehicle.trim}
          </span>
        </div>

        <div className="absolute top-2.5 right-2.5 flex items-center gap-1.5">
          <div
            className={`px-2.5 py-1 rounded-full text-xs font-bold border backdrop-blur-xs flex items-center gap-1 ${getScoreBadgeColor(
              vehicle.matchScore
            )}`}
          >
            <Sparkles className="w-3 h-3" />
            <span>{vehicle.matchScore}% Match</span>
          </div>
        </div>

        {/* Bottom Title on Image */}
        <div className="absolute bottom-2.5 left-3 right-3 flex items-end justify-between">
          <div>
            <span className="text-xs text-muted-foreground font-mono">{vehicle.year} {vehicle.make}</span>
            <h3 className="text-base font-bold text-foreground tracking-tight line-clamp-1">
              {vehicle.model}
            </h3>
          </div>
          <div className="text-right">
            <span className="text-[10px] text-muted-foreground uppercase font-mono">MSRP</span>
            <div className="text-base font-extrabold text-foreground font-mono">
              ${vehicle.price.toLocaleString()}
            </div>
          </div>
        </div>
      </div>

      {/* Spec Attributes Grid */}
      <div className="p-3.5 space-y-3">
        <div className="grid grid-cols-4 gap-2 text-center bg-muted/40 p-2 rounded-lg border border-border/50">
          <div className="flex flex-col items-center">
            <BatteryCharging className="w-3.5 h-3.5 text-primary mb-0.5" />
            <span className="text-[10px] text-muted-foreground uppercase font-mono">Range/MPG</span>
            <span className="text-xs font-semibold text-foreground truncate w-full text-center">
              {vehicle.epaMpgOrRange.split(' ')[0]}
            </span>
          </div>

          <div className="flex flex-col items-center">
            <Gauge className="w-3.5 h-3.5 text-amber-500 mb-0.5" />
            <span className="text-[10px] text-muted-foreground uppercase font-mono">0-60 MPH</span>
            <span className="text-xs font-semibold text-foreground">{vehicle.zeroToSixty}</span>
          </div>

          <div className="flex flex-col items-center">
            <Box className="w-3.5 h-3.5 text-blue-500 mb-0.5" />
            <span className="text-[10px] text-muted-foreground uppercase font-mono">Cargo</span>
            <span className="text-xs font-semibold text-foreground">{vehicle.cargoVolumeCuFt} cu ft</span>
          </div>

          <div className="flex flex-col items-center">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500 mb-0.5" />
            <span className="text-[10px] text-muted-foreground uppercase font-mono">Safety</span>
            <div className="flex items-center text-xs font-semibold text-foreground">
              <span>{vehicle.safetyRatingStars}</span>
              <Star className="w-3 h-3 fill-amber-400 text-amber-400 ml-0.5" />
            </div>
          </div>
        </div>

        {/* Fuzzy Multi-Attribute Score Bars */}
        <div className="space-y-1.5 pt-1">
          <div className="flex justify-between text-[11px] text-muted-foreground font-mono">
            <span>Fuzzy Scoring Multi-Attribute Fit</span>
            <span className="font-semibold text-foreground">{vehicle.matchScore}/100</span>
          </div>
          <div className="grid grid-cols-5 gap-1.5">
            <div>
              <div className="flex justify-between text-[9px] text-muted-foreground mb-0.5">
                <span>Budget</span>
                <span>{vehicle.fuzzyMatchBreakdown.budgetScore}%</span>
              </div>
              <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${vehicle.fuzzyMatchBreakdown.budgetScore}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[9px] text-muted-foreground mb-0.5">
                <span>Efficiency</span>
                <span>{vehicle.fuzzyMatchBreakdown.efficiencyScore}%</span>
              </div>
              <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: `${vehicle.fuzzyMatchBreakdown.efficiencyScore}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[9px] text-muted-foreground mb-0.5">
                <span>Space</span>
                <span>{vehicle.fuzzyMatchBreakdown.spaceScore}%</span>
              </div>
              <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${vehicle.fuzzyMatchBreakdown.spaceScore}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[9px] text-muted-foreground mb-0.5">
                <span>Speed</span>
                <span>{vehicle.fuzzyMatchBreakdown.performanceScore}%</span>
              </div>
              <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: `${vehicle.fuzzyMatchBreakdown.performanceScore}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[9px] text-muted-foreground mb-0.5">
                <span>Safety</span>
                <span>{vehicle.fuzzyMatchBreakdown.safetyScore}%</span>
              </div>
              <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                <div className="h-full bg-purple-500 rounded-full" style={{ width: `${vehicle.fuzzyMatchBreakdown.safetyScore}%` }} />
              </div>
            </div>
          </div>
        </div>

        {/* Pros tags */}
        <div className="flex flex-wrap gap-1 pt-1">
          {vehicle.pros.slice(0, 2).map((pro, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 font-medium"
            >
              <Check className="w-2.5 h-2.5" />
              <span className="truncate max-w-[200px]">{pro}</span>
            </span>
          ))}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-2 border-t border-border/50">
          <div className="text-[11px] text-muted-foreground font-mono">
            5-Yr Est: <span className="font-semibold text-foreground">${vehicle.estimated5YearOwnershipCost.toLocaleString()}</span>
          </div>

          <Button
            size="xs"
            variant={isShortlisted ? 'default' : 'outline'}
            onClick={(e) => {
              e.stopPropagation();
              onToggleShortlist(vehicle.id);
            }}
            className="gap-1 text-xs"
          >
            {isShortlisted ? (
              <>
                <Check className="w-3 h-3" /> Shortlisted
              </>
            ) : (
              <>
                <Plus className="w-3 h-3" /> Add to Compare
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};
