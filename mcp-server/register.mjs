#!/usr/bin/env node
/**
 * register.mjs — Auto-registers the boomi-skills MCP server with every
 * supported AI tool found on this machine.
 *
 * Supported tools:
 *   - Claude Desktop  (macOS, Windows)
 *   - Claude Code CLI (macOS/Linux, Windows)
 *   - Gemini CLI      (macOS/Linux, Windows)
 *   - Cursor          (macOS, Windows)
 *
 * Usage:
 *   node register.mjs          # register with all detected tools
 *   node register.mjs --dry-run  # preview changes without writing
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { homedir, platform } from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
const SERVER_PATH = join(__dirname, 'index.mjs');
const DRY_RUN = process.argv.includes('--dry-run');
const IS_WIN  = platform() === 'win32';
const HOME    = homedir();

// ---------------------------------------------------------------------------
// MCP server entry to inject
// ---------------------------------------------------------------------------
const SERVER_ENTRY = {
  command: 'node',
  args: [SERVER_PATH],
};

// ---------------------------------------------------------------------------
// Config file locations per tool
// ---------------------------------------------------------------------------
function configLocations() {
  if (IS_WIN) {
    const appData = process.env.APPDATA || join(HOME, 'AppData', 'Roaming');
    const localAppData = process.env.LOCALAPPDATA || join(HOME, 'AppData', 'Local');
    return [
      {
        tool: 'Claude Desktop',
        path: join(appData, 'Claude', 'claude_desktop_config.json'),
        key:  'mcpServers',
      },
      {
        tool: 'Claude Code CLI',
        path: join(HOME, '.claude', 'settings.json'),
        key:  'mcpServers',
      },
      {
        tool: 'Gemini CLI',
        path: join(HOME, '.gemini', 'settings.json'),
        key:  'mcpServers',
      },
      {
        tool: 'Cursor',
        path: join(appData, 'Cursor', 'User', 'settings.json'),
        key:  'mcpServers',
        cursorFormat: true,
      },
    ];
  } else {
    // macOS / Linux
    const claudeDesktopPath = platform() === 'darwin'
      ? join(HOME, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json')
      : join(HOME, '.config', 'Claude', 'claude_desktop_config.json');

    return [
      {
        tool: 'Claude Desktop',
        path: claudeDesktopPath,
        key:  'mcpServers',
      },
      {
        tool: 'Claude Code CLI',
        path: join(HOME, '.claude', 'settings.json'),
        key:  'mcpServers',
      },
      {
        tool: 'Gemini CLI',
        path: join(HOME, '.gemini', 'settings.json'),
        key:  'mcpServers',
      },
      {
        tool: 'Cursor',
        path: join(HOME, '.cursor', 'mcp.json'),
        key:  'mcpServers',
      },
    ];
  }
}

// ---------------------------------------------------------------------------
// Read / write helpers
// ---------------------------------------------------------------------------
function readJson(filePath) {
  if (!existsSync(filePath)) return {};
  try {
    return JSON.parse(readFileSync(filePath, 'utf8'));
  } catch {
    return {};
  }
}

function writeJson(filePath, data) {
  const dir = dirname(filePath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

// ---------------------------------------------------------------------------
// Register
// ---------------------------------------------------------------------------
let registered = 0;
let skipped    = 0;

for (const loc of configLocations()) {
  const config = readJson(loc.path);
  const fileExists = existsSync(loc.path);

  // Only register if the config file already exists (tool is installed)
  // Exception: Claude Code CLI — create it if missing
  if (!fileExists && loc.tool !== 'Claude Code CLI') {
    console.log(`⏭  ${loc.tool} — config not found, skipping (tool may not be installed)`);
    skipped++;
    continue;
  }

  const servers = config[loc.key] || {};

  if (servers['boomi-skills-server']) {
    console.log(`✓  ${loc.tool} — already registered`);
    skipped++;
    continue;
  }

  servers['boomi-skills-server'] = SERVER_ENTRY;
  config[loc.key] = servers;

  if (DRY_RUN) {
    console.log(`[dry-run] Would write to: ${loc.path}`);
    console.log(JSON.stringify({ [loc.key]: { 'boomi-skills-server': SERVER_ENTRY } }, null, 2));
  } else {
    writeJson(loc.path, config);
    console.log(`✅ ${loc.tool} — registered at ${loc.path}`);
  }
  registered++;
}

console.log(`\n${DRY_RUN ? '[dry-run] ' : ''}Done. ${registered} registered, ${skipped} skipped.`);
if (registered > 0 && !DRY_RUN) {
  console.log('\nRestart any running AI tools for changes to take effect.');
}
