'use strict';

/**
 * Extracted from addyosmani/agent-skills, scripts/lib/skill-lint.js, MIT,
 * commit aeac41d. Keep byte-identical to upstream so runner diffs stay
 * readable; add new rules upstream rather than here.
 */

/**
 * Parse YAML-style frontmatter from the top of a markdown file.
 * Returns a key→value object, or null if no frontmatter block found.
 * Values are stripped of surrounding quotes.
 */
function parseFrontmatter(content) {
  const match = content.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*\r?\n/);
  if (!match) return null;

  const result = {};
  for (const line of match[1].split(/\r?\n/)) {
    if (/^\s*#/.test(line)) continue;
    const m = line.match(/^([A-Za-z0-9_-]+)\s*:\s*(.*)$/);
    if (!m) continue;
    const key   = m[1];
    const value = m[2].trim().replace(/^['"]|['"]$/g, '');
    result[key] = value;
  }
  return result;
}

module.exports = { parseFrontmatter };
