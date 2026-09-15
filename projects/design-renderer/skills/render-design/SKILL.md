---
name: render-design-json
description: Render one final PNG or JPG from an extracted design.json after asking for the product and post content. Use for the local design renderer, not for reference-image analysis or template creation.
---

Use this project only for `design.json` + user content → one raster image.

For a bound generation, require the incoming `designId`, `designVersionId`, `assetBinding` and `generatedAssets`, preserve the identifiers unchanged, ask for the product name when it is not known, create a UUID-v4 `generationId`, and use the repository-relative path `generated-content/{produto}/styles/{designId}/versions/{designVersionId}/posts/{designId}--{generationId}.png`. After the PNG is successfully saved and validated, append exactly `{"generationId": "...", "designVersionId": "...", "path": "generated-content/...png"}` to the existing `generatedAssets` array. Never replace or delete previous records and never write literal placeholders.

1. Load the supplied JSON with `renderer.design_reader.load_design`. The extractor's `{"value": ...}` fields are observations, not a second schema to reproduce.
2. Treat an attached `design.json` as the request to start the rendering flow, even when the user sends no additional sentence. Do not offer a menu asking whether to render, validate, review, or collect answers. First ask exactly `Para qual produto devo criar esses posts?`; after the answer, ask exactly `Escreva o texto do post.` If the text is already present, briefly confirm it. Use the supplied text according to the JSON's slots and roles, then render immediately. Never invent content or ask an unnecessary follow-up question.
3. Do not infer original words from the reference. For every generation, an unresolved image slot must receive a new thematic photo generated from the supplied post text, the image role, and the slot geometry. Never open, reuse, or reconstruct the image that was used to extract the JSON; the generated scene may be invented and must not be a placeholder. A slot remains empty only when the user explicitly says `ignorar`. Pass the newly generated local image path to the renderer, which preserves the declared crop, mask and position.
4. Render with `renderer.raster_renderer.render`, respecting every visual field declared by the schema: canvas, bboxes, normalised-coordinate fallback, z-index, background/gradients, style, crop/focal point, masks, opacity, transforms, shapes and typography. Keep unrelated elements fixed and never silently discard a declared visual property.
5. Run the validator before delivery. For the CLI flow, update `generatedAssets` only after the PNG passes validation, then validate and commit the related product folder. Deliver only the valid final PNG/JPG; an unavailable font may be reported as a warning, but a missing or unreadable image is a render failure, never a successful empty slot.

The current extractor (`schemaVersion: 1.0.0`) stores elements in `elements`, bounds in `bounds.{xPx,yPx,widthPx,heightPx}`, and redacted text in `text.value: null`. The adapter also handles equivalent direct fields without defining a parallel template format.
