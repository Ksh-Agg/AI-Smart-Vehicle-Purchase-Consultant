import React from 'react';
import { IndianRupee, MapPin, Sliders } from 'lucide-react';
import type { FuelType, Priority, TransmissionType, UserPreferenceProfile } from '../../types/agent';
import { Button } from '../ui/button';

interface IntakeProfileDrawerProps {
  profile: UserPreferenceProfile;
  onUpdateProfile: (updated: UserPreferenceProfile) => void;
  onRunConsultationWithProfile?: () => void;
}

const FUELS: FuelType[] = ['petrol', 'cng', 'hybrid', 'electric'];
const TRANSMISSIONS: TransmissionType[] = ['manual', 'automatic', 'amt', 'torque_converter', 'e_cvt'];
const PRIORITIES: Array<[keyof UserPreferenceProfile['priorities'], string]> = [
  ['safety', 'Safety'], ['efficiency', 'Efficiency'], ['space', 'Space'], ['performance', 'Performance'], ['features', 'Features'],
];

export const IntakeProfileDrawer: React.FC<IntakeProfileDrawerProps> = ({ profile, onUpdateProfile, onRunConsultationWithProfile }) => {
  const toggle = <T,>(items: T[], value: T) => items.includes(value) ? items.filter((item) => item !== value) : [...items, value];
  const setPriority = (key: keyof UserPreferenceProfile['priorities'], value: Priority) => onUpdateProfile({ ...profile, priorities: { ...profile.priorities, [key]: value } });
  return (
    <div className="space-y-4 text-xs">
      <div><h3 className="flex items-center gap-2 text-sm font-bold"><Sliders className="w-4 h-4 text-primary" /> Purchase profile</h3><p className="text-muted-foreground">City and maximum on-road budget are the only required fields.</p></div>
      <section className="p-3 rounded-xl border border-border bg-card space-y-3">
        <label className="font-semibold flex items-center gap-1"><MapPin className="w-3.5 h-3.5" /> City</label>
        <input value={profile.city} onChange={(event) => onUpdateProfile({ ...profile, city: event.target.value })} placeholder="e.g. Pune" className="w-full rounded-md border border-border bg-background px-3 py-2 outline-none focus:ring-2 focus:ring-primary/30" />
        <div className="flex justify-between"><label className="font-semibold flex items-center gap-1"><IndianRupee className="w-3.5 h-3.5" /> Maximum budget</label><span className="font-mono font-bold">{profile.maxBudget ? `₹${profile.maxBudget.toLocaleString('en-IN')}` : 'Not set'}</span></div>
        <input type="range" min="300000" max="3000000" step="50000" value={profile.maxBudget} onChange={(event) => onUpdateProfile({ ...profile, maxBudget: Number(event.target.value) })} className="w-full accent-primary" />
      </section>
      <section className="p-3 rounded-xl border border-border bg-card space-y-2"><label className="font-semibold">Preferred fuels</label><div className="flex flex-wrap gap-2">{FUELS.map((fuel) => <button key={fuel} type="button" onClick={() => onUpdateProfile({ ...profile, preferredFuels: toggle(profile.preferredFuels, fuel) })} className={`rounded-md border px-2 py-1 capitalize ${profile.preferredFuels.includes(fuel) ? 'border-primary bg-primary/10 text-primary' : 'border-border'}`}>{fuel}</button>)}</div></section>
      <section className="p-3 rounded-xl border border-border bg-card space-y-2"><label className="font-semibold">Preferred transmissions</label><div className="flex flex-wrap gap-2">{TRANSMISSIONS.map((transmission) => <button key={transmission} type="button" onClick={() => onUpdateProfile({ ...profile, preferredTransmissions: toggle(profile.preferredTransmissions, transmission) })} className={`rounded-md border px-2 py-1 capitalize ${profile.preferredTransmissions.includes(transmission) ? 'border-primary bg-primary/10 text-primary' : 'border-border'}`}>{transmission.replaceAll('_', ' ')}</button>)}</div></section>
      <section className="grid grid-cols-3 gap-2 p-3 rounded-xl border border-border bg-card">
        <label>Annual km<input type="number" min="1000" step="1000" value={profile.annualDistanceKm} onChange={(event) => onUpdateProfile({ ...profile, annualDistanceKm: Number(event.target.value) })} className="mt-1 w-full rounded border border-border bg-background p-2" /></label>
        <label>Years<input type="number" min="1" max="15" value={profile.ownershipYears} onChange={(event) => onUpdateProfile({ ...profile, ownershipYears: Number(event.target.value) })} className="mt-1 w-full rounded border border-border bg-background p-2" /></label>
        <label>Hard seats<input type="number" min="1" max="20" value={profile.mandatorySeats || ''} onChange={(event) => onUpdateProfile({ ...profile, mandatorySeats: event.target.value ? Number(event.target.value) : undefined })} className="mt-1 w-full rounded border border-border bg-background p-2" /></label>
      </section>
      <section className="p-3 rounded-xl border border-border bg-card space-y-3">{PRIORITIES.map(([key, label]) => <div key={key} className="flex items-center justify-between"><span className="font-medium">{label}</span><div className="flex gap-1">{(['low', 'medium', 'high'] as Priority[]).map((value) => <button key={value} type="button" onClick={() => setPriority(key, value)} className={`rounded border px-2 py-0.5 capitalize ${profile.priorities[key] === value ? 'border-primary bg-primary text-primary-foreground' : 'border-border'}`}>{value}</button>)}</div></div>)}</section>
      <Button className="w-full" onClick={onRunConsultationWithProfile} disabled={!profile.city.trim() || !profile.maxBudget}>Run consultation</Button>
    </div>
  );
};
