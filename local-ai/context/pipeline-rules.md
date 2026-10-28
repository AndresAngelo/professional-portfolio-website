# Pipeline rules

- Configuration in `local-ai/config/orchestrator.toml` is authoritative.
- Use exactly one configured LM Studio model. Python selects the execution mode; the model does not select a role or mode.
- Send one fresh, no-history request for each selected mode/attempt. Do not reuse prior-task or prior-attempt conversation state.
- Include only the bounded three-bucket context: system rules, architecture schema, and active task scope. An optional plan belongs in the same request.
- Verify runtime capabilities before relying on the configured low-VRAM KV-cache policy.
- Return exactly one Tool Protocol JSON object for executor actions, with no Markdown fence or prose.
- Use only workspace-relative paths and allowed protocol actions.
- Never request Git mutations, remote access, package installation, or undeclared commands.
- Declared validation commands are executed only by the orchestrator from the configured workspace root.
