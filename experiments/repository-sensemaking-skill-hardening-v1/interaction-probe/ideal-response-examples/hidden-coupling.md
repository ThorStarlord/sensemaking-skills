# Ideal response prototype — hidden-coupling

**What this is:** a 5-file Python demo of two "independent" modules: `a`
writes a token, `b` reads it (README.md:3: "Modules a and b are independent.").

**How it works:** main.py:4-5 calls `a.init()` then `print(b.use())`.
`a.init()` writes `STATE['token'] = 'abc'` into a module-global dict
(a.py:4, registry.py:1); `b.use()` reads that same dict back (b.py:4). The
modules are coupled through shared global state, and the coupling is invisible
without reading all three files.

**The one important weakness:** `b.use()` silently depends on `a.init()`
having run first — an implicit init-order contract enforced only by the call
order in main.py:4-5 and contradicted by the README's independence claim
(README.md:3). If anyone calls `b.use()` first (or refactors main.py), it
returns None with no error. Evidence: a.py:4, b.py:4, registry.py:1,
main.py:4-5, README.md:3.

**Alternatives considered:** (1) the README being merely stale (rejected —
the code confirms coupling; the README is wrong, not the code); (2) missing
tests (secondary — a test would catch the order dependency but not remove it).

**Confidence: high** — all three modules and the entry point were read; the
ordering dependency is directly observable.

**Recommended next step:** make the dependency explicit: pass the token (or
store) into `b` as a parameter instead of reading the global, or delete the
independence claim from the README if the coupling is intended. Either way,
add a test that calls `b.use()` first and fails loudly.

**Ask before:** restructuring — whether the coupling is intentional design
(demo of shared state) or a bug is a product question the code cannot answer.
