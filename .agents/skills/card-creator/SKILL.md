---
name: card-creator
description: Create atomic Obsidian knowledge cards from user-provided ideas, sources, notes, or confirmed learning outcomes. Use when the user asks to save, record, create, or turn material into a reusable knowledge card, even without naming a card type.
---

# Card Creator

Create one reusable knowledge unit at a time. Preserve the user's meaning,
source, and uncertainty; write cards only after the requested scope is clear.

## Workflow

### 1. Confirm the card scope

Apply the **atomic** test: a card has one core object, claim, question, or
practice that can be named in one sentence and reused independently.

Read `System/Vault_Schema.md` and search existing cards before proposing a
new file. Update an existing card instead of duplicating it when the same core
is already covered; do not create a card for a passing mention that fails the
Vault's create/update threshold.

When the input contains multiple independently reusable cores, propose a split
with one title and type per card, then wait for user confirmation before
creating multiple files. Treat length, headings, and connective words only as
signals to inspect; they do not by themselves require splitting.

MOC is the explicit exception: create it only when the user asks for a
navigational map rather than an atomic knowledge unit.

**Completion:** The input has one atomic core, a user-approved split plan, or a
confirmed MOC scope.

### 2. Select the type and template

Honor a user-specified type when it exists. Otherwise select the type from the
core object, not incidental source words: an idea learned from a book may be an
`insight`; use `book-note` only for a book-specific passage or annotation.

Read `references/card-type-map.md` before selecting a type. It is the sole
authority for supported types, detection cues, template filenames, and source
policy. If two types remain plausible, show the two candidates and ask the user
to choose.

**Completion:** The selected `card_type`, exact template path, and source
policy are explicit.

### 3. Fill the template

Read the exact mapped template under `Templates/Cards/`.
Keep `type: card`; set `card_type` to the mapped type. Fill only fields present
in that template.

For cards whose template requires `source`, use the original URL when available;
otherwise use a concise source name such as a book, conversation, personal
experience, or `自己整理`. Put titles, authors, context, and explanations in the
body's 来源 section. For mapped source-exempt templates, follow the template
without inventing a frontmatter field.

Use `待补充` or an empty optional value for genuinely unknown information; leave
no literal `{{...}}` placeholders in the completed card. Read
`references/writing-rules.md` when filling frontmatter, filenames, or links.
When the selected template contains `use_when`, fill it with 1–3 concrete
retrieval moments only when they can be inferred from the approved content;
otherwise use an empty list rather than inventing a scenario.
Use `tags` only for 1–3 stable subject tags registered in
`System/Vault_Schema.md`; never repeat `type`, `card_type`, source, status,
people, dates, or filenames as tags. If no subject tag clearly applies, use an
empty list instead of inventing one. Propose a Schema update separately when a
genuinely stable new subject emerges.

**Completion:** Every required template field is populated, intentionally left
empty, or marked `待补充`; frontmatter contains valid YAML and no unintended
template placeholders.

### 4. Find meaningful links

Search card titles, `card_type`, tags, source, and core concepts. Read only the
strongest matches, then add up to three meaningful links to the new card using
the template's `related` format. Explain additional relationships in the body
when useful.

Creating a card does not authorize modifications to existing cards. When the
user explicitly asks for bidirectional links, show the exact existing files and
proposed changes before updating them.

**Completion:** Related cards were searched by core concept and only meaningful
new-card links were selected.

### 5. Create and verify the card

Name the file `{card_type}_{title}.md`, using a concise stable title and the
Vault naming rules. If that exact filename already exists, show the collision
and obtain confirmation before replacing or choosing a new name.

Write the card to `03_Knowledge/00_Cards/`, parse its frontmatter, verify its
template and links, add or update its one-line entry in
`03_Knowledge/INDEX.md`, append one concise entry to
`03_Knowledge/CHANGELOG.md`, and report the final paths.

**Completion:** The new file exists at the approved path, its frontmatter
parses, and the reported card matches the selected type and approved scope.

## References

- Read `references/card-type-map.md` to select a supported type and template.
- Read `references/writing-rules.md` when producing final card text or YAML.
- Read `references/examples.md` only when a user request is ambiguous and a
  nearby example would clarify the type decision.
