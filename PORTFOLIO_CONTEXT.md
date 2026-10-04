# Portfolio Context

This file is the authoritative context for AI coding agents working on this repository.

Read this file before making decisions about public content, positioning, project descriptions, homepage copy, case studies, skills, or portfolio structure.

Do not invent facts to fill gaps.

---

# 1. Portfolio Owner

## Name

Miguel Ribeiro

## Professional direction

Miguel is moving toward increasingly technical roles involving:

- automation engineering
- software engineering
- Python/backend development
- cloud engineering
- infrastructure and deployment
- technical problem solving

The portfolio should demonstrate both what he has already built and the engineering skills he is deliberately developing.

## Career background

Miguel did not begin his career in software.

He previously worked professionally in hospitality and kitchens, with chef and sous-chef roles in Portugal, Germany and Australia.

He later transitioned into technology after formal training in ISCTE for networking and cybersecurity.

He currently works at Cisco in an Asset Management / technical operations environment.

His work has increasingly moved toward building software and automation solutions for operational problems.

This career transition is useful context, but it should not dominate every page.

The important narrative is:

> Miguel developed strong operational problem-solving skills in previous careers and now applies those skills to building practical technical systems.

Avoid overly dramatic or inspirational career-change language.

---

# 2. Professional Positioning

Miguel should not be presented as a conventional lifelong software developer.

A more accurate positioning is:

> A technical builder who identifies operational problems, understands workflows and requirements, and builds practical software and automation solutions to improve them.

He works particularly well at the intersection of:

- operational understanding
- automation
- data processing
- Python
- internal tools
- web applications
- cloud infrastructure

The portfolio should demonstrate evidence rather than relying on generic claims such as:

- passionate developer
- technology enthusiast
- innovative thinker
- results-driven professional

Prefer showing actual systems, decisions, problems, and outcomes.

---

# 3. Current Professional Environment

Miguel works at Cisco.

Public descriptions of Cisco work must be deliberately sanitized.

The portfolio should demonstrate engineering skill while also demonstrating that Miguel can be trusted with employer and customer information.

A prospective employer should come away thinking:

> This person can explain meaningful enterprise technical work without exposing confidential information.

Never expose:

- customer identities
- internal URLs
- internal application names unless explicitly approved
- proprietary system names
- confidential architecture
- credentials
- secrets
- internal infrastructure details
- sensitive operational processes
- confidential metrics
- private source code
- customer-specific data

When uncertain, describe the engineering problem at a higher level rather than guessing.

Do not invent metrics.

---

# 4. Major Professional Work

## Standardized Reporting Workflow

### Context

A professional automation project created within Cisco Asset Management.

The existing public portfolio title is:

**Standardized Reporting Workflow**

### Problem

The reporting process depended on multiple manual deliverables and scattered data sources.

This created:

- repeated manual work
- inconsistent outputs
- unnecessary complexity
- opportunities for user input errors

### Initial solution

Miguel built an Excel/VBA ETL and reporting automation.

It processed roughly 15 data sources or source files.

The workflow included:

- data ingestion
- transformation
- consolidation
- calculation of reporting outputs
- automatic refreshing of PivotTables and charts

The Excel/VBA system should accurately be described as:

**Excel/VBA ETL and reporting automation**

### Evolution

The workflow was later migrated to a Python-backed implementation integrated into an internal application.

Miguel worked on:

- Python backend processing
- data transformation
- Excel generation and modification
- OOXML-based Excel handling
- input validation
- backend error handling
- frontend feedback for common input mistakes

The error-handling work helped users identify and correct problems themselves rather than relying unnecessarily on product-team support.

### Public outcome

Safe public framing:

The workflow became part of an internal system used to generate standardized customer-facing reporting.

The Python implementation improved:

- scalability
- processing capability
- maintainability
- user feedback
- ability to handle larger datasets

Do not expose internal application names or unsupported usage/adoption metrics.

---

# 5. Customer Context / Knowledge Capture Tool

This is another professional internal project.

Do not expose its internal product name.

## Problem

A pooled delivery model created a need to preserve operational knowledge and make existing customer/context information easier to retrieve.

Relevant information existed across a large collection of Word documents.

## Solution

Miguel built a system that:

- processed more than 700 DOCX files
- extracted information using Python
- stored structured information in a relational database
- provided a UI for finding relevant context
- supported conventional search/navigation
- included an AI-assisted conversational interface

The ingestion process also identified documents that could not be parsed successfully so they could be reviewed.

## Public positioning

This project demonstrates:

- Python document processing
- data ingestion
- database design/use
- search and retrieval
- web application development
- practical LLM integration
- operational knowledge management

Do not expose:

- customer names
- internal forms
- proprietary workflows
- internal infrastructure
- confidential business processes

---

# 6. Personal Projects

## SME Process Discovery Agent

The SME Process Discovery Agent is a personal production project and the strongest
current public example of Miguel's AI-system engineering work.

Live application:

https://process-agent.miguelribeiro.dev

Public repository:

https://github.com/MiguelRibeiro-Cloud/sme-process-agent

### Purpose

The application is an evidence-aware AI process-discovery system. It:

- interviews users about business processes
- investigates connected operational systems through MCP
- retrieves relevant internal documentation through RAG
- builds an explicit, application-owned AS-IS process model
- preserves evidence provenance, uncertainty, branches, and conflicting claims
- produces an automation proposal through an explicit Analyst → Designer → Verifier pipeline

It should not be presented as merely a chatbot.

### Verified architecture and engineering characteristics

- Python, FastAPI, and Pydantic backend
- OpenAI Responses API
- GPT-6 Luna
- text-embedding-3-small
- tool calling
- MCP integration through an application-controlled client
- semantic document retrieval through RAG
- typed structured model output proposed as ProcessState patches
- Python validation and application ownership of ProcessState
- branch-aware process modeling
- evidence provenance and policy/practice conflict preservation
- application-controlled Process Analyst → Automation Designer → Evidence Verifier orchestration
- deterministic validation and integration tests
- scenario-based AI behavioral evaluations
- semantic LLM judging only where meaning requires interpretation
- SSE activity based on real backend events rather than fabricated model thinking
- HTML, CSS, and JavaScript frontend
- Docker deployment on Railway with a custom domain

MCP handles operational capabilities. RAG handles semantic company knowledge. The
application owns state and orchestration. Do not imply that the model communicates
with MCP directly.

### Evaluation snapshot

The final release evaluation snapshot passed:

- 9 of 11 scenario runs
- 35 of 37 behavioral criteria
- capability routing: 11/11
- RAG grounding: 4/4
- conflict preservation: 3/3
- verifier calibration: 2/2

These figures are regression signals, not a claim that the AI is "91% accurate."
Failures remain visible rather than being hidden behind a vanity score.

### Public-demo hardening and deployment boundary

Implemented public-demo controls include:

- anonymous cookie-backed session isolation
- per-session ProcessState and conversation context
- rate and lifetime request limits
- a global model-operation emergency fuse
- a restricted MCP subprocess environment
- safe Markdown and DOM rendering
- non-root Docker runtime
- secure production cookies
- health checks
- an explicit synthetic RAG release artifact

Describe these as public-demo hardening, not enterprise security.

The Railway deployment deliberately runs one application worker because session
state is currently in memory. Horizontal scaling would require shared state such as
Redis or a database. Redis is not currently implemented in this project.

### Demo data and contribution

Northstar Industrial Services is a fictional demo company using synthetic data. Do
not imply that Northstar is a real company or customer.

Miguel designed the system architecture, product behavior, trust boundaries, state
model, evaluation strategy, technical direction, and deployment approach. He used
AI coding agents heavily for implementation. Do not imply that he manually typed
every line of code, and do not frame AI-assisted implementation defensively.

## livedhere.pt

livedhere.pt is a personal project created after a poor rental experience.

The concept is a place-to-live review platform allowing people to review their experience of living at very specific locations.

Relevant engineering experience includes:

- Python backend
- React frontend
- SQL database
- Azure deployment
- interactive mapping
- passwordless / magic-link authentication
- AI functionality
- privacy-conscious application design

The project has used Azure services including containerized deployment and managed database infrastructure.

Do not invent:

- user counts
- commercial success
- adoption statistics
- traffic metrics

unless explicitly added later.

---
# Personal Project: The Judge / AITA AI Chatbot

The Judge is a personal production project.

Live application:

https://www.amitheassholeai.com/

The project is intentionally playful: users submit disagreements, petty dilemmas, or similar situations and receive a humorous courtroom-style guilty/not-guilty ruling.

## Current production architecture

Browser
→ React frontend
→ Azure Static Web Apps
→ same-origin Python Azure Functions
→ Google GenAI
→ PostgreSQL for deployment-wide shared state

## Verified technologies

- React
- JavaScript
- Python
- Azure Functions
- Azure Static Web Apps
- Google GenAI
- PostgreSQL
- GitHub Actions
- server-side environment configuration

## Implemented engineering characteristics

The application includes:

- conversational AI interaction
- bounded short-session conversation history
- server-side LLM credentials
- input validation
- timeout and provider-error handling
- retry and cancellation UX
- copy / clear / transcript-export controls
- responsive UI
- privacy and terms disclosures
- restricted Markdown rendering
- production security headers
- automated Python tests
- PostgreSQL-backed deployment-wide case counter

Conversations are not intentionally persisted as server-side chat transcripts.

The global case counter is stored outside ephemeral serverless function instances.

## LLM output handling

Earlier versions relied more heavily on free-form model output and defensive text cleanup.

This proved brittle when adversarial or out-of-role user messages caused the model to expose drafting or instruction-related commentary.

The current implementation uses structured model output with three validated fields:

- verdict: `guilty` or `not_guilty`
- ruling
- consequence

Python owns the final response structure rather than relying on the model to format the public reply correctly.

The frontend derives the displayed YTA/NTA badge directly from the validated structured verdict.

User-submitted messages are explicitly treated as case material rather than model instructions.

Requests such as:
- recipe requests
- role-change attempts
- system-prompt requests

are treated as material for the Judge to rule on rather than instructions to follow.

Do not describe this as complete protection against all prompt injection. It is a deliberately stronger trust boundary and structured-output approach.

## Streaming clarification

The application uses an SSE-compatible response path, but the current backend buffers the provider response before returning the final result.

Do not describe the current implementation as true token-by-token or real-time streaming.

## Public portfolio presentation

Classification:

- kind: personal
- status: production

Live URL:

https://www.amitheassholeai.com/

Do not add a public source/GitHub link yet.

The repository has been cleaned enough for internal confidence, but source-code presentation is intentionally deferred.

Approved portfolio screenshots:

1. Normal completed ruling
2. Main / landing state
3. Prompt-injection / cake request handled as case material
4. Privacy / disclaimer view

The normal ruling should be the primary screenshot.

## Public positioning

The project is useful portfolio evidence because it demonstrates:

- React application development
- Python serverless APIs
- LLM integration
- structured model output
- prompt-boundary design
- defensive validation
- external API failure handling
- shared state in serverless systems
- PostgreSQL integration
- Azure deployment
- practical iteration after real model-output failure modes

Do not invent:
- user counts
- traffic
- adoption
- uptime
- commercial success
- cost savings

## Book as Code / The Fog

Classification: learning / experiment

The Fog is a human-directed, repository-driven AI-assisted long-form fiction experiment.

The central experiment was whether a coding/writing agent could produce coherent long-form work from an extremely small per-task instruction:

    Write Chapter X. Follow the repository instructions.

Instead of placing story context into each prompt, durable context and operating rules were externalized into the repository.

The repository separates:

- Manuscript — established prose and events
- Narrative — future story planning and routing
- Characters — character reference
- World — setting and world canon
- State — compact continuity and current-state memory
- AGENTS.md — repository-wide instructions governing retrieval, authority, drafting, revision, and state updates

Agents are expected to discover the relevant context selectively, draft the chapter, preserve established continuity, and update materially affected State files.

The human remains the final creative authority: chapters are reviewed, edited, redirected, or revised before acceptance.

At the time the portfolio case study was created, the project contained approximately:

- 29 chapters
- 164,700 manuscript words
- 541 numbered narrative planning beats
- 37 world-reference files
- 8 character-reference files
- 10 state files
- a substantial repository-level agent instruction specification

The project demonstrates document-level context engineering, persistent project state, selective context retrieval, domain-specific authority rules, continuity management, and human review gates.

It does NOT include a custom agent runtime, RAG/vector database, automated continuity validation, multi-agent orchestration, model training, or autonomous novel generation.

Best public framing:

“Designing a repository-resident context and continuity system for human-directed, agent-assisted long-form fiction under minimal per-chapter prompting.”

The GitHub repository is private because it contains the unpublished manuscript, future narrative plans, spoilers, and worldbuilding.

Public portfolio material should use only sanitized/cropped artifacts such as:

- the minimal chapter prompt beside the repository structure
- selected AGENTS.md authority/retrieval rules
- sanitized Narrative routing/index structure
- State category structure without story-specific contents


# 7. Other Relevant Technical Work

Miguel has also built or worked with:

- React applications
- TypeScript
- Flask
- FastAPI
- Django
- Python APIs
- LLM-powered chat interfaces
- streaming LLM responses
- Azure Functions
- PostgreSQL-backed applications
- MySQL
- SQLite
- pandas
- Excel automation
- VBA
- GitHub Actions
- Docker

Only surface these where they strengthen the portfolio narrative.

Avoid building a giant undifferentiated technology-logo wall.

---

# 8. Networking and Infrastructure Background

Miguel entered technology through networking and cybersecurity training.

Relevant background includes:

- CCNA
- networking fundamentals
- routing and switching
- cybersecurity training
- Azure experience

He is continuing to deepen his knowledge of:

- cloud infrastructure
- AWS
- Infrastructure as Code
- Terraform
- containers
- Kubernetes
- observability
- security / IAM
- production engineering

Important:

Do not present technologies currently being learned as established professional expertise.

The portfolio should make a clear distinction between:

1. demonstrated experience
2. technologies implemented in this portfolio
3. technologies currently being learned

---

# 9. AI-Native Engineering Workflow

Miguel uses AI coding agents extensively.

This should not be hidden or treated defensively.

His engineering workflow increasingly involves:

- defining problems and requirements
- making architecture decisions
- giving scoped implementation work to coding agents
- reviewing generated code
- testing behaviour
- debugging failures
- understanding infrastructure and system behaviour
- refining solutions iteratively

The portfolio should not falsely imply that every line of code was manually typed.

The value being demonstrated is the ability to design, build, understand, debug, and deliver technical systems effectively.

---

# 10. This Portfolio Is Also an Engineering Project

The portfolio itself is intentionally being used as a practical engineering laboratory.

## Currently implemented

The portfolio currently uses:

- Django
- PostgreSQL
- Django Admin
- Django templates
- environment-based configuration
- Gunicorn
- WhiteNoise
- Docker
- Docker Compose
- separate Django and PostgreSQL containers locally
- Docker-managed persistent database volumes
- database health checks
- automated Django tests
- PostgreSQL-backed GitHub Actions CI
- feature branches
- Pull Requests
- CI-gated deployment
- Railway production deployment
- canonical public portfolio URL: https://miguelribeiro.dev
- production canonical-host behavior derived from `PUBLIC_SITE_URL`
- production Docker builds
- pre-deployment Django migrations
- public health endpoint

These technologies may be described as implemented.

## Not yet implemented

The following are roadmap technologies and must NOT currently be presented as completed:

- Redis
- Celery
- production background jobs
- AWS deployment
- Terraform
- Kubernetes
- advanced observability stack
- production Infrastructure as Code

These may be described as learning goals or roadmap items where appropriate.

---

# 11. Planned AI Portfolio Assistant

A public-facing AI Assistant is planned shortly after the main portfolio pages are completed.

Do not implement it unless explicitly requested.

The assistant will allow visitors to ask questions such as:

- What automation work has Miguel done?
- What Python experience does Miguel have?
- Which projects demonstrate backend engineering?
- What cloud platforms has Miguel worked with?
- What is Miguel currently learning?
- How did Miguel transition into technology?

The assistant should eventually use curated portfolio/career/project information as its knowledge base.

It must:

- remain grounded in known information
- avoid inventing experience
- avoid exposing confidential information
- distinguish demonstrated experience from learning goals

A lightweight architecture is preferred initially.

A vector database or complex RAG system should not be introduced unless the amount of portfolio knowledge makes it useful.

---

# 12. Public Portfolio Goals

The website has two equally important purposes.

## Professional purpose

Help recruiters and hiring managers quickly understand:

- who Miguel is
- what he builds
- what problems he solves
- what technical experience he has
- what direction his career is taking

A visitor should understand the core value proposition within approximately 10–20 seconds.

## Engineering purpose

Provide tangible evidence that Miguel can build and operate increasingly production-like systems.

The portfolio itself should progressively become evidence of engineering knowledge.

---

# 13. Homepage Direction

The homepage should clearly communicate:

- Miguel Ribeiro
- automation / software / cloud direction
- practical engineering mindset
- career transition into technology
- selected project evidence

Useful sections include:

- strong hero / introduction
- selected work
- capabilities / areas of engineering
- portfolio engineering / how this site is built
- GitHub / project call to action

Avoid overwhelming visitors with biography before showing technical relevance.

---

# 14. Case Study Direction

Project pages should read like concise engineering case studies.

Existing Project model content includes:

- title
- slug
- summary
- problem
- solution
- outcome
- lessons
- status

The preferred structure is approximately:

1. Context / summary
2. Problem
3. Engineering approach / solution
4. Outcome
5. Lessons / growth

Project content should remain data-driven through Django/Admin rather than being hardcoded into templates wherever practical.

---

# 15. Design Direction

The visual direction should be:

- modern
- restrained
- technical
- professional
- readable
- responsive

The existing dark design system can be evolved rather than replaced without reason.

Prefer:

- strong typography
- clear hierarchy
- generous spacing
- evidence-driven content
- restrained visual effects

Avoid:

- excessive gradients
- glowing neon everywhere
- meaningless animated backgrounds
- giant technology-logo walls
- percentage-based skill bars
- gratuitous animations
- generic SaaS layouts
- generic AI-generated portfolio aesthetics
- excessive buzzwords

The portfolio should feel like the work of a practical engineer.

---

# 16. Content Tone

Preferred writing style:

- clear
- direct
- specific
- technically credible
- confident without exaggeration

Avoid:

- corporate filler
- motivational language
- excessive self-praise
- inflated claims
- unnecessary adjectives

Prefer:

> Built a Python pipeline that processed...

over:

> Passionately leveraged cutting-edge technologies to revolutionize...

---

# 17. Accuracy Rules for Agents

When working on public content:

1. Never invent facts.
2. Never invent metrics.
3. Never infer technologies that are not documented.
4. Never expose secrets or confidential employer information.
5. Never turn a learning goal into claimed experience.
6. Preserve meaningful technical specificity where it is safe.
7. If information is uncertain, leave it general or request clarification.
8. Existing repository content and this file should be treated as the primary sources of truth.

---

# 18. Engineering Rules for Agents

Before modifying the repository:

1. Inspect the existing architecture.
2. Reuse existing patterns where sensible.
3. Avoid unnecessary dependencies.
4. Do not change infrastructure or deployment configuration unless the task requires it.
5. Do not weaken tests to make changes pass.
6. Preserve existing routes unless explicitly changing them.
7. Run relevant tests after implementation.
8. Do not commit or push unless explicitly instructed.
9. Never place credentials or secrets into source control.
10. Treat `main` as the production branch.

For significant changes, prefer:

feature branch
→ implementation
→ tests
→ Pull Request
→ CI
→ merge
→ deployment

---

# 19. Current Near-Term Roadmap

Current intended sequence:

1. Strengthen homepage
2. Build polished portfolio/case-study experience
3. Add public AI Portfolio Assistant
4. Improve Docker-aware CI and observability
5. Introduce a meaningful background-job use case with Redis/Celery
6. Begin AWS infrastructure work
7. Introduce Terraform / Infrastructure as Code
8. Explore Kubernetes once there is a genuine containerized system worth orchestrating

The roadmap may evolve.

Do not implement future roadmap items simply because they appear here.

---

# 20. Primary Principle

The portfolio should demonstrate:

> Miguel can understand a real problem, make sensible technical decisions, use modern tools effectively, and deliver a working solution.

Evidence matters more than buzzwords.
