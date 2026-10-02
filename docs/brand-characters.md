# GLO brand characters

These are the recurring people in GLO's AI-generated imagery. Reuse them so the same faces appear across the site, ads and social posts.

They are saved two ways in the Higgsfield account:

- **Higgsfield Element.** Reference it by its element ID inside a prompt, e.g. `"<<<cecf1a44-ee8b-462c-b0c4-c63240940356>>> walking into a bright medspa lobby"`. Elements work with GPT Image 2, Nano Banana Pro/2, Seedream 4.5/5 lite, Cinema Studio, Kling 3.0 and Seedance 2.0. Several Elements can share one shot.
- **Source job.** The original generation. Its job ID can be passed as a reference image (`medias`) to Higgsfield image models.

All imagery is AI-generated and must keep the "Representative imagery, AI-generated" disclosure wherever it appears. Never present these people as real clients or testimonials.

| Name | Who | Higgsfield Element ID | Source job ID | Used on |
| --- | --- | --- | --- | --- |
| **GLO-Diane-60s** | Black woman, early 60s, short natural silver hair, cream knit sweater | `cecf1a44-ee8b-462c-b0c4-c63240940356` | `175e4678-0ae9-4464-8168-4d4a5e763ed7` | Home: "Horse Country Mornings" |
| **GLO-Marcus-40s** | Man ~48, racially ambiguous mixed heritage, light olive-beige skin, salt-and-pepper hair, trimmed beard | `75855eb5-86d2-4595-acb5-6552df02776b` | `f2efb89a-4a81-4e8a-ac4e-4c29d2e70aba` | Home: "Active & Recharged" |
| **GLO-Sofia-30s** | Latina woman ~30, long dark wavy hair, dewy skin, ivory linen top | `1abda1b5-a3f2-401e-aaec-f40b6dac0055` | `a0a683a6-c3f0-4e84-b5d5-d3d138eabaee` | Home: "Golden Hour Glow" |
| **GLO-Mei-40s** | East Asian woman, mid-40s, shoulder-length dark hair, oatmeal lounge set | `0bc4f584-7d5d-4c25-9672-252eff5234ba` | `0f788a80-530e-483a-ba1b-60820956532a` | Home: "Balanced & Energized" |

Image URL pattern: `https://d8j0ntlcm91z4.cloudfront.net/user_3JRDtqjRvBX48mQoPYnwuq2wzO6/hf_20261001_004311_<source job ID>.png`

## Style used for all four

Model `gpt_image_2_5`, aspect ratio 3:4. Prompts follow this pattern: photorealistic editorial lifestyle portrait, warm golden light, a soft beige and gold palette, natural minimal makeup, real skin texture and shallow depth of field. The subject sits in the upper two-thirds, leaving a softer, darker lower third for overlaid text. No text, logos or watermarks.

## Group shot

- **All four together in a GLO lounge.** Generated with `gpt_image_2` using all four Element IDs in one prompt. Source job ID `2940c9f3-89bf-4257-a861-f02aa9a1279d`, aspect ratio 3:4. Used as the Locations page hero.

## Photo bands (16:9)

One wide lifestyle image per treatment page, generated with `gpt_image_2` (2k, medium) from the Elements above, with the
subject in the left third so the band copy sits on the right. Copy and image URLs live in `content/bands.json`.

| Page | Scene | File |
| --- | --- | --- |
| xeomin | Woman laughing with friends on a sunlit cafe patio | `hf_20261002_044125_faaa6be1-cc0f-4fa4-ab06-e51892944ef6.png` |
| daxxify | Woman relaxing on a garden terrace with a cup of tea | `hf_20261002_044125_ba027226-b166-4eb5-9890-1395be914827.png` |
| dermal-filler | Woman in soft profile beside a sunlit window | `hf_20261002_044125_2b5d9a8a-f530-48cd-b49b-d7e91f575ea3.png` |
| liquid-rhinoplasty | Woman in elegant side profile against a warm wall | `hf_20261002_044125_d0cf1b3c-8bf0-4b89-a6eb-7caa2d1af7c3.png` |
| dissolve-ha-dermal-filler | Woman smiling at her reflection in a brass mirror | `hf_20261002_044125_f2d4dac7-b7ee-440d-a28c-789b148d0e2a.png` |
| daxxify-facial-microneedling | Woman relaxing in a treatment chair with glowing skin | `hf_20261002_044125_9cb70f13-e870-44ce-8d54-8c422029a8e4.png` |
| microneedling | Woman in her sixties relaxing in a sunlit treatment room | `hf_20261002_044125_f230fdf5-9468-4e25-b0a2-c9ea66a0cf47.png` |
| laser-skin-revitalization | Woman with glowing skin on a shaded Florida porch | `hf_20261002_044125_9b4496ee-0e13-4e75-b3c3-c2d069ab442e.png` |
| coolpeel | Woman wearing protective goggles during a laser treatment | `hf_20261002_044125_a74d3fcb-b71a-4523-8db8-0e94fa9d2f6b.png` |
| motus-laser-facial | Woman relaxing during a gentle laser facial | `hf_20261002_044125_fc8a6168-a0a2-4668-b063-6234bad7a318.png` |
| laser-hair-removal | Woman in summer linen on a sunny Florida boardwalk | `hf_20261002_060611_7f69aa10-4471-44ce-931c-0fd9009fe895.png` |
| skin-tightening | Woman touching her jawline and smiling in a mirror | `hf_20261002_044125_e80d2e95-98e5-415b-8909-5ce7bd9eeaec.png` |
| radiant-lift | Woman tilting her chin up in golden light | `hf_20261002_054939_83e02a30-5fb0-43fd-9ec8-9b3047d1180c.png` |
| custom-facials-peels | Woman relaxing during a facial with a clay mask | `hf_20261002_054939_3f2f3cc0-8d9c-4410-aeee-83f1a6b51fd7.png` |
| mini-facials | Woman smiling after a quick facial | `hf_20261002_054939_7575537f-841c-4d5f-8532-d1af9b967fe8.png` |
| functional-weight-loss | Man walking a shaded forest trail with a water bottle | `hf_20261002_054939_e892d371-a5d6-4a4d-bdb0-589b40c53686.png` |
| hormone-replacement-therapy | Man and woman laughing together on a sunny porch | `hf_20261002_054939_7928f69c-ad76-4d20-8aca-635d7d04cbee.png` |
| peptide-therapy | Man stretching on a wooden deck at sunrise | `hf_20261002_054939_dd3b675f-8256-44c3-a186-40ac3e0ff757.png` |
| iv-hydration | Woman reading in a lounge chair during IV hydration | `hf_20261002_054939_7798f828-e557-49e3-bb43-28ab9dd99d1d.png` |
| locations/ocala | Four GLO clients of different ages relaxing together in the lounge | `hf_20261001_004311_2940c9f3-89bf-4257-a861-f02aa9a1279d.png` |
| locations/palatka | Four GLO clients of different ages relaxing together in the lounge | `hf_20261001_004311_2940c9f3-89bf-4257-a861-f02aa9a1279d.png` |
