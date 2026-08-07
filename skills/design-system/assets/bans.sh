#!/usr/bin/env bash
# design-system bans — deterministic checks that encode scars.
# A clean run is evidence, not proof; it can't see costume. Pair it with a
# taste verdict on the real interaction path. Exit 1 if any ban trips.
#
# Usage: bans.sh [DIR ...]   (defaults to src/app src/blocks)
# Point it at the app/page code, NOT at your component library
# (shadcn/ui and friends are token-driven and managed by their generator).

set -uo pipefail
dirs=("${@:-src/app src/blocks}")
# shellcheck disable=SC2206
dirs=(${dirs[@]})
fail=0

hit() { echo "DEFECT [$1]: $2"; fail=1; }

# 1. Raw palette classes — semantic states must come from tokens, not from
#    Tailwind's default ramp. One page carrying token-red + red-600 + amber-*
#    is three color systems with no shared meaning.
if out=$(grep -rInE '\b(bg|text|border|ring|from|to|via)-(red|amber|orange|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose|slate|zinc|neutral|stone|gray)-[0-9]{2,3}\b' "${dirs[@]}" 2>/dev/null | grep -v '/ui/'); then
  hit palette "raw Tailwind color classes in app code"; echo "$out" | head -20
fi

# 2. Urgency kit — pulsing/counting/bouncing spends trust to buy attention.
#    Deadlines render as dated facts.
if out=$(grep -rInE 'animate-(ping|pulse|bounce)' "${dirs[@]}" 2>/dev/null | grep -v '/ui/'); then
  hit urgency "urgency animations (ping/pulse/bounce)"; echo "$out" | head -20
fi

# 3. Hardcoded hex — color lives in the token layer so both themes stay
#    coherent. A hex in a component is a color that dark mode can't reach.
if out=$(grep -rInE '#[0-9a-fA-F]{3,8}\b' "${dirs[@]}" 2>/dev/null | grep -v '/ui/'); then
  hit hex "hardcoded hex colors in app code"; echo "$out" | head -20
fi

# 4. Saturated display fonts — the training-data reflex. Re-seed if a reflex
#    reaches for one. (Body/system use is fine; this flags font-family decls.)
if out=$(grep -rInE "font-family[^;]*(Inter|Poppins|Montserrat|'?DM Sans|Plus Jakarta|Playfair|Fraunces|Space Grotesk|Space Mono)" "${dirs[@]}" 2>/dev/null | grep -v '/ui/'); then
  hit font "saturated display font in a font-family declaration"; echo "$out" | head -20
fi

if [ "$fail" -eq 0 ]; then
  echo "bans: clean"
fi
exit "$fail"
