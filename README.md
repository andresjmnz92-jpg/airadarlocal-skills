# AI Radar Local Agent Skills

Version: `0.1.0` (draft)

Bilingual Agent Skills for local visibility research and content workflows. These skills are designed to work with the AI Radar Local MCP at `https://app.airadarlocal.com/mcp`; connect the MCP separately in your AI client. The skills provide workflow guidance. They do not grant access to an account or business data by themselves.

## Choose a language

- English: `skills/en/`
- Español: `skills/es/`

Each skill is a folder containing `SKILL.md`. Install only the language and skills you want, so your assistant does not see duplicate English and Spanish workflows.

| English | Español |
| --- | --- |
| `90-day-plan` | `plan-90-dias` |
| `content` | `contenido` |
| `gaps` | `huecos` |
| `google-profile` | `perfil-google` |
| `questions` | `preguntas` |
| `technical-check` | `chequeo-tecnico` |

## Install with GitHub CLI

`gh skill` is currently in public preview. To avoid loading duplicate English and Spanish guidance, install the six skills for your language. In PowerShell, for English:

```powershell
$skills = @('90-day-plan','content','gaps','google-profile','questions','technical-check')
foreach ($skill in $skills) { gh skill install andresjmnz92-jpg/airadarlocal-skills "skills/en/$skill" --agent codex --scope user }
```

For Spanish, use:

```powershell
$skills = @('chequeo-tecnico','contenido','huecos','perfil-google','plan-90-dias','preguntas')
foreach ($skill in $skills) { gh skill install andresjmnz92-jpg/airadarlocal-skills "skills/es/$skill" --agent codex --scope user }
```

For Claude Code, replace `codex` with `claude-code`. To install only one skill, replace the loop with an individual command, for example `gh skill install andresjmnz92-jpg/airadarlocal-skills skills/es/preguntas --agent codex --scope user`. To install at project scope, use `--scope project` instead of `--scope user`.

## Claude web

1. Download a ZIP for one skill and language from the [version 0.1.1 ZIP packages](packages/0.1.1/). The ZIP contains that skill folder and its `SKILL.md`.
2. In Claude, open **Customize → Skills → Create skill → Upload a skill** and upload the ZIP.
3. Enable the skill. Connect AI Radar Local MCP separately if you want the skill to use your Radar account.

Skill availability and upload options can depend on your Claude plan or workspace administrator.

## ChatGPT web

1. Download a ZIP for one skill and language from the [version 0.1.1 ZIP packages](packages/0.1.1/).
2. Open **Skills**, choose **Create → Upload from your computer**, and upload the ZIP if the feature is available for your account or workspace.
3. Enable the skill. Connect AI Radar Local MCP separately; a skill package does not configure the MCP connection.

## Codex and other compatible CLIs

Install from this repository using `gh skill` as shown above. The CLI can also install an individual skill from a repository path. Check the installed skill's `SKILL.md` before using it, especially when installing community or third-party skills.

## Versioning

This draft packages version `0.1.1` under `packages/0.1.1/`. A tagged GitHub Release will be created when the public repository is ready.

## License and use

**All rights reserved.** Copyright © 2026 AI Radar Local. You may use these skills in personal or commercial workflows, including services delivered to your clients. You may not redistribute, resell, modify, or sublicense the files themselves, or package them as a competing skills product without written permission.

## Español

Estas skills bilingües guían flujos de visibilidad local y creación de contenido. Se conectan al MCP de AI Radar Local (`https://app.airadarlocal.com/mcp`), pero debes configurar ese conector por separado.

- Inglés: `skills/en/`
- Español: `skills/es/`

Instala las seis skills del idioma que vas a usar para evitar instrucciones duplicadas. `gh skill` está en vista previa pública. En PowerShell, para español:

```powershell
$skills = @('chequeo-tecnico','contenido','huecos','perfil-google','plan-90-dias','preguntas')
foreach ($skill in $skills) { gh skill install andresjmnz92-jpg/airadarlocal-skills "skills/es/$skill" --agent codex --scope user }
```

Para inglés, usa los nombres en `skills/en/` de la tabla de arriba. Para Claude Code, usa `--agent claude-code`. Claude web y ChatGPT web permiten cargar el ZIP individual de una skill desde sus opciones de Skills cuando la función está disponible en la cuenta. Descarga el ZIP de `packages/0.1.1/` y conecta el MCP por separado.

**Todos los derechos reservados.** Consulta “License and use” antes de usar estos archivos.
