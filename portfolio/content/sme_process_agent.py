"""Public, version-controlled content for the flagship process-agent case study."""

SLUG = "sme-process-discovery-agent"

PROJECT = {
    "slug": SLUG,
    "kind": "personal",
    "title": "SME Process Discovery Agent",
    "summary": (
        "An evidence-aware AI system that investigates how business processes "
        "really work before recommending automation."
    ),
    "problem": (
        "Business processes rarely live in one place. Documented policy, actual "
        "practice, operational systems, and institutional knowledge can disagree. "
        "Automating the first description of a process can simply automate the "
        "wrong process."
    ),
    "solution": (
        "The application conducts a process-discovery interview while consulting "
        "connected business systems through MCP and company documents through RAG. "
        "It captures evidence in application-owned ProcessState, preserves conflicts "
        "and unknowns, and runs an explicit Analyst-to-Designer-to-Verifier pipeline."
    ),
    "outcome": (
        "The result is a deployed public demo that builds an evidence-linked AS-IS "
        "process model and produces an automation proposal that is challenged against "
        "the collected evidence before presentation."
    ),
    "lessons": (
        "Durable process state should not live only in model conversation history. "
        "MCP and RAG solve different integration problems, structured model output "
        "still needs application validation, and AI evals complement rather than "
        "replace deterministic tests."
    ),
    "status": "production",
    "live_url": "https://process-agent.miguelribeiro.dev",
    "source_url": "https://github.com/MiguelRibeiro-Cloud/sme-process-agent",
    "screenshots": (),
}

CASE_STUDY = {
    "kicker": "Evidence-aware AI process discovery",
    "hero": (
        "An AI system that interviews users about business processes, investigates "
        "connected systems and internal documentation, builds a structured AS-IS "
        "model, and produces a verified automation proposal."
    ),
    "meta_description": (
        "Evidence-aware AI process discovery using MCP, RAG, structured state, "
        "explicit orchestration, and behavioral evaluation."
    ),
    "domain": "process-agent.miguelribeiro.dev",
    "card_supporting_copy": (
        "Combines MCP business-system access, semantic document retrieval, "
        "application-owned structured state, explicit orchestration, and behavioral "
        "evaluation in a deployed public demo."
    ),
    "card_tags": ("Python", "FastAPI", "GPT", "MCP", "RAG", "AI Evals"),
    "problem_paragraphs": (
        (
            "Business processes rarely live in one place. The documented procedure "
            "says one thing, employees may actually do another, and critical details "
            "are buried across systems, spreadsheets, emails, and institutional knowledge."
        ),
        "Automating the first description of a process can simply automate the wrong process.",
    ),
    "build_paragraphs": (
        (
            "The application conducts a process-discovery interview while independently "
            "consulting available business systems and internal documentation. Facts are "
            "captured into application-owned structured state rather than left only in "
            "model conversation history."
        ),
        (
            "When discovery has enough substance, an explicit orchestration pipeline "
            "analyzes the AS-IS process, proposes automation opportunities, and verifies "
            "those recommendations against the evidence collected."
        ),
    ),
    "architecture": {
        "application": ("Browser", "FastAPI"),
        "branches": (
            {"title": "Discovery agent", "detail": "GPT model", "note": "Interview and typed patch proposals"},
            {"title": "MCP client", "detail": "Northstar Business Systems MCP server (synthetic demo)", "note": "CRM and pricing capabilities"},
            {"title": "RAG", "detail": "Embedding model + company documents", "note": "Semantic company knowledge"},
            {"title": "ProcessState", "detail": "Application-owned structured model", "note": "Evidence, branches, conflicts, and unknowns"},
        ),
        "orchestration": ("Process Analyst", "Automation Designer", "Evidence Verifier"),
        "caption": (
            "MCP handles operational capabilities. RAG handles semantic company "
            "knowledge. The application owns state and orchestration."
        ),
    },
    "engineering_decisions": (
        {"title": "Application-owned state", "copy": "Model output proposes typed patches; Python validates and owns the durable process model."},
        {"title": "Evidence provenance", "copy": "User-reported practice, documented policy, MCP system facts, and unresolved unknowns stay distinguishable."},
        {"title": "Explicit orchestration", "copy": "Analyst → Designer → Verifier is application-controlled rather than autonomous agent-to-agent conversation."},
        {"title": "Observable by design", "copy": "The execution trace is generated from real backend events—no fake model ‘thinking’."},
    ),
    "discovery_example": {
        "company_note": "Northstar Industrial Services is a fictional demo company using synthetic data.",
        "claims": (
            {"label": "Reported practice", "quote": "No management approval unless the discount is above 15%."},
            {"label": "Documented policy", "quote": "Sales Manager approval is required above 10%."},
        ),
        "result": (
            "The system preserves both claims and creates an unresolved policy/practice "
            "conflict rather than silently choosing one. Above 15%, it can then map the "
            "manual path: Sales emails Marta → Marta prints → signs → scans → emails back "
            "→ Sales waits."
        ),
    },
    "orchestration": (
        {"title": "Process Analyst", "copy": "Identifies bottlenecks, handoffs, gaps, duplicate work, and unresolved questions."},
        {"title": "Automation Designer", "copy": "Proposes TO-BE improvements while preserving required human decisions and documenting assumptions and dependencies."},
        {"title": "Evidence Verifier", "copy": "Challenges each recommendation against the evidence and marks it supported, partially supported, unsupported, or blocked by unknown information. It is not designed to rubber-stamp the proposal."},
    ),
    "evaluation": {
        "intro": "Traditional tests can prove that software behaves as programmed. They cannot fully prove that a nondeterministic AI system behaves as intended.",
        "strategy": (
            "Deterministic checks where Python can inspect behavior objectively",
            "Semantic LLM judging only where meaning requires interpretation",
            "Scenario-based regression testing",
            "Visible failures retained as regression signals",
        ),
        "release": "The final release snapshot passed 35/37 behavioral criteria across 11 scenarios, with 9/11 scenario runs passing. This is a regression signal, not a claim of ‘91% AI accuracy’.",
        "signals": ("Capability routing 11/11", "RAG grounding 4/4", "Conflict preservation 3/3", "Verifier calibration 2/2"),
    },
    "hardening": (
        "Anonymous cookie-backed session isolation",
        "Per-session ProcessState and conversation context",
        "Rate and lifetime request limits",
        "Global model-operation emergency fuse",
        "Restricted MCP subprocess environment",
        "Safe Markdown and DOM rendering",
        "Non-root Docker runtime",
        "Secure production cookies and health checks",
        "Explicit synthetic RAG release artifact",
    ),
    "deployment": "The application is containerized with Docker, deployed on Railway, and served through a custom domain. It deliberately runs one application worker because session state is currently held in memory. Horizontal scaling would require moving that state to shared storage such as Redis or a database.",
    "role": "My role: system architecture, product design, AI-system behavior, trust boundaries, state model, evaluation strategy, technical direction, and deployment—using AI coding agents heavily for implementation.",
    "judgment": (
        "Durable state belongs outside model history",
        "MCP and RAG address different integration needs",
        "Structured outputs remain proposals until application validation accepts them",
        "AI evals and deterministic tests measure different failure modes",
        "Public AI demos need spend controls and session isolation",
        "Visible AI activity should correspond to actual system events",
    ),
    "stack": (
        {"label": "Backend", "items": "Python, FastAPI, Pydantic"},
        {"label": "AI", "items": "OpenAI Responses API, GPT-6 Luna, text-embedding-3-small"},
        {"label": "Agent architecture", "items": "Tool calling, MCP, RAG, Structured Outputs, application-controlled orchestration"},
        {"label": "Frontend", "items": "HTML, CSS, JavaScript, SSE"},
        {"label": "Quality", "items": "unittest, deterministic integration tests, AI eval harness, browser smoke tests"},
        {"label": "Deployment", "items": "Docker, Railway, Cloudflare DNS/custom domain"},
    ),
    "visual_placeholders": (
        {"filename": "sme-process-agent-discovery.png", "title": "Discovery interface", "description": "Conversation and real Agent Activity events"},
        {"filename": "sme-process-agent-process-model.png", "title": "Structured process model", "description": "Policy/practice conflict and branch-aware process flow"},
        {"filename": "sme-process-agent-orchestration.png", "title": "Verified proposal", "description": "Process Analyst, Automation Designer, and Evidence Verifier"},
    ),
}
