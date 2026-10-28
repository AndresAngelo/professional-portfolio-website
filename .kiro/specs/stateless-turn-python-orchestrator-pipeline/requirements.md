# Requirements Document

## Introduction

The Stateless Turn Python Orchestrator Pipeline is a local coding automation system that discovers populated Markdown goal files for Milestones M1 through M5, parses coding tasks, and processes one task at a time through fresh LM Studio planning and execution requests. The pipeline persists scheduling state, controls workspace-scoped tool use through JSON, runs task-declared PowerShell validation, preserves partial workspace changes, and records recoverable failures locally.

## Glossary

- **Stateless Turn Python Orchestrator Pipeline**: The Python coding automation system described by this document.
- **Workspace**: The repository directory selected for one pipeline run and every descendant path within that directory.
- **Goal File**: A non-empty Markdown file at `.kiro/specs/m1-*/goals/goal1.md` through `goal10.md`, `.kiro/specs/m2-*/goals/goal1.md` through `goal10.md`, `.kiro/specs/m3-*/goals/goal1.md` through `goal10.md`, `.kiro/specs/m4-*/goals/goal1.md` through `goal10.md`, or `.kiro/specs/m5-*/goals/goal1.md` through `goal10.md`; the populated M5 source set includes `.kiro/specs/m5-homepage-experience/goals/goal1.md` through `.kiro/specs/m5-homepage-experience/goals/goal10.md`.
- **Goal Task**: A Markdown task section in a Goal File that has a unique task heading, coding objective, acceptance criteria, and a declared PowerShell validation block.
- **Task Identifier**: The milestone, goal, and task coordinates extracted from a Goal Task heading, such as `M5.G1.T1`.
- **Task Queue**: The ordered collection of parsed Goal Tasks awaiting processing.
- **Run State**: The durable local record of Task Queue status, current Task Identifier, retry count, execution mode, timestamps, model request identifiers, validation outcome, and artifact paths for one Workspace.
- **Local AI Storage**: The Workspace-local directory that stores Run State, generated plans, JSON protocol records, telemetry, validation output, and quarantine reports.
- **Planner Model**: The LM Studio model identifier `google/gemma-4-12b-qat` used to generate a Goal Task plan.
- **Executor Model**: The LM Studio model identifier `google/gemma-4-e2b` used to generate Goal Task coding actions.
- **Fresh Request**: A single LM Studio HTTP request whose message payload is constructed for one Goal Task and is not reused by a later Goal Task.
- **Tool Protocol**: A JSON request and response contract that identifies a Workspace-relative action, declared arguments, and execution result.
- **Declared Command**: A PowerShell command present in the active Goal Task validation block after Markdown parsing.
- **Execution Mode**: One of `Scaffold`, `Aligner`, `CoT-Task`, or `Error` selected for a Goal Task.
- **Quarantine Report**: A Markdown record of a Goal File or Goal Task that cannot be safely parsed or completed.
- **Low-VRAM Setting**: A configured LM Studio runtime option for Flash Attention, KV cache behavior, or GPU offload that the active LM Studio installation reports as supported.

## Requirements

### Requirement 1: Goal discovery and Markdown parsing

**User Story:** As a developer, I want the pipeline to discover and parse the populated M1–M5 goal files, so that the coding backlog is derived from the approved Markdown source.

#### Acceptance Criteria

1. WHEN a pipeline run starts, THE Stateless Turn Python Orchestrator Pipeline SHALL enumerate every existing Goal File in Milestones M1, M2, M3, M4, and M5, including populated `m5-homepage-experience/goals/goal1.md` through `goal10.md`.
2. WHEN the Stateless Turn Python Orchestrator Pipeline reads a Goal File, THE Stateless Turn Python Orchestrator Pipeline SHALL parse each Goal Task heading, objective, acceptance criteria, prerequisites, implementation details, declared PowerShell validation block, and Task Identifier into a Task Queue record.
3. IF a Goal File or Goal Task lacks a parseable Task Identifier, coding objective, acceptance criteria, or declared PowerShell validation block, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL exclude the Goal File or Goal Task from execution and create a Quarantine Report that identifies the source path, missing element, parser timestamp, and raw Markdown section.
4. WHEN a Goal File is parsed successfully, THE Stateless Turn Python Orchestrator Pipeline SHALL store the source content hash and parsed Task Queue records in Local AI Storage.

### Requirement 2: Deterministic numeric queue ordering

**User Story:** As a developer, I want a deterministic task sequence, so that pipeline runs process the same eligible coding tasks in the same order.

#### Acceptance Criteria

1. WHEN the Stateless Turn Python Orchestrator Pipeline creates a Task Queue, THE Stateless Turn Python Orchestrator Pipeline SHALL order Goal Files by numeric milestone number and numeric goal number before parsing Goal Tasks.
2. WHEN the Stateless Turn Python Orchestrator Pipeline orders Goal Tasks from one Goal File, THE Stateless Turn Python Orchestrator Pipeline SHALL order Goal Tasks by numeric task number extracted from the Task Identifier.
3. WHEN Goal File names or Task Identifiers contain numeric values with different digit counts, THE Stateless Turn Python Orchestrator Pipeline SHALL compare numeric values rather than lexical text values.
4. IF two parsed Goal Tasks resolve to the same Task Identifier, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL quarantine both Goal Tasks and record the duplicate identifier and source paths in a Quarantine Report.

### Requirement 3: Durable one-at-a-time scheduling and resume

**User Story:** As a developer, I want durable single-task scheduling, so that an interrupted run resumes without repeating completed coding work.

#### Acceptance Criteria

1. WHEN the Stateless Turn Python Orchestrator Pipeline selects a queued Goal Task, THE Stateless Turn Python Orchestrator Pipeline SHALL persist the selected Task Identifier and `in_progress` status in Run State before requesting a Planner Model or Executor Model response.
2. WHILE a Goal Task has `in_progress` status, THE Stateless Turn Python Orchestrator Pipeline SHALL prevent selection or execution of another Goal Task in the same Workspace.
3. WHEN a pipeline run restarts, THE Stateless Turn Python Orchestrator Pipeline SHALL load Run State and resume the recorded `in_progress` Goal Task before selecting the next queued Goal Task.
4. WHEN a Goal Task completes declared validation with a zero exit code, THE Stateless Turn Python Orchestrator Pipeline SHALL persist `completed` status, validation output path, and completion timestamp before selecting another Goal Task.
5. IF Run State is absent or unreadable, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL create a Quarantine Report for the Run State failure and refuse Goal Task execution until valid Run State is restored.

### Requirement 4: Stateless local model planning and execution

**User Story:** As a developer, I want fresh local model requests for planning and coding, so that each Goal Task has bounded task-specific context.

#### Acceptance Criteria

1. WHEN the Stateless Turn Python Orchestrator Pipeline begins planning for a Goal Task, THE Stateless Turn Python Orchestrator Pipeline SHALL send one Fresh Request to the Planner Model identifier `google/gemma-4-12b-qat` through the configured local LM Studio endpoint.
2. WHEN the Stateless Turn Python Orchestrator Pipeline begins coding for a Goal Task, THE Stateless Turn Python Orchestrator Pipeline SHALL send one Fresh Request to the Executor Model identifier `google/gemma-4-e2b` through the configured local LM Studio endpoint.
3. WHEN the Stateless Turn Python Orchestrator Pipeline creates a Fresh Request, THE Stateless Turn Python Orchestrator Pipeline SHALL include the active Goal Task, selected Execution Mode, declared validation block, Workspace-relative active file context, and applicable pipeline rules.
4. WHEN the Stateless Turn Python Orchestrator Pipeline starts a later Goal Task, THE Stateless Turn Python Orchestrator Pipeline SHALL construct a new request payload and SHALL omit prior Goal Task conversational messages from the new request payload.
5. IF the configured local LM Studio endpoint returns a connection error, timeout, or non-success response, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL retain Run State as `in_progress`, preserve Workspace changes, and record the request error, model identifier, timestamp, and Task Identifier in Local AI Storage.

### Requirement 5: Workspace-scoped JSON tool protocol

**User Story:** As a developer, I want model-proposed coding actions constrained by a machine-readable local protocol, so that the pipeline can validate each Workspace action before execution.

#### Acceptance Criteria

1. WHEN the Executor Model proposes a coding action, THE Stateless Turn Python Orchestrator Pipeline SHALL accept the action only as a valid Tool Protocol JSON object containing a protocol version, Task Identifier, Workspace-relative target path, action type, declared arguments, and expected result.
2. WHEN the Stateless Turn Python Orchestrator Pipeline receives a Tool Protocol JSON object, THE Stateless Turn Python Orchestrator Pipeline SHALL resolve every target path against the selected Workspace and reject a target path that resolves outside the Workspace.
3. WHEN the Stateless Turn Python Orchestrator Pipeline completes a Tool Protocol action, THE Stateless Turn Python Orchestrator Pipeline SHALL store a JSON result containing the Task Identifier, action type, resolved Workspace-relative path, result status, timestamp, and error details when applicable in Local AI Storage.
4. IF an Executor Model response is not valid Tool Protocol JSON, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL preserve Workspace changes, retain the Goal Task as `in_progress`, and create a Quarantine Report containing the response text and parse error.

### Requirement 6: Command and mutation safety boundaries

**User Story:** As a developer, I want strict execution boundaries, so that the pipeline performs only task-declared local coding and validation activities.

#### Acceptance Criteria

1. WHEN the Stateless Turn Python Orchestrator Pipeline evaluates a command for execution, THE Stateless Turn Python Orchestrator Pipeline SHALL execute the command only when the command exactly matches a Declared Command for the active Goal Task after normalized whitespace comparison.
2. WHEN the Stateless Turn Python Orchestrator Pipeline evaluates a Tool Protocol action or Declared Command, THE Stateless Turn Python Orchestrator Pipeline SHALL reject actions that invoke Git mutations, create commits, create tags, create branches, push to remotes, access outbound network endpoints, or invoke undeclared commands.
3. IF the Stateless Turn Python Orchestrator Pipeline rejects a Tool Protocol action or Declared Command, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL prevent execution and record the Task Identifier, rejected text, denylist category, and timestamp in Local AI Storage.
4. WHEN the Stateless Turn Python Orchestrator Pipeline executes an accepted Declared Command, THE Stateless Turn Python Orchestrator Pipeline SHALL run the command through PowerShell with the Workspace as the working directory and persist standard output, standard error, exit code, and execution timestamp in Local AI Storage.

### Requirement 7: Execution-mode selection

**User Story:** As a developer, I want execution modes selected from observable task conditions, so that the pipeline supplies task-relevant repair or scaffolding context.

#### Acceptance Criteria

1. WHEN preflight inspection finds that an active Goal Task target path does not exist in the Workspace, THE Stateless Turn Python Orchestrator Pipeline SHALL select `Scaffold` Execution Mode and include the active Goal Task target path in the Executor Model Fresh Request.
2. WHEN preflight inspection finds a missing import, unresolved declared dependency, or mismatched parsed interface signature for an active Goal Task target, THE Stateless Turn Python Orchestrator Pipeline SHALL select `Aligner` Execution Mode and include the detected mismatch in the Executor Model Fresh Request.
3. WHEN preflight inspection finds an existing target path without a missing import, unresolved declared dependency, or mismatched parsed interface signature, THE Stateless Turn Python Orchestrator Pipeline SHALL select `CoT-Task` Execution Mode.
4. WHEN declared PowerShell validation returns a non-zero exit code, THE Stateless Turn Python Orchestrator Pipeline SHALL select `Error` Execution Mode and include the validation standard error and exit code in the next Executor Model Fresh Request.

### Requirement 8: Validation, retries, and partial-change preservation

**User Story:** As a developer, I want declared validation and bounded error recovery, so that coding tasks receive repair attempts without losing useful local changes.

#### Acceptance Criteria

1. WHEN the Executor Model reports completion for a Goal Task, THE Stateless Turn Python Orchestrator Pipeline SHALL execute each Declared Command for the active Goal Task in declaration order before recording `completed` status.
2. WHEN Error Execution Mode is selected for a Goal Task, THE Stateless Turn Python Orchestrator Pipeline SHALL perform no more than three Error Execution Mode Executor Model requests for the Goal Task.
3. WHEN a Goal Task passes all Declared Commands after an Error Execution Mode request, THE Stateless Turn Python Orchestrator Pipeline SHALL record the Goal Task as `completed` and record the total Error Execution Mode request count in Run State.
4. IF a Goal Task has three Error Execution Mode Executor Model requests and a Declared Command still returns a non-zero exit code, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL preserve all current Workspace changes, record the Goal Task as `quarantined`, and create a Markdown Quarantine Report containing the Task Identifier, mode history, validation commands, standard output, standard error, exit codes, retry count, changed Workspace paths, and recovery timestamp.

### Requirement 9: Local storage and low-VRAM configuration telemetry

**User Story:** As a developer, I want local run artifacts and measured low-VRAM settings, so that pipeline behavior can be resumed and evaluated on constrained hardware.

#### Acceptance Criteria

1. WHEN a pipeline run initializes, THE Stateless Turn Python Orchestrator Pipeline SHALL create or reuse Workspace-scoped Local AI Storage without writing Run State, plans, Tool Protocol records, telemetry, validation output, or Quarantine Reports outside the Workspace.
2. WHEN the Stateless Turn Python Orchestrator Pipeline queries the configured local LM Studio runtime, THE Stateless Turn Python Orchestrator Pipeline SHALL record whether Flash Attention, KV cache configuration, and GPU offload configuration are reported as supported by the active runtime.
3. WHERE the configured local LM Studio runtime reports a Low-VRAM Setting as supported, THE Stateless Turn Python Orchestrator Pipeline SHALL allow the Low-VRAM Setting to be configured for a benchmarked run and record the configured value, model identifier, measured elapsed request time, and reported memory telemetry in Local AI Storage.
4. IF the configured local LM Studio runtime does not report a Low-VRAM Setting as supported, THEN THE Stateless Turn Python Orchestrator Pipeline SHALL retain the runtime default for the Low-VRAM Setting and record `unsupported` status without asserting that Flash Attention, KV cache configuration, or GPU offload is active.
5. WHEN a benchmarked run completes, THE Stateless Turn Python Orchestrator Pipeline SHALL persist a telemetry record for each model request containing the Task Identifier, model identifier, Execution Mode, request timestamp, elapsed request time, configured supported Low-VRAM Settings, and reported memory telemetry when available.
