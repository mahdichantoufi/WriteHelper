import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from datetime import datetime
import os, sys

# Resolve path relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DICT_PATH = os.path.join(SCRIPT_DIR, "dictionary.py")

def load_phrases():
    """Load PHRASES dict from dictionary.py"""
    ns = {}
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        exec(f.read(), ns)
    return ns.get("PHRASES", {})

def resolve_code(phrases, code):
    """Resolve a code: if it's a group (list), expand recursively. Otherwise return the phrase."""
    val = phrases.get(code)
    if val is None:
        return [f"[Code inconnu: {code}]"]
    if isinstance(val, list):
        lines = []
        for sub in val:
            lines.extend(resolve_code(phrases, sub.strip().upper()))
        return lines
    return [val]

def save_phrases(phrases):
    """Write PHRASES dict back to dictionary.py"""
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        f.write("PHRASES = {\n")
        for code, phrase in phrases.items():
            escaped = phrase.replace("\\", "\\\\").replace('"', '\\"')
            f.write(f'    "{code}": "{escaped}",\n')
        f.write("}\n")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WriteHelper - M\u00e9decine L\u00e9gale")
        self.geometry("900x600")
        self.configure(bg="#f0f4f8")
        self.phrases = load_phrases()

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#f0f4f8")
        style.configure("TNotebook.Tab", padding=[12, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#4a90d9"), ("!selected", "#d0dce8")], foreground=[("selected", "white"), ("!selected", "#333")])
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#4a90d9", foreground="white")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.tab_view = ttk.Frame(notebook)
        self.tab_edit = ttk.Frame(notebook)
        self.tab_gen = ttk.Frame(notebook)

        notebook.add(self.tab_view, text="\U0001f4cb Dictionnaire")
        notebook.add(self.tab_edit, text="\u270f\ufe0f \u00c9diteur")
        notebook.add(self.tab_gen, text="\u26a1 G\u00e9n\u00e9rateur")

        self.build_view_tab()
        self.build_edit_tab()
        self.build_gen_tab()

    # --- TAB 1: VIEW ---
    def build_view_tab(self):
        search_frame = ttk.Frame(self.tab_view)
        search_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(search_frame, text="🔍 Rechercher :").pack(side="left")
        self.view_search = ttk.Entry(search_frame, width=40)
        self.view_search.pack(side="left", padx=5)
        self.view_search.bind("<KeyRelease>", lambda e: self.refresh_view())

        tree_frame = ttk.Frame(self.tab_view)
        tree_frame.pack(fill="both", expand=True)

        cols = ("Code", "Phrase")
        self.view_tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        self.view_tree.heading("Code", text="Code")
        self.view_tree.heading("Phrase", text="Phrase")
        self.view_tree.column("Code", width=80, minwidth=60)
        self.view_tree.column("Phrase", width=750)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.view_tree.yview)
        self.view_tree.configure(yscrollcommand=scrollbar.set)

        self.view_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.refresh_view()

    def refresh_view(self):
        self.view_tree.delete(*self.view_tree.get_children())
        query = self.view_search.get().strip().lower() if hasattr(self, 'view_search') else ""
        for code, phrase in self.phrases.items():
            display = str(phrase)
            if query and query not in code.lower() and query not in display.lower():
                continue
            self.view_tree.insert("", "end", values=(code, display))

    # --- TAB 2: EDIT ---
    def build_edit_tab(self):
        form = ttk.Frame(self.tab_edit)
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Code:").grid(row=0, column=0, sticky="w")
        self.edit_code = ttk.Entry(form, width=15)
        self.edit_code.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Phrase:").grid(row=0, column=2, sticky="w")
        self.edit_phrase = ttk.Entry(form, width=60)
        self.edit_phrase.grid(row=0, column=3, padx=5)

        ttk.Button(form, text="Ajouter / Modifier", command=self.add_or_update).grid(row=0, column=4, padx=5)
        ttk.Button(form, text="Supprimer", command=self.delete_entry).grid(row=0, column=5, padx=5)

        cols = ("Code", "Phrase")
        self.edit_tree = ttk.Treeview(self.tab_edit, columns=cols, show="headings")
        self.edit_tree.heading("Code", text="Code")
        self.edit_tree.heading("Phrase", text="Phrase")
        self.edit_tree.column("Code", width=80, minwidth=60)
        self.edit_tree.column("Phrase", width=750)
        self.edit_tree.pack(fill="both", expand=True, padx=10)
        self.edit_tree.bind("<<TreeviewSelect>>", self.on_edit_select)
        self.refresh_edit()

    def refresh_edit(self):
        self.edit_tree.delete(*self.edit_tree.get_children())
        for code, phrase in self.phrases.items():
            self.edit_tree.insert("", "end", values=(code, phrase))

    def on_edit_select(self, event):
        sel = self.edit_tree.selection()
        if sel:
            values = self.edit_tree.item(sel[0], "values")
            self.edit_code.delete(0, "end")
            self.edit_code.insert(0, values[0])
            self.edit_phrase.delete(0, "end")
            self.edit_phrase.insert(0, values[1])

    def validate_input(self, code, phrase):
        forbidden = ['"', "'", "\\", "{", "}", "`"]
        for ch in forbidden:
            if ch in code or ch in phrase:
                messagebox.showerror("Erreur", f"Caractère interdit détecté : {ch}\nCaractères interdits : {' '.join(forbidden)}")
                return False
        if not code or not phrase:
            messagebox.showwarning("Erreur", "Le code et la phrase ne peuvent pas être vides.")
            return False
        return True

    def add_or_update(self):
        code = self.edit_code.get().strip().upper()
        phrase = self.edit_phrase.get().strip()
        if not self.validate_input(code, phrase):
            return
        if code in self.phrases:
            if not messagebox.askyesno("Confirmation", f"Le code '{code}' existe déjà.\nVoulez-vous écraser la phrase existante ?"):
                return
        self.phrases[code] = phrase
        save_phrases(self.phrases)
        self.refresh_edit()
        self.refresh_view()

    def delete_entry(self):
        code = self.edit_code.get().strip().upper()
        if code not in self.phrases:
            messagebox.showwarning("Erreur", f"Le code '{code}' n'existe pas.")
            return
        if not messagebox.askyesno("Confirmation", f"Supprimer définitivement le code '{code}' ?\n\n{self.phrases[code]}"):
            return
        del self.phrases[code]
        save_phrases(self.phrases)
        self.refresh_edit()
        self.refresh_view()
        self.edit_code.delete(0, "end")
        self.edit_phrase.delete(0, "end")

    # --- TAB 3: GENERATOR ---
    def build_gen_tab(self):
        top = ttk.Frame(self.tab_gen)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(top, text="Codes (séparés par -):").pack(side="left")
        self.gen_input = ttk.Entry(top, width=60)
        self.gen_input.pack(side="left", padx=10)
        self.gen_input.bind("<KeyRelease>", self.update_preview)

        ttk.Button(top, text="Copier", command=self.copy_output).pack(side="left")
        ttk.Button(top, text="Sauvegarder", command=self.save_output).pack(side="left", padx=5)
        ttk.Button(top, text="Effacer", command=self.clear_gen).pack(side="left", padx=5)

        # Code picker + preview side by side
        body = ttk.Frame(self.tab_gen)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left: code list to click
        picker_frame = ttk.Frame(body)
        picker_frame.pack(side="left", fill="y", padx=(0, 5))

        ttk.Label(picker_frame, text="Cliquer pour ajouter :").pack(anchor="w")
        self.gen_search = ttk.Entry(picker_frame, width=20)
        self.gen_search.pack(fill="x", pady=2)
        self.gen_search.bind("<KeyRelease>", lambda e: self.refresh_picker())

        picker_scroll = ttk.Scrollbar(picker_frame, orient="vertical")
        self.picker_list = tk.Listbox(picker_frame, width=25, font=("Segoe UI", 9), yscrollcommand=picker_scroll.set)
        picker_scroll.config(command=self.picker_list.yview)
        self.picker_list.pack(side="left", fill="both", expand=True)
        picker_scroll.pack(side="right", fill="y")
        self.picker_list.bind("<Double-1>", self.on_picker_click)
        self.refresh_picker()

        # Right: preview
        self.preview = tk.Text(body, wrap="word", state="disabled", height=20)
        self.preview.pack(side="left", fill="both", expand=True)

        self.bind("<Control-c>", lambda e: self.copy_output())

    def refresh_picker(self):
        self.picker_list.delete(0, "end")
        query = self.gen_search.get().strip().lower()
        for code, phrase in self.phrases.items():
            display = f"{code} - {phrase}" if isinstance(phrase, str) else f"{code} (groupe)"
            if query and query not in code.lower() and query not in display.lower():
                continue
            self.picker_list.insert("end", display)

    def on_picker_click(self, event):
        sel = self.picker_list.curselection()
        if not sel:
            return
        code = self.picker_list.get(sel[0]).split(" - ")[0].split(" (")[0].strip()
        current = self.gen_input.get().strip()
        if current:
            self.gen_input.insert("end", f"-{code}")
        else:
            self.gen_input.insert(0, code)
        self.update_preview()

    def get_output(self):
        codes = self.gen_input.get().strip().split("-")
        lines = []
        for code in codes:
            code = code.strip().upper()
            if not code:
                continue
            for phrase in resolve_code(self.phrases, code):
                lines.append(f"• {phrase}")
        return "\n".join(lines)

    def update_preview(self, event=None):
        output = self.get_output()
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", output)
        self.preview.config(state="disabled")

    def clear_gen(self):
        self.gen_input.delete(0, "end")
        self.update_preview()

    def copy_output(self, event=None):
        output = self.get_output()
        if not output:
            return
        pyperclip.copy(output)
        messagebox.showinfo("WriteHelper", "Copié dans le presse-papier !")

    def save_output(self):
        output = self.get_output()
        if not output:
            return
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt")],
            initialfile=datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        )
        if not filename:
            return
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)
        messagebox.showinfo("WriteHelper", f"Sauvegardé: {os.path.basename(filename)}")

if __name__ == "__main__":
    App().mainloop()
