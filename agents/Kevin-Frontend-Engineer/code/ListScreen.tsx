import React from 'react';
import AppShell from './AppShell';
import Card from './Card';
import FAB from './FAB';
import PrimaryButton from './PrimaryButton';

interface Item {
  id: string;
  title: string;
  subtitle?: string;
}

interface ListScreenProps {
  items: Item[];
  onCreate?: () => void;
  onSelect?: (id: string) => void;
}

export const ListScreen: React.FC<ListScreenProps> = ({ items, onCreate, onSelect }) => {
  return (
    <AppShell title="List" onBack={undefined}>
      <div className="space-y-3">
        {items.map((it) => (
          <Card key={it.id} title={it.title} subtitle={it.subtitle} onClick={() => onSelect && onSelect(it.id)} />
        ))}
      </div>

      <div>
        <FAB icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>} label="Create" onClick={onCreate} />
      </div>

      <div className="mt-6">
        <PrimaryButton label="Primary action" onClick={() => alert('Primary clicked')} />
      </div>
    </AppShell>
  );
};

export default ListScreen;
