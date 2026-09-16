"""Nesting-aware corpus path resolver (round 128, Chris's template-folder layer).

The corpus gained a template-type layer: modules now live at
  01-(Finalized|Claude)_Modules_/<TemplateType>/<CODE>/   (was .../<CODE>/).

These helpers resolve a module flat-OR-nested so every tool keeps working regardless
of layout. CRITICAL: on the OLD flat layout, mdir() == os.path.join() exactly and
mods() == "the dirs directly under root" — so patching tools to use them is
behavior-NEUTRAL until the move actually happens. That neutrality is what lets us
prove the gates are unchanged before moving anything.
"""
import os, glob as _glob

TEMPLATE_DIRS = ("Standard", "Inquiry", "Fundamentals", "Bilingual")

def mdir(root, *parts):
    """Resolve <root>/<parts...> where the first part is a module code that may sit
    under a TemplateType subfolder. Falls back to the plain flat join (identical to
    os.path.join) whenever that path already exists or no nested match is found."""
    flat = os.path.join(root, *parts)
    if os.path.exists(flat):
        return flat
    if parts:
        for t in TEMPLATE_DIRS:
            cand = os.path.join(root, t, *parts)
            if os.path.exists(cand):
                return cand
        hits = _glob.glob(os.path.join(root, "*", parts[0]))
        if hits:
            return os.path.join(hits[0], *parts[1:])
    return flat

def mods(root):
    """Module-code basenames under root, flat OR nested under TemplateType folders."""
    out = []
    try:
        entries = sorted(os.listdir(root))
    except FileNotFoundError:
        return out
    for e in entries:
        p = os.path.join(root, e)
        if not os.path.isdir(p):
            continue
        if e in TEMPLATE_DIRS:
            out += [d for d in sorted(os.listdir(p)) if os.path.isdir(os.path.join(p, d))]
        else:
            out.append(e)
    return out

def mdirs(root):
    """Full paths of every module dir under root (flat or nested) — replaces
    glob(os.path.join(root, '*'))."""
    return [mdir(root, c) for c in mods(root)]

def gany(root, *parts):
    """Glob files matching <parts> inside EVERY module, flat OR nested depth —
    replaces glob(os.path.join(root, '*', *parts)). The flat-depth pattern matches
    on the old layout, the nested-depth on the new one; their union is correct for
    both (and a half-migrated mix)."""
    return sorted(set(_glob.glob(os.path.join(root, "*", *parts)) +
                      _glob.glob(os.path.join(root, "*", "*", *parts))))

# ---------------------------------------------------------------------------------------------------------------------
# ROUND 343 (Chris's decision D10-6, 2026-09-16): the SCORED population is the corpus minus compare_exclusions.txt.
# mods() stays inclusive (regeneration / manifest / registries / feature index cover every module); the GATES call
# gate_mods(). One list, honoured by every gate — see compare_exclusions.txt for the reason each module is there.
EXCLUSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compare_exclusions.txt")

def excluded():
    """The module codes compare_exclusions.txt lists (comments after '#' ignored); empty when the file is absent."""
    try:
        with open(EXCLUSIONS_FILE, encoding="utf-8") as f:
            return {ln.split("#", 1)[0].strip() for ln in f if ln.split("#", 1)[0].strip()}
    except FileNotFoundError:
        return set()

def gate_mods(root):
    """mods(root) minus the compare exclusions — the population every scored gate measures."""
    ex = excluded()
    return [c for c in mods(root) if c not in ex]
