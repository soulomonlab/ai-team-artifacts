import React, {useState} from 'react';
import {Template, Draft} from './types';
import {createDraft} from './api';
import Templates from './Templates';
import Scheduling from './Scheduling';

interface ComposerProps {
  initialTemplateId?: string;
  onCreated?: (d: Draft) => void;
}

export default function Composer({initialTemplateId, onCreated}: ComposerProps) {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [template, setTemplate] = useState<Template | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSave(sendAt?: string) {
    setError(null);
    if (!title.trim()) return setError('제목은 필수입니다.');
    if (!body.trim()) return setError('본문은 필수입니다.');
    setIsSaving(true);
    try {
      const draft = await createDraft({title, body, templateId: template?.id, sendAt});
      onCreated?.(draft);
    } catch (e: any) {
      setError(e?.message || '저장 실패');
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-lg font-semibold mb-3">Composer</h2>
      <div className="grid gap-3">
        <input
          className="border px-2 py-1 rounded"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          aria-label="title"
        />
        <textarea
          className="border px-2 py-1 rounded h-32"
          placeholder="Body"
          value={body}
          onChange={(e) => setBody(e.target.value)}
          aria-label="body"
        />
        <div>
          <label className="block text-sm font-medium mb-1">Templates</label>
          <Templates
            selectedId={template?.id}
            onSelect={(t) => {
              setTemplate(t);
              if (t) {
                setTitle((s) => s || t.title);
                setBody((s) => s || t.body);
              }
            }}
          />
        </div>
        <Scheduling
          onSchedule={(sendAt) => handleSave(sendAt)}
          onSendNow={() => handleSave(undefined)}
        />
        {error && <div className="text-red-600">{error}</div>}
        <div className="flex gap-2">
          <button
            className="bg-blue-600 text-white px-3 py-1 rounded disabled:opacity-50"
            onClick={() => handleSave(undefined)}
            disabled={isSaving}
          >
            Save draft
          </button>
        </div>
      </div>
    </div>
  );
}
