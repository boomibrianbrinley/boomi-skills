#!/usr/bin/env node
/**
 * Boomi Skills MCP Server
 * =======================
 * Exposes the boomi-skills library to Claude Desktop (or any MCP client)
 * as callable tools. Claude Desktop spawns this as a child process on
 * startup and it remains available for the entire session.
 *
 * Tools provided:
 *   list_skills   — returns all installed skills with name + description
 *   get_skill     — returns the full SKILL.md content for a named skill
 *   update_skills — runs `git pull` on the skills repo and reports changes
 *
 * Claude Desktop config registration:
 *
 *   macOS/Linux (~/.config/Claude/claude_desktop_config.json or
 *               ~/Library/Application Support/Claude/claude_desktop_config.json):
 *   {
 *     "mcpServers": {
 *       "boomi-skills-server": {
 *         "command": "node",
 *         "args": ["/Users/<you>/boomi-skills/mcp-server/index.mjs"]
 *       }
 *     }
 *   }
 *
 *   Windows (%APPDATA%\Claude\claude_desktop_config.json):
 *   {
 *     "mcpServers": {
 *       "boomi-skills-server": {
 *         "command": "node",
 *         "args": ["C:\\Users\\<you>\\boomi-skills\\mcp-server\\index.mjs"]
 *       }
 *     }
 *   }
 */

import { McpServer }            from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z }                    from 'zod';
import { readFileSync, readdirSync, existsSync } from 'fs';
import { join }                 from 'path';
import { execSync }             from 'child_process';
import { homedir, platform }    from 'os';

// ---------------------------------------------------------------------------
// Resolve skills directory — works on macOS, Linux, and Windows
// ---------------------------------------------------------------------------
const SKILLS_DIR = join(homedir(), 'boomi-skills');

if (!existsSync(SKILLS_DIR)) {
  process.stderr.write(
    `[boomi-skills-server] ERROR: Skills directory not found at ${SKILLS_DIR}\n` +
    `Run the installer first: https://github.com/boomibrianbrinley/boomi-skills\n`
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Returns all skill entries that have a SKILL.md */
function discoverSkills() {
  return readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory() && existsSync(join(SKILLS_DIR, d.name, 'SKILL.md')))
    .map(d => {
      const content = readFileSync(join(SKILLS_DIR, d.name, 'SKILL.md'), 'utf8');
      const lines   = content.split('\n');
      // First non-empty line after the h1 title that isn't a heading
      const desc    = lines.find((l, i) => i > 0 && l.trim() && !l.startsWith('#')) || '';
      return { name: d.name, description: desc.trim(), content };
    });
}

/** Run git pull; returns stdout or a formatted error string */
function gitPull() {
  try {
    const out = execSync(`git -C "${SKILLS_DIR}" pull`, {
      encoding: 'utf8',
      timeout: 30_000,
    });
    return out.trim() || 'Already up to date.';
  } catch (err) {
    return `git pull failed: ${err.message}`;
  }
}

// ---------------------------------------------------------------------------
// MCP Server
// ---------------------------------------------------------------------------

const server = new McpServer({
  name:    'boomi-skills-server',
  version: '1.0.0',
});

// --- list_skills ------------------------------------------------------------
server.tool(
  'list_skills',
  'List all installed skills with their names and one-line descriptions',
  {},
  async () => {
    const skills = discoverSkills();
    if (skills.length === 0) {
      return { content: [{ type: 'text', text: 'No skills found in ' + SKILLS_DIR }] };
    }
    const lines = skills.map(s => `- **${s.name}**: ${s.description}`).join('\n');
    return { content: [{ type: 'text', text: `Installed skills (${skills.length}):\n\n${lines}` }] };
  }
);

// --- get_skill --------------------------------------------------------------
server.tool(
  'get_skill',
  'Get the full SKILL.md content for a named skill',
  { name: z.string().describe('Skill directory name, e.g. "global-utilities"') },
  async ({ name }) => {
    const skillFile = join(SKILLS_DIR, name, 'SKILL.md');
    if (!existsSync(skillFile)) {
      const available = discoverSkills().map(s => s.name).join(', ');
      return {
        content: [{
          type: 'text',
          text: `Skill "${name}" not found. Available skills: ${available}`,
        }],
      };
    }
    return { content: [{ type: 'text', text: readFileSync(skillFile, 'utf8') }] };
  }
);

// --- update_skills ----------------------------------------------------------
server.tool(
  'update_skills',
  'Pull the latest skill updates from GitHub and report what changed',
  {},
  async () => {
    const result = gitPull();
    return { content: [{ type: 'text', text: result }] };
  }
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

const transport = new StdioServerTransport();
await server.connect(transport);
process.stderr.write(`[boomi-skills-server] ready — serving ${discoverSkills().length} skills from ${SKILLS_DIR}\n`);
