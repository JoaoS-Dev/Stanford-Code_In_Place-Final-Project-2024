#!/usr/bin/env python3
"""
URL Image Alt Text Checker — versão single-file

Melhorias principais face ao protótipo original:
- Robusteza de rede: Session com User-Agent, timeouts e retries exponenciais.
- Parsing mais completo: <img>, atributos data-*, srcset, <picture>/<source> e URLs relativas resolvidas.
- Heurísticas WCAG úteis: marca problemas comuns (alt vazio, demasiado longo, igual ao ficheiro, duplicados, falta em links).
- UI responsiva: threading para não bloquear o tkinter; indicador de estado; duplo‑clique para abrir URL.
- Exportação: CSV e JSON com resumo e detalhes.

Requisitos (requirements.txt):
beautifulsoup4>=4.12
requests>=2.31

Como correr:
python url_alt_text_checker.py
"""
from __future__ import annotations

import csv
import json
import logging
import re
import threading
import time
import webbrowser
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter, Retry

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from tkinter import ttk
except Exception as e:  # pragma: no cover
    raise SystemExit("Este programa requer tkinter.") from e

# --------------- Configuração de logging ---------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)

USER_AGENT = "AltTextChecker/0.3 (+github.com/JoaoS-Dev)"
TIMEOUT = 12
RETRY_TOTAL = 3
RETRY_BACKOFF = 0.6
RETRY_STATUSES = (429, 500, 502, 503, 504)


# --------------- Modelo de dados ---------------
@dataclass
class ImgInfo:
    page_url: str
    src_url: str
    alt: Optional[str]
    in_link: bool
    role: Optional[str] = None
    issues: List[str] = field(default_factory=list)


# --------------- Rede ---------------

def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    retries = Retry(
        total=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=RETRY_STATUSES,
        allowed_methods=("GET", "HEAD"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def fetch_html(url: str) -> str:
    with make_session() as s:
        r = s.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        # requests irá detetar correctamente o encoding na maioria dos casos
        return r.text


# --------------- Parsing HTML ---------------

IMG_FILE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif")


def _first_from_srcset(srcset: str) -> Optional[str]:
    # Estratégia simples: escolhe o primeiro candidato do srcset
    if not srcset:
        return None
    parts = [p.strip() for p in srcset.split(",") if p.strip()]
    if not parts:
        return None
    first = parts[0].split()[0]
    return first or None


def _candidate_src(tag: Tag) -> Iterable[str]:
    # Devolve possíveis URLs de imagem a partir de um tag <img> ou <source>
    # 1) src e variantes data-*
    for attr in ("src", "data-src", "data-lazy-src", "data-original", "data-img"):
        val = tag.get(attr)
        if val and isinstance(val, str) and val.strip():
            yield val.strip()
    # 2) srcset
    srcset = tag.get("srcset")
    if isinstance(srcset, str):
        first = _first_from_srcset(srcset)
        if first:
            yield first
    # 3) CSS inline simples: background-image:url(...)
    style = tag.get("style")
    if isinstance(style, str) and "background-image" in style:
        m = re.search(r"background-image\s*:\s*url\(([^)]+)\)", style)
        if m:
            cand = m.group(1).strip('"\' ')
            if cand:
                yield cand


def iter_image_candidates(soup: BeautifulSoup, base_url: str) -> Iterable[Tuple[str, Tag, bool]]:
    # <img>
    for img in soup.find_all("img"):
        parent = img.parent
        in_link = bool(parent and isinstance(parent, Tag) and parent.name == "a")
        for cand in _candidate_src(img):
            yield urljoin(base_url, cand), img, in_link
    # <picture><source>
    for source in soup.find_all("source"):
        # Consideramos que o <img> associado terá o alt; o <source> não tem alt próprio
        parent = source.parent
        in_link = bool(parent and isinstance(parent, Tag) and parent.name == "a")
        for cand in _candidate_src(source):
            yield urljoin(base_url, cand), source, in_link


# --------------- Auditoria de ALT ---------------

MAX_ALT_LEN = 150


def audit_alt(tag: Tag, src_url: str, in_link: bool) -> Tuple[Optional[str], List[str]]:
    issues: List[str] = []
    alt: Optional[str] = None
    if tag.name == "img":
        raw_alt = tag.get("alt")
        alt = raw_alt.strip() if isinstance(raw_alt, str) else None
        if alt is None:
            issues.append("sem atributo alt")
        else:
            # alt existe (pode ser vazio)
            if alt == "":
                issues.append("alt vazio (verificar se é decorativa)")
            if len(alt) > MAX_ALT_LEN:
                issues.append("alt potencialmente demasiado longo")
            # igual ao nome do ficheiro
            path = urlparse(src_url).path.lower()
            fname = path.rsplit("/", 1)[-1]
            if fname and alt and alt.lower().strip().startswith(fname):
                issues.append("alt igual/semelhante ao nome do ficheiro")
    else:
        # <source> não possui alt; dependerá do <img> associado
        issues.append("fonte <source> sem alt (verificar <img> associado)")

    if in_link and (not alt or alt == ""):
        issues.append("imagem em link sem texto alternativo descritivo")

    return alt, issues


def analyze_url(url: str) -> Tuple[List[ImgInfo], dict]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    images: List[ImgInfo] = []
    seen_srcs = set()

    for src, tag, in_link in iter_image_candidates(soup, url):
        # Normalizar e evitar duplicados exatos
        key = (src, tag.name)
        if key in seen_srcs:
            continue
        seen_srcs.add(key)

        alt, issues = audit_alt(tag, src, in_link)
        images.append(
            ImgInfo(
                page_url=url,
                src_url=src,
                alt=alt,
                in_link=in_link,
                role=tag.get("role") if isinstance(tag.get("role"), str) else None,
                issues=issues,
            )
        )

    # Heurísticas adicionais: duplicados de alt
    alt_counts = {}
    for info in images:
        if info.alt:
            alt_counts[info.alt] = alt_counts.get(info.alt, 0) + 1
    for info in images:
        if info.alt and alt_counts.get(info.alt, 0) > 3:
            info.issues.append("alt muito repetido")

    summary = {
        "total": len(images),
        "com_alt": sum(1 for i in images if i.alt not in (None, "")),
        "sem_alt": sum(1 for i in images if i.alt is None),
        "alt_vazio": sum(1 for i in images if i.alt == ""),
        "em_link": sum(1 for i in images if i.in_link),
        "com_problemas": sum(1 for i in images if i.issues),
        "url": url,
    }
    return images, summary


# --------------- UI (tkinter) ---------------

class AltTextCheckerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("URL Image Alt Text Checker")
        self.root.geometry("1000x640")

        # Estado
        self._current_results: List[ImgInfo] = []
        self._current_summary: dict = {}
        self._worker: Optional[threading.Thread] = None
        self._stop_flag = threading.Event()

        self._build_widgets()

    def _build_widgets(self):
        frm_top = ttk.Frame(self.root, padding=10)
        frm_top.pack(fill=tk.X)

        ttk.Label(frm_top, text="URL da página:").pack(side=tk.LEFT)
        self.url_var = tk.StringVar()
        self.ent_url = ttk.Entry(frm_top, textvariable=self.url_var, width=80)
        self.ent_url.pack(side=tk.LEFT, padx=8)
        self.ent_url.insert(0, "https://example.com")

        self.btn_check = ttk.Button(frm_top, text="Analisar", command=self.on_analyze)
        self.btn_check.pack(side=tk.LEFT)

        self.lbl_status = ttk.Label(frm_top, text="Pronto")
        self.lbl_status.pack(side=tk.RIGHT)

        # Resumo
        self.txt_summary = tk.Text(self.root, height=5)
        self.txt_summary.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.txt_summary.configure(state=tk.DISABLED)

        # Tabela de resultados
        columns = ("#", "src_url", "alt", "issues", "in_link")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("#", text="#")
        self.tree.heading("src_url", text="Imagem (src)")
        self.tree.heading("alt", text="alt")
        self.tree.heading("issues", text="Problemas")
        self.tree.heading("in_link", text="Em link?")
        self.tree.column("#", width=40, anchor=tk.CENTER)
        self.tree.column("src_url", width=520)
        self.tree.column("alt", width=260)
        self.tree.column("issues", width=260)
        self.tree.column("in_link", width=80, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.tree.bind("<Double-1>", self.on_open_item)

        # Botões de exportação
        frm_bottom = ttk.Frame(self.root, padding=10)
        frm_bottom.pack(fill=tk.X)
        ttk.Button(frm_bottom, text="Exportar CSV", command=self.export_csv).pack(side=tk.LEFT)
        ttk.Button(frm_bottom, text="Exportar JSON", command=self.export_json).pack(side=tk.LEFT, padx=6)
        ttk.Button(frm_bottom, text="Abrir página", command=self.open_page).pack(side=tk.RIGHT)

    # ---------- Interações ----------
    def set_status(self, msg: str):
        self.lbl_status.configure(text=msg)
        self.root.update_idletasks()

    def on_analyze(self):
        url = self.url_var.get().strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            messagebox.showwarning("URL inválido", "Indica um URL completo, começando por http:// ou https://")
            return
        if self._worker and self._worker.is_alive():
            messagebox.showinfo("A decorrer", "Já existe uma análise em curso.")
            return

        self._stop_flag.clear()
        self.set_status("A analisar…")
        self.btn_check.configure(state=tk.DISABLED)
        self._current_results = []
        self._current_summary = {}
        self.tree.delete(*self.tree.get_children())
        self._clear_summary()

        self._worker = threading.Thread(target=self._analyze_worker, args=(url,), daemon=True)
        self._worker.start()
        self.root.after(150, self._poll_worker)

    def _poll_worker(self):
        if self._worker and self._worker.is_alive():
            self.root.after(200, self._poll_worker)
        else:
            self.btn_check.configure(state=tk.NORMAL)
            if self._current_results:
                self._render_results()
                self.set_status("Concluído")
            else:
                # Caso erro
                if not self._current_summary:
                    self.set_status("Falhou")

    def _analyze_worker(self, url: str):
        try:
            images, summary = analyze_url(url)
            self._current_results = images
            self._current_summary = summary
        except requests.exceptions.RequestException as e:
            logging.error("Erro de rede: %s", e)
            messagebox.showerror("Erro de rede", f"Ocorreu um erro ao obter a página:\n{e}")
        except Exception as e:  # pragma: no cover
            logging.exception("Erro inesperado")
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

    def _render_results(self):
        self.tree.delete(*self.tree.get_children())
        for idx, info in enumerate(self._current_results, start=1):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    idx,
                    info.src_url,
                    info.alt if info.alt is not None else "<sem alt>",
                    "; ".join(info.issues) if info.issues else "",
                    "sim" if info.in_link else "não",
                ),
            )
        self._show_summary()

    def _show_summary(self):
        s = self._current_summary or {}
        lines = [
            f"URL: {s.get('url','')}\n",
            f"Total de imagens: {s.get('total',0)}\n",
            f"Com alt: {s.get('com_alt',0)}\n",
            f"Sem alt (atributo): {s.get('sem_alt',0)}\n",
            f"alt vazio: {s.get('alt_vazio',0)}\n",
            f"Em links: {s.get('em_link',0)}\n",
            f"Com problemas: {s.get('com_problemas',0)}\n",
        ]
        self.txt_summary.configure(state=tk.NORMAL)
        self.txt_summary.delete("1.0", tk.END)
        self.txt_summary.insert("1.0", "".join(lines))
        self.txt_summary.configure(state=tk.DISABLED)

    def _clear_summary(self):
        self.txt_summary.configure(state=tk.NORMAL)
        self.txt_summary.delete("1.0", tk.END)
        self.txt_summary.configure(state=tk.DISABLED)

    def on_open_item(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        vals = self.tree.item(sel, "values")
        if not vals:
            return
        src_url = vals[1]
        webbrowser.open(src_url)

    def open_page(self):
        s = self._current_summary
        if s and s.get("url"):
            webbrowser.open(str(s["url"]))

    # ---------- Exportação ----------
    def export_csv(self):
        if not self._current_results:
            messagebox.showinfo("Sem dados", "Corre uma análise primeiro.")
            return
        fpath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", ".csv")],
            title="Guardar relatório CSV",
        )
        if not fpath:
            return
        with open(fpath, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["page_url", "src_url", "alt", "in_link", "issues"]) 
            for i in self._current_results:
                w.writerow([i.page_url, i.src_url, i.alt if i.alt is not None else "", int(i.in_link), "; ".join(i.issues)])
        messagebox.showinfo("Exportado", f"CSV guardado em:\n{fpath}")

    def export_json(self):
        if not self._current_results:
            messagebox.showinfo("Sem dados", "Corre uma análise primeiro.")
            return
        fpath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", ".json")],
            title="Guardar relatório JSON",
        )
        if not fpath:
            return
        payload = {
            "summary": self._current_summary,
            "results": [
                {
                    "page_url": i.page_url,
                    "src_url": i.src_url,
                    "alt": i.alt,
                    "in_link": i.in_link,
                    "role": i.role,
                    "issues": i.issues,
                }
                for i in self._current_results
            ],
        }
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Exportado", f"JSON guardado em:\n{fpath}")


def main():
    root = tk.Tk()
    app = AltTextCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
