#!/usr/bin/env python3
"""Local desktop ingestion workbench for the ARK universal ingestion MVP.

Contract:
- Inputs: operator-selected local ChatGPT ZIP files and bounded query strings.
- Outputs: visible import/search/timeline/provenance/artifact views.
- Runtime constraint: all API calls are bounded by IngestionConfig.
- Memory assumption: GUI lists display at most configured query/result caps.
- Failure cases: invalid file, import failure, invalid query, and storage errors are
  shown as structured status text.
- Determinism: API results are deterministic except import timestamps.
"""

from __future__ import annotations

from pathlib import Path
import sys
from tkinter import BOTH, END, LEFT, RIGHT, Button, Entry, Frame, Label, Listbox, StringVar, Tk, filedialog, messagebox, ttk

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engines.ark.ingress.universal_ingestion import IngestionAPI, IngestionConfig

MAX_DISPLAY_ITEMS = 100


class IngestionWorkbench:
    """Small Tkinter frontend over the universal ingestion API."""

    def __init__(self, root: Tk, storage_root: Path) -> None:
        self._root = root
        self._api = IngestionAPI(storage_root, IngestionConfig(max_search_results=MAX_DISPLAY_ITEMS))
        self._status = StringVar(value="Ready")
        self._query = StringVar(value="")
        self._selected_rids: list[str] = []
        root.title("Wayfinder Ingestion Workbench")
        root.geometry("980x640")
        self._build()
        self._refresh_imports()

    def _build(self) -> None:
        top = Frame(self._root)
        top.pack(fill="x", padx=8, pady=8)
        Button(top, text="Import ChatGPT ZIP", command=self._select_and_import).pack(side=LEFT)
        Entry(top, textvariable=self._query, width=48).pack(side=LEFT, padx=8)
        Button(top, text="Search", command=self._search).pack(side=LEFT)
        Button(top, text="Timeline", command=self._timeline).pack(side=LEFT, padx=4)
        Label(top, textvariable=self._status).pack(side=RIGHT)

        panes = ttk.PanedWindow(self._root, orient="horizontal")
        panes.pack(fill=BOTH, expand=True, padx=8, pady=8)

        left = Frame(panes)
        right = Frame(panes)
        panes.add(left, weight=1)
        panes.add(right, weight=2)

        Label(left, text="Imports").pack(anchor="w")
        self._imports = Listbox(left, height=8)
        self._imports.pack(fill=BOTH, expand=False)
        Label(left, text="Artifacts").pack(anchor="w", pady=(8, 0))
        self._artifacts = Listbox(left)
        self._artifacts.pack(fill=BOTH, expand=True)

        Label(right, text="Observations").pack(anchor="w")
        self._observations = Listbox(right)
        self._observations.pack(fill=BOTH, expand=True)
        self._observations.bind("<<ListboxSelect>>", self._show_provenance)
        Label(right, text="Provenance").pack(anchor="w", pady=(8, 0))
        self._provenance = Listbox(right, height=8)
        self._provenance.pack(fill=BOTH, expand=False)

    def _select_and_import(self) -> None:
        selected = filedialog.askopenfilename(title="Select ChatGPT export ZIP", filetypes=(("ZIP files", "*.zip"), ("All files", "*.*")))
        if not selected:
            return
        self._status.set("Importing")
        self._root.update_idletasks()
        result = self._api.ingest("chatgpt", Path(selected))
        if result.status != "ok":
            reason = result.failure.reason if result.failure else "Unknown import failure"
            self._status.set("Import failed")
            messagebox.showerror("Import failed", reason)
            return
        self._status.set(f"Imported {len(result.observations)} observations")
        self._refresh_imports()
        self._refresh_artifacts()

    def _refresh_imports(self) -> None:
        self._imports.delete(0, END)
        imports = self._api.imports()
        limit = min(len(imports), MAX_DISPLAY_ITEMS)
        for index in range(limit):
            item = imports[index]
            stats = item.get("statistics", {})
            self._imports.insert(END, f"{item.get('import_id')} observations={stats.get('observations', 0)}")
        self._refresh_artifacts()

    def _refresh_artifacts(self) -> None:
        self._artifacts.delete(0, END)
        artifacts = self._api.artifacts()
        limit = min(len(artifacts), MAX_DISPLAY_ITEMS)
        for index in range(limit):
            item = artifacts[index]
            self._artifacts.insert(END, f"{item.get('rid')} {item.get('source_path')}")

    def _search(self) -> None:
        result = self._api.search(self._query.get())
        if result.status != "ok":
            self._status.set(result.failure.reason if result.failure else "Search failed")
            return
        self._load_observations(result.observations)
        self._status.set(f"Search returned {len(result.observations)} observations")

    def _timeline(self) -> None:
        query = self._query.get().strip() or None
        result = self._api.timeline(query)
        if result.status != "ok":
            self._status.set(result.failure.reason if result.failure else "Timeline failed")
            return
        self._load_observations(result.observations)
        self._status.set(f"Timeline loaded {len(result.observations)} observations")

    def _load_observations(self, observations) -> None:
        self._observations.delete(0, END)
        self._provenance.delete(0, END)
        self._selected_rids = []
        limit = min(len(observations), MAX_DISPLAY_ITEMS)
        for index in range(limit):
            item = observations[index]
            self._selected_rids.append(item.rid)
            self._observations.insert(END, f"{item.timestamp} {item.actor}: {item.content[:120]}")

    def _show_provenance(self, _event) -> None:
        selection = self._observations.curselection()
        self._provenance.delete(0, END)
        if not selection:
            return
        index = int(selection[0])
        if index >= len(self._selected_rids):
            return
        provenance = self._api.provenance(self._selected_rids[index])
        if not isinstance(provenance, dict):
            self._provenance.insert(END, str(provenance))
            return
        items = tuple(sorted(provenance.items()))
        limit = min(len(items), MAX_DISPLAY_ITEMS)
        for item_index in range(limit):
            key, value = items[item_index]
            self._provenance.insert(END, f"{key}: {value}")


def main() -> int:
    root = Tk()
    IngestionWorkbench(root, Path("ARK"))
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
