import React from 'react';
import { Check, Gauge, Luggage, Plus, ShieldCheck, Sparkles, Users } from 'lucide-react';
import type { Vehicle } from '../../types/agent';
import { Button } from '../ui/button';

interface VehicleCardProps {
  vehicle: Vehicle;
  isShortlisted: boolean;
  onToggleShortlist: (vehicleId: string) => void;
  onSelectVehicle?: (vehicleId: string) => void;
  isSelected?: boolean;
}

const inr = (value: number) => new Intl.NumberFormat('en-IN', {
  style: 'currency', currency: 'INR', maximumFractionDigits: 0,
}).format(value);

export const VehicleCard: React.FC<VehicleCardProps> = ({
  vehicle, isShortlisted, onToggleShortlist, onSelectVehicle, isSelected = false,
}) => (
  <article
    onClick={() => onSelectVehicle?.(vehicle.id)}
    className={`rounded-xl border bg-card shadow-sm transition-all cursor-pointer hover:border-primary/50 ${isSelected ? 'ring-2 ring-primary border-primary' : 'border-border'}`}
  >
    <div className="p-4 border-b border-border/60 bg-gradient-to-br from-primary/8 via-card to-card rounded-t-xl">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">{vehicle.year} · {vehicle.make}</p>
          <h3 className="text-base font-bold text-foreground">{vehicle.model} {vehicle.variantName}</h3>
          <p className="text-xs text-muted-foreground mt-0.5">{vehicle.fuelType.toUpperCase()} · {vehicle.transmissionType.replaceAll('_', ' ').toUpperCase()}</p>
        </div>
        <div className="text-right">
          <span className="inline-flex items-center gap-1 rounded-full border border-primary/30 bg-primary/10 px-2 py-1 text-xs font-bold text-primary">
            <Sparkles className="w-3 h-3" /> {vehicle.matchScore}%
          </span>
          <p className="font-mono font-bold mt-2">{inr(vehicle.price)}</p>
          <p className="text-[10px] text-muted-foreground">{vehicle.priceBasis === 'on_road' ? `On-road · ${vehicle.city}` : 'Provisional ex-showroom'}</p>
        </div>
      </div>
    </div>

    <div className="p-4 space-y-3">
      <div className="grid grid-cols-4 gap-2 rounded-lg bg-muted/40 border border-border/50 p-2 text-center">
        <div><Gauge className="w-3.5 h-3.5 text-blue-500 mx-auto" /><p className="text-[10px] text-muted-foreground mt-1">Efficiency</p><p className="text-[11px] font-semibold">{vehicle.efficiency}</p></div>
        <div><Luggage className="w-3.5 h-3.5 text-amber-500 mx-auto" /><p className="text-[10px] text-muted-foreground mt-1">Boot</p><p className="text-[11px] font-semibold">{vehicle.bootspaceLitres ? `${vehicle.bootspaceLitres} L` : 'Unknown'}</p></div>
        <div><Users className="w-3.5 h-3.5 text-indigo-500 mx-auto" /><p className="text-[10px] text-muted-foreground mt-1">Seats</p><p className="text-[11px] font-semibold">{vehicle.seatingCapacity ?? 'Unknown'}</p></div>
        <div><ShieldCheck className="w-3.5 h-3.5 text-emerald-500 mx-auto" /><p className="text-[10px] text-muted-foreground mt-1">Airbags</p><p className="text-[11px] font-semibold">{vehicle.airbagCount ?? 'Unknown'}</p></div>
      </div>

      <div className="grid grid-cols-3 gap-2">
        {Object.entries(vehicle.scoreBreakdown).slice(0, 6).map(([name, score]) => (
          <div key={name}>
            <div className="flex justify-between text-[9px] text-muted-foreground"><span className="capitalize">{name.replaceAll('_', ' ')}</span><span>{score}%</span></div>
            <div className="h-1.5 mt-1 rounded-full bg-muted overflow-hidden"><div className="h-full bg-primary" style={{ width: `${score}%` }} /></div>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap gap-1">
        {vehicle.pros.slice(0, 2).map((pro) => <span key={pro} className="inline-flex items-center gap-1 rounded-md bg-emerald-500/10 px-2 py-0.5 text-[10px] text-emerald-700 dark:text-emerald-300"><Check className="w-2.5 h-2.5" />{pro}</span>)}
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-border/50">
        <p className="text-[11px] text-muted-foreground font-mono">{vehicle.ownershipCost.years}-yr cost: <span className="font-semibold text-foreground">{inr(vehicle.ownershipCost.total_cost)}</span></p>
        <Button size="xs" variant={isShortlisted ? 'default' : 'outline'} onClick={(event) => { event.stopPropagation(); onToggleShortlist(vehicle.id); }} className="gap-1 text-xs">
          {isShortlisted ? <><Check className="w-3 h-3" /> Shortlisted</> : <><Plus className="w-3 h-3" /> Compare</>}
        </Button>
      </div>
    </div>
  </article>
);
