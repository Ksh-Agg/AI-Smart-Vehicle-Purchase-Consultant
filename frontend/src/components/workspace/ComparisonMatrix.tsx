import React from 'react';
import { Layers, Sparkles, X } from 'lucide-react';
import type { Vehicle } from '../../types/agent';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

interface ComparisonMatrixProps {
  vehicles: Vehicle[];
  shortlistedIds: string[];
  onToggleShortlist: (vehicleId: string) => void;
}

const inr = (value: number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(value);

export const ComparisonMatrix: React.FC<ComparisonMatrixProps> = ({ vehicles, shortlistedIds, onToggleShortlist }) => {
  const compared = vehicles.filter((vehicle) => shortlistedIds.includes(vehicle.id));
  if (!compared.length) return (
    <div className="flex flex-col items-center justify-center p-8 text-center border border-dashed border-border rounded-xl bg-card">
      <Layers className="w-8 h-8 text-muted-foreground mb-2" />
      <h4 className="text-sm font-semibold">No vehicles selected</h4>
      <p className="text-xs text-muted-foreground mt-1 mb-4">Add recommendation cards to compare current Indian-market facts.</p>
      <Button size="sm" variant="outline" onClick={() => vehicles.slice(0, 3).forEach((vehicle) => onToggleShortlist(vehicle.id))}><Sparkles className="w-3.5 h-3.5" /> Compare top 3</Button>
    </div>
  );
  const rows: Array<[string, (vehicle: Vehicle) => React.ReactNode]> = [
    ['Match', (vehicle) => <Badge>{vehicle.matchScore}%</Badge>],
    ['City price', (vehicle) => inr(vehicle.price)],
    ['Price basis', (vehicle) => vehicle.priceBasis.replaceAll('_', ' ')],
    ['Fuel', (vehicle) => vehicle.fuelType.toUpperCase()],
    ['Transmission', (vehicle) => vehicle.transmissionType.replaceAll('_', ' ')],
    ['Efficiency', (vehicle) => vehicle.efficiency],
    ['Power', (vehicle) => vehicle.powerBhp ? `${vehicle.powerBhp} bhp` : 'Unknown'],
    ['Boot space', (vehicle) => vehicle.bootspaceLitres ? `${vehicle.bootspaceLitres} L` : 'Unknown'],
    ['Seats', (vehicle) => vehicle.seatingCapacity ?? 'Unknown'],
    ['Airbags', (vehicle) => vehicle.airbagCount ?? 'Unknown'],
    ['Ownership cost', (vehicle) => inr(vehicle.ownershipCost.total_cost)],
    ['Evidence confidence', (vehicle) => `${Math.round(vehicle.confidence * 100)}%`],
  ];
  return (
    <div className="overflow-x-auto border border-border rounded-xl bg-card">
      <table className="w-full text-xs border-collapse">
        <thead><tr className="bg-muted/40 border-b border-border"><th className="p-3 text-left">Attribute</th>{compared.map((vehicle) => <th key={vehicle.id} className="p-3 min-w-48 border-l border-border text-left"><div className="flex justify-between gap-2"><span>{vehicle.model} {vehicle.variantName}</span><button onClick={() => onToggleShortlist(vehicle.id)} aria-label="Remove from comparison"><X className="w-3.5 h-3.5" /></button></div></th>)}</tr></thead>
        <tbody>{rows.map(([label, value]) => <tr key={label} className="border-b border-border/60 last:border-0"><td className="p-3 bg-muted/20 font-medium">{label}</td>{compared.map((vehicle) => <td key={vehicle.id} className="p-3 border-l border-border">{value(vehicle)}</td>)}</tr>)}</tbody>
      </table>
    </div>
  );
};
