import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
from datetime import datetime
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DICT_PATH = os.path.join(SCRIPT_DIR, "dictionary.py")

def load_data():
    ns = {}
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        exec(f.read(), ns)
    phrases = dict(sorted(ns.get("PHRASES", {}).items()))
    groups = dict(sorted(ns.get("GROUPS", {}).items()))
    return phrases, groups

def save_data(phrases, groups):
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        f.write("# Dictionnaire de phrases pour comptes rendus de médecine légale\n\n")
        f.write("PHRASES = {\n")
        for code, phrase in phrases.items():
            escaped = phrase.replace("\\", "\\\\").replace('"', '\\"')
            f.write(f'    "{code}": "{escaped}",\n')
        f.write("}\n\n")
        f.write("# --- GROUPES (PARAGRAPHES) ---\n")
        f.write("GROUPS = {\n")
        for code, codes_list in groups.items():
            f.write(f'    "{code}": {codes_list},\n')
        f.write("}\n")

def resolve_code(phrases, groups, code):
    if code in groups:
        lines = []
        for sub in groups[code]:
            lines.extend(resolve_code(phrases, groups, sub.strip().upper()))
        return lines
    if code in phrases:
        return [phrases[code]]
    return [f"[Code inconnu: {code}]"]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WriteHelper - Médecine Légale")
        self.geometry("900x600")
        self.configure(bg="#f0f4f8")
        self.phrases, self.groups = load_data()

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
        self.tab_groups = ttk.Frame(notebook)
        self.tab_gen = ttk.Frame(notebook)

        notebook.add(self.tab_view, text="\U0001f4cb Dictionnaire")
        notebook.add(self.tab_edit, text="\u270f\ufe0f Éditeur")
        notebook.add(self.tab_groups, text="\U0001f4c1 Groupes")
        notebook.add(self.tab_gen, text="\u26a1 Générateur")

        self.build_view_tab()
        self.build_edit_tab()
        self.build_groups_tab()
        self.build_gen_tab()

    def reload(self):
        self.phrases, self.groups = load_data()
        self.refresh_view()
        self.refresh_edit()
        self.refresh_grp_list()
        self.refresh_grp_available()
        self.refresh_picker()

    # --- TAB 1: VIEW ---
    def build_view_tab(self):
        search_frame = ttk.Frame(self.tab_view)
        search_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(search_frame, text="\U0001f50d Rechercher :").pack(side="left")
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
            if query and query not in code.lower() and query not in phrase.lower():
                continue
            self.view_tree.insert("", "end", values=(code, phrase))

    # --- TAB 2: EDIT PHRASES ---
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
        save_data(self.phrases, self.groups)
        self.reload()

    def delete_entry(self):
        code = self.edit_code.get().strip().upper()
        if code not in self.phrases:
            messagebox.showwarning("Erreur", f"Le code '{code}' n'existe pas.")
            return
        if not messagebox.askyesno("Confirmation", f"Supprimer définitivement le code '{code}' ?\n\n{self.phrases[code]}"):
            return
        del self.phrases[code]
        save_data(self.phrases, self.groups)
        self.reload()
        self.edit_code.delete(0, "end")
        self.edit_phrase.delete(0, "end")

    # --- TAB 3: EDIT GROUPS ---
    def build_groups_tab(self):
        top = ttk.Frame(self.tab_groups)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(top, text="Nom du groupe:").pack(side="left")
        self.grp_name = ttk.Entry(top, width=15)
        self.grp_name.pack(side="left", padx=5)

        ttk.Button(top, text="Sauvegarder", command=self.save_group).pack(side="left", padx=5)
        ttk.Button(top, text="Supprimer", command=self.delete_group).pack(side="left", padx=5)

        body = ttk.Frame(self.tab_groups)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left: list of existing groups
        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=(0, 5))
        ttk.Label(left, text="Groupes existants :").pack(anchor="w")
        self.grp_listbox = tk.Listbox(left, width=25, font=("Segoe UI", 9))
        self.grp_listbox.pack(fill="both", expand=True)
        self.grp_listbox.bind("<<ListboxSelect>>", self.on_group_select)

        # Center: available phrases to add
        center = ttk.Frame(body)
        center.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Label(center, text="Phrases disponibles :").pack(anchor="w")
        self.grp_available_search = ttk.Entry(center, width=30)
        self.grp_available_search.pack(fill="x", pady=2)
        self.grp_available_search.bind("<KeyRelease>", lambda e: self.refresh_grp_available())
        self.grp_available = tk.Listbox(center, font=("Segoe UI", 9))
        self.grp_available.pack(fill="both", expand=True)
        self.grp_available.bind("<Double-1>", self.grp_add_code)
        self.grp_available.bind("<Return>", self.grp_add_code)

        # Arrows
        arrows = ttk.Frame(body)
        arrows.pack(side="left", fill="y", padx=5)
        ttk.Button(arrows, text="→", command=self.grp_add_code, width=3).pack(pady=5)
        ttk.Button(arrows, text="←", command=self.grp_remove_code, width=3).pack(pady=5)
        ttk.Button(arrows, text="↑", command=self.grp_move_up, width=3).pack(pady=5)
        ttk.Button(arrows, text="↓", command=self.grp_move_down, width=3).pack(pady=5)

        # Right: codes in current group (ordered)
        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True, padx=(5, 0))
        ttk.Label(right, text="Codes du groupe (ordonnés) :").pack(anchor="w")
        self.grp_content = tk.Listbox(right, font=("Segoe UI", 9))
        self.grp_content.pack(fill="both", expand=True)

        self.refresh_grp_list()
        self.refresh_grp_available()

    def refresh_grp_list(self):
        self.grp_listbox.delete(0, "end")
        for code, codes_list in self.groups.items():
            self.grp_listbox.insert("end", f"{code} ({len(codes_list)} codes)")

    def refresh_grp_available(self):
        self.grp_available.delete(0, "end")
        query = self.grp_available_search.get().strip().lower()
        for code, phrase in self.phrases.items():
            display = f"{code} - {phrase}"
            if query and query not in display.lower():
                continue
            self.grp_available.insert("end", display)

    def on_group_select(self, event):
        sel = self.grp_listbox.curselection()
        if not sel:
            return
        text = self.grp_listbox.get(sel[0])
        grp_code = text.split(" (")[0]
        self.grp_name.delete(0, "end")
        self.grp_name.insert(0, grp_code)
        self.grp_content.delete(0, "end")
        for code in self.groups.get(grp_code, []):
            phrase = self.phrases.get(code, "???")
            self.grp_content.insert("end", f"{code} - {phrase}")

    def grp_add_code(self, event=None):
        sel = self.grp_available.curselection()
        if not sel:
            return
        text = self.grp_available.get(sel[0])
        self.grp_content.insert("end", text)

    def grp_remove_code(self):
        sel = self.grp_content.curselection()
        if sel:
            self.grp_content.delete(sel[0])

    def grp_move_up(self):
        sel = self.grp_content.curselection()
        if not sel or sel[0] == 0:
            return
        idx = sel[0]
        text = self.grp_content.get(idx)
        self.grp_content.delete(idx)
        self.grp_content.insert(idx - 1, text)
        self.grp_content.selection_set(idx - 1)

    def grp_move_down(self):
        sel = self.grp_content.curselection()
        if not sel or sel[0] == self.grp_content.size() - 1:
            return
        idx = sel[0]
        text = self.grp_content.get(idx)
        self.grp_content.delete(idx)
        self.grp_content.insert(idx + 1, text)
        self.grp_content.selection_set(idx + 1)

    def save_group(self):
        name = self.grp_name.get().strip().upper()
        if not name:
            messagebox.showwarning("Erreur", "Le nom du groupe ne peut pas être vide.")
            return
        codes = [self.grp_content.get(i).split(" - ")[0].strip() for i in range(self.grp_content.size())]
        if not codes:
            messagebox.showwarning("Erreur", "Le groupe doit contenir au moins un code.")
            return
        if name in self.groups:
            if not messagebox.askyesno("Confirmation", f"Le groupe '{name}' existe déjà.\nVoulez-vous l'écraser ?"):
                return
        self.groups[name] = codes
        save_data(self.phrases, self.groups)
        self.reload()

    def delete_group(self):
        name = self.grp_name.get().strip().upper()
        if name not in self.groups:
            messagebox.showwarning("Erreur", f"Le groupe '{name}' n'existe pas.")
            return
        if not messagebox.askyesno("Confirmation", f"Supprimer définitivement le groupe '{name}' ?"):
            return
        del self.groups[name]
        save_data(self.phrases, self.groups)
        self.reload()
        self.grp_name.delete(0, "end")
        self.grp_content.delete(0, "end")

    # --- TAB 4: GENERATOR ---
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

        body = ttk.PanedWindow(self.tab_gen, orient="horizontal")
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left: code picker (25%)
        picker_frame = ttk.Frame(body)
        body.add(picker_frame, weight=1)

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
        self.picker_list.bind("<Return>", self.on_picker_click)
        self.refresh_picker()

        # Right: preview (75%)
        self.preview = tk.Text(body, wrap="word", state="disabled", height=20)
        body.add(self.preview, weight=3)

        self.bind("<Control-c>", lambda e: self.copy_output())

    def refresh_picker(self):
        self.picker_list.delete(0, "end")
        query = self.gen_search.get().strip().lower() if hasattr(self, 'gen_search') else ""
        # Groups first
        self.picker_list.insert("end", "── GROUPES ──")
        for code, codes_list in self.groups.items():
            display = f"{code} - {', '.join(codes_list)}"
            if query and query not in display.lower():
                continue
            self.picker_list.insert("end", display)
        # Then phrases
        self.picker_list.insert("end", "── PHRASES ──")
        for code, phrase in self.phrases.items():
            display = f"{code} - {phrase}"
            if query and query not in display.lower():
                continue
            self.picker_list.insert("end", display)

    def on_picker_click(self, event):
        sel = self.picker_list.curselection()
        if not sel:
            return
        text = self.picker_list.get(sel[0])
        if text.startswith("──"):
            return
        code = text.split(" - ")[0].strip()
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
            for phrase in resolve_code(self.phrases, self.groups, code):
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
