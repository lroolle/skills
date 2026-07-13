# Report precision

Load this when the artifact is a project report, benchmark
writeup, experiment note, or any document where a decision rests
on numbers. The report / explainer layout lives in
[patterns.md](patterns.md); this file is the measurement
discipline on top of it. An engineer reading a report probes it
the way a reviewer probes a proof: can I find the number, trust
the number, and reproduce the number? Every rule here serves one
of those three.

## Figures and tables

- Number them and reference them by number. The document template
  does this with CSS counters: every `figure.diagram` with a
  `figcaption` becomes "Figure N."; every `<table>` with a
  `<caption>` becomes "Table N." Tables without captions stay
  unnumbered -- layout tables and small inline lists do not earn
  numbers.
- Cross-reference with links, not proximity: `see
  <a href="#fig-flow">Figure 1</a>`. "The diagram below" breaks
  the first time a section is reordered.
- A caption states the takeaway, not the topic. "Figure 2. p99
  latency doubles past 400 rps" tells the reader what to see;
  "Figure 2. Latency results" makes them derive it. The caption
  is the one line skimmers are guaranteed to read.

## Numbers

- Units live in the header (`Latency (ms)`), never repeated in
  every cell. A column that mixes units is two columns.
- Numeric columns are right-aligned in `tabular-nums` -- the
  template's `td.num` class. Magnitude comparison is done by eye
  down a column; proportional digits and left alignment break the
  eye's alignment.
- Pick one precision per column and hold it: `12.40, 3.07, 0.92`,
  not `12.4, 3.065, 1`. Three significant figures is almost
  always enough; more digits claim precision the measurement does
  not have.
- A measurement without spread is a claim, not a measurement.
  Give n and the spread (`142 ms ± 6, n=50`, or p50/p99). Never
  average percentiles across runs -- percentiles do not compose;
  pool the raw samples or report the range of the percentile.
- State the environment once, near the numbers: hardware, dataset
  size, warm or cold. Benchmarks travel without their context and
  get quoted against mismatched baselines.

## Charts

Hand-rolled inline SVG, per patterns.md. The bar an engineer
holds a chart to:

- Axes labeled with quantity and unit, ticks at round intervals.
  An unlabeled axis makes the chart decoration.
- Bar charts start at zero. A truncated baseline turns a 3%
  difference into a visual 3x -- readers who notice stop trusting
  every other figure in the document. When the interesting range
  genuinely sits far from zero, use points or a line instead, and
  say the axis range in the caption.
- Log scales are legitimate and must be announced -- in the axis
  label and tick values, not a footnote.
- One series color plus the accent on the anomaly the chart
  exists to show. Six-color spaghetti means the chart wants to be
  two charts or a table.
- When the reader needs exact values, the chart gains a collapsed
  `<details>` table of the plotted numbers. Charts show shape;
  tables carry values; a report with decisions riding on the
  values ships both.

## Equations

MathML, inline. Every current browser renders it natively --
no KaTeX or MathJax CDN, which would break rule 1
(self-containment) for a formula that renders for free:

```html
<math display="block">
  <mi>L</mi><mo>=</mo>
  <mfrac>
    <mi>&#x3BB;</mi>
    <mrow><mi>&#x3BC;</mi><mo>&#x2212;</mo><mi>&#x3BB;</mi></mrow>
  </mfrac>
</math>
```

Define every symbol at first use. Past ~5 symbols, add a
nomenclature table -- symbol, meaning, unit -- and link it from
the first equation. An undefined symbol costs each reader a
search; the table costs one.

## Provenance

The template ends with a colophon; fill it, do not delete it.
Minimum contract: generation date, source commit or data
snapshot, and the command or query that produced the numbers.

```
Generated 2026-07-13 from lroolle/skills@c05060d.
Latency data: bench/run.sh --profile p99, 50 runs, m7i.large.
```

The colophon is what lets a reader six weeks later tell whether
the report describes the current system or an ancestor -- and
lets them rerun the measurement instead of arguing with it. A
report that cannot be reproduced can only be believed, and
engineers are right not to.
