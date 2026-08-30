---
name: org-logo-treatment
description: The site's mark is the faceted-V art (v-forge-icon.png), knocked out by a saturation key so it floats on whatever ground the page has; the old chromed-anvil render it replaced could not be knocked out at all, which is why the plate treatment existed.
metadata:
  type: project
---

# The site mark — saturation key, no plate

**Current mark (since 2026-08-14):** the faceted **V**, cyan→violet, with a crystal
centre, supplied by Rafael as `assets/img/v-forge-icon.png` (425×355, charcoal ground
with faint circuit traces). It is the source art; everything else is derived from it:

| File | What | Ground |
|---|---|---|
| `mark.png` | header, 128px drawn at 26 | transparent |
| `favicon-32.png` | favicon | transparent |
| `logo-180.png` | apple-touch | opaque black plate |
| `logo.png` | `og:image`, 512 | opaque black plate |

**The knockout is a saturation key, not a flood fill.** The V is saturated; the ground
*and its circuit traces* are not. So: separate the HSL saturation channel, level it, and
use it as alpha —

```
convert A.png \( +clone -colorspace HSL -channel G -separate +channel -level 12%,32% \) \
        -alpha off -compose CopyOpacity -composite B.png
```

A corner-seeded flood fill is the wrong tool here: the traces are not connected to the
corner, so they survive as grey specks at 26px.

Keep the two plated derivatives plated. iOS composites an apple-touch icon over an
unknown ground, and social cards do the same — and at 180/512px the circuit traces read
as texture worth having. Re-encode both at **`-depth 8`**: ImageMagick defaults to 16-bit
here, which made `logo.png` 1.0 MB instead of 202 KB.

## Why the CSS used to say "present it on a plate"

The mark this replaced was a 3D render — a chromed V with circuit inlay standing on a
steel anvil bearing an M — and it **could not be background-removed at all**. Measured
2026-07-16: the V's bevels and the anvil's top faces are specular white, neutral ≥250,
*identical in value to the paper backdrop and connected to it*, so every border-seeded
fill leaked through a bevel and chewed notches out of the arms; a soft cast shadow
reaching ~222 meant no single luminance cut spared both. Edge-limited region growing
killed the shadow but still bit the bevels. Hence `.brand__mark` carrying
`background:#fff` + a 1px ring — the plate was a workaround for an unkeyable image, not
a design choice.

**That constraint is gone with the art.** The header mark now sits directly on the page;
the plate and ring are removed. Don't reintroduce them, and don't port the old
"never try to knock this out" rule to the new mark — it keys cleanly, as above.

**And the knockout is real, which is why the 2026-08-30 flip to a light default needed
no logo work.** Measured on the shipped file: `mark.png`'s corner alpha is 1–3/255, so
there is no baked ground to show against white. It was drawn for a black page and is not
bound to one. (`logo.png` and `logo-180.png` keep their opaque plates on purpose —
social cards and iOS icons want an opaque tile — and they are never the header mark.)

The old render remains the **GitHub org avatar**
(`https://avatars.githubusercontent.com/u/287217332`) and is unaffected by this; if the
avatar is ever refreshed to match the site, it is an upload, not a file in any repo.
