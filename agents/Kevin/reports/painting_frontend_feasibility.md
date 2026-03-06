Painting App — Frontend Feasibility & Implementation Notes

Purpose
- Short feasibility review for Task #117 (frontend implementation) based on output/design/painting_app_components.md.

Key conclusions (top line)
- Feasible to implement an offline-capable, performant painting experience in-browser using a tile-based canvas + IndexedDB blobs + WebGL/OffscreenCanvas for compositing.
- PSD export: two viable paths. Recommend Product/Tech decision (client-only vs server-side). See trade-offs below.

Constraints & facts that drove choices
- Browser storage: IndexedDB good for binary blobs; per-origin quota varies by browser and device. Recommend using navigator.storage.persist() and quota checks at runtime.
- Texture limits: WebGL max texture size commonly 16384 but varies by device; targeting <= 8192x8192 is safer across mobile and integrated GPUs.
- Memory: Keeping full-resolution ImageData for large canvases will OOM on low-end devices. Use tile/chunk strategy (e.g., 1024–4096 px tiles) to cap in-memory ImageData.
- OffscreenCanvas + WebGL/Worker: enables rendering/compositing off main thread and reduces jank. Falls back to 2D canvas where unsupported.

Recommended architecture (frontend)
1. Tile store in IndexedDB: store each tile as compressed PNG/WEBP blob + metadata (z-layer, transform, version).
2. In-memory LRU cache: hold N recent tiles in memory (configurable by device heuristics). Default cache cap ~100–200MB.
3. Renderer: WebGL compositor in OffscreenWorker that assembles visible tiles into a viewport FBO; fall back to Canvas2D.
4. Change log & sync: keep op-level change log (compact) for incremental sync and undo/redo; apply ops to tiles and checkpoint to IndexedDB.
5. Export: rasterize visible tiles to a final canvas at export time (server or client).

PSD export options (trade-offs)
- Client-only: Pros = works offline, no server cost, immediate. Cons = heavy memory/CPU; may fail for very large canvases or on mobile.
- Server-side: Pros = can handle larger canvases (server memory), generate PSD reliably, lighter client. Cons = requires upload, increases infra and privacy considerations.
- Recommended default: Implement client export for small/medium canvases (<= 8192), add server-side PSD endpoint for larger canvases. Use ag-psd or native image libraries server-side.

Performance & accessibility notes
- Use requestIdleCallback for background checkpointing.
- Ensure keyboard accessibility for tools and ARIA labels for controls.

Acceptance criteria for frontend MVP
- Tile-based painting with undo/redo, persistent storage to IndexedDB, viewport rendering with WebGL/OffscreenCanvas (fallback enabled), export to PNG client-side for target max canvas.

Estimates (rough)
- Frontend MVP (single dev): 3–4 weeks (core renderer, tiles, basic tools, IndexedDB persistence, client export).
- Add OffscreenCanvas/WebGL + optimizations: +1–2 weeks.
- Server PSD export endpoint (backend work + integration): backend 1 week + frontend integration 1 week.

Open questions (need Product/Tech answers)
- Offline-first: YES/NO? (affects sync & conflict model)
- PSD export approach: client-only vs server-side (or both). If server-side: provide size/format constraints and infra owner.
- Max canvas size target (recommend 8192x8192 default). If higher, frontend complexity and memory risk increase significantly.

Next steps for frontend
- Await Product/Tech decisions above.
- Once decided, I will produce a technical implementation PR and break into tickets (renderer, persistence, sync, export).

References & notes
- Use navigator.storage.persist() to request persistent storage where available.
- Consider using web-worker + transferable objects for tile ImageData.
