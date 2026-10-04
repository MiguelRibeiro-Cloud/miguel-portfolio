"""Public case-study content synchronized by the seed_portfolio command."""

from .sme_process_agent import PROJECT as SME_PROCESS_AGENT

PROJECTS = (
    SME_PROCESS_AGENT,
    {
        "slug": "standardized-reporting-workflow",
        "kind": "professional",
        "title": "Standardized Reporting Workflow",
        "summary": (
            "An Excel/VBA ETL and reporting automation for Cisco Asset Management "
            "that evolved into Python-backed processing in an internal application."
        ),
        "problem": (
            "Reporting depended on multiple manual deliverables and scattered source "
            "files. The process involved repeated work, inconsistent outputs, "
            "and opportunities for input errors."
        ),
        "solution": (
            "I first built an Excel/VBA ETL workflow that ingested, transformed, "
            "and consolidated roughly 15 source files. It calculated reporting "
            "outputs and refreshed PivotTables and charts automatically.\n\n"
            "I later moved the processing into a Python backend within an internal "
            "application. That work included data transformation, Excel generation "
            "and modification using OOXML, input validation, backend error handling, "
            "and frontend feedback for common input mistakes."
        ),
        "outcome": (
            "The workflow became part of an internal system used to generate "
            "standardized customer-facing reporting. The Python implementation "
            "improved processing capability, maintainability, support for larger "
            "datasets, and the feedback users receive when inputs need correction."
        ),
        "lessons": (
            "Moving a working spreadsheet automation into an application required "
            "more than transferring calculations. Input validation, maintainable "
            "processing, and actionable error feedback became part of the solution."
        ),
        "status": "production",
        "live_url": "",
        "source_url": "",
        "screenshots": (),
    },
    {
        "slug": "customer-context-knowledge-capture-tool",
        "kind": "professional",
        "title": "Customer Context / Knowledge Capture Tool",
        "summary": (
            "A Python document-processing and retrieval tool that made information "
            "from more than 700 DOCX files accessible through search and an "
            "AI-assisted interface."
        ),
        "problem": (
            "A shared delivery model increased the need to preserve and update "
            "customer context. That information was "
            "spread across a large collection of Word documents."
        ),
        "solution": (
            "I built a Python ingestion process for more than 700 DOCX files and "
            "stored extracted information in a relational database. A web UI "
            "provided conventional search and navigation alongside an AI-assisted "
            "conversational interface. The ingestion process also identified "
            "documents it could not parse so they could be reviewed."
        ),
        "outcome": (
            "The prototype demonstrated that a large collection of unstructured "
            "documents could be converted into structured, searchable context while "
            "also supporting conversational retrieval. Failed ingestion cases remained "
            "visible for human review rather than being silently discarded."
        ),
        "lessons": (
            "A retrieval interface depends on reliable ingestion as well as search. "
            "Identifying documents that could not be parsed was part of making "
            "the captured information useful."
        ),
        "status": "prototype",
        "live_url": "",
        "source_url": "",
        "screenshots": (),
    },
    {
        "slug": "livedhere-pt",
        "kind": "personal",
        "title": "livedhere.pt",
        "summary": (
            "A personal place-to-live review platform for sharing experiences "
            "at specific locations, built with a Python backend, React frontend, "
            "and Azure deployment."
        ),
        "problem": (
            "After a poor rental experience, I wanted a way for people to share "
            "what it was like to live at a specific location. The idea called "
            "for location-based reviews with attention to privacy."
        ),
        "solution": (
            "I built a Python backend and React frontend with a SQL database, "
            "interactive mapping, passwordless magic-link authentication, and "
            "AI functionality. The application has used Azure services for "
            "containerized deployment and managed database infrastructure, with "
            "privacy-conscious design throughout."
        ),
        "outcome": (
            "The application is live in production on Azure. It demonstrates "
            "end-to-end ownership of a public full-stack product, from "
            "location-specific reviews and SQL persistence to interactive maps, "
            "passwordless authentication, and AI functionality."
        ),
        "lessons": (
            "The project gave me end-to-end experience beyond application code: "
            "authentication, database design, location-based UX, privacy decisions, "
            "cloud deployment, and operating a full-stack application as a connected "
            "system."
        ),
        "status": "production",
        "live_url": "https://www.livedhere.pt/en",
        "source_url": "",
        "screenshots": (
            {
                "image_path": "portfolio/projects/livedhere/livedhere_main.png",
                "caption": "LiveHere homepage with search, privacy-focused messaging, and the AI assistant.",
                "sort_order": 1,
            },
            {
                "image_path": "portfolio/projects/livedhere/livedhere_map.png",
                "caption": "Location search and interactive map for exploring reviewed places.",
                "sort_order": 2,
            },
            {
                "image_path": "portfolio/projects/livedhere/livedhere_review.png",
                "caption": "Detailed building review showing category ratings, overall score, and written feedback.",
                "sort_order": 3,
            },
        ),
    },
    {
        "slug": "the-judge-aita-ai-chatbot",
        "kind": "personal",
        "title": "The Judge — AITA AI Chatbot",
        "summary": (
            "A public AI courtroom app that turns everyday disagreements into "
            "humorous rulings, built with React, Python Azure Functions, "
            "Google GenAI, and PostgreSQL."
        ),
        "problem": (
            "Users submit disagreements and petty dilemmas for humorous courtroom "
            "rulings. Making that simple interaction reliable in a public serverless "
            "app meant handling variable model responses, bounded conversation "
            "context, input validation, provider failures, shared state, and "
            "verdicts that agree with the UI."
        ),
        "solution": (
            "I built the React frontend on Azure Static Web Apps and a same-origin "
            "Python Azure Functions backend that calls Google GenAI. Credentials "
            "stay server-side; the backend validates input, bounds conversation "
            "history, and handles timeouts and provider errors. PostgreSQL holds "
            "the deployment-wide case counter outside serverless function memory.\n\n"
            "After free-form replies proved brittle, I moved the model to structured "
            "verdict, ruling, and consequence fields. Python validates those fields "
            "and owns the final response structure; React derives the YTA/NTA badge "
            "from the validated verdict. User messages are treated as case material."
        ),
        "outcome": (
            "The app is live in production, turning submitted dilemmas into "
            "conversational courtroom rulings. Its validated verdict drives the "
            "displayed badge, and PostgreSQL keeps the case counter shared across "
            "serverless instances."
        ),
        "lessons": (
            "Free-form model output is a poor application contract; validated "
            "fields are safer than parsing prose. External AI providers need "
            "validation and failure handling, and user content needs a clear "
            "boundary from system instructions. Shared serverless state belongs "
            "in persistent storage; optional features should not block a ruling."
        ),
        "status": "production",
        "live_url": "https://www.amitheassholeai.com/",
        "source_url": "",
        "screenshots": (
            {
                "image_path": "portfolio/projects/aitabot/normal.png",
                "caption": "A completed courtroom ruling showing the conversation and YTA verdict badge.",
                "sort_order": 1,
            },
            {
                "image_path": "portfolio/projects/aitabot/main.png",
                "caption": "The Judge's main interface with service status, case count, and conversation entry point.",
                "sort_order": 2,
            },
            {
                "image_path": "portfolio/projects/aitabot/prompt_cake_injection.png",
                "caption": "An out-of-role cake request treated as case material and returned as a normal courtroom ruling.",
                "sort_order": 3,
            },
            {
                "image_path": "portfolio/projects/aitabot/disclaimer.png",
                "caption": "First-use privacy and entertainment disclosure shown before entering the application.",
                "sort_order": 4,
            },
        ),
    },
    {
        "slug": "the-fog-book-as-code",
        "kind": "learning",
        "title": "The Fog — Book as Code",
        "summary": (
            "A human-directed, repository-driven AI-assisted long-form fiction experiment. "
            "Manuscript, plans, continuity state, and agent instructions live together "
            "so a chapter can begin from a minimal task prompt."
        ),
        "problem": (
            "Long-running AI-assisted writing can depend on chat history or large "
            "manually assembled prompts. I tested whether durable repository context "
            "could support continuity across a large manuscript while leaving "
            "creative decisions with a human."
        ),
        "solution": (
            "I separated Manuscript (established prose and events), Narrative (future "
            "plans and beats), Characters (reference), World (canon and knowledge "
            "boundaries), and State (compact current continuity). AGENTS.md defines "
            "retrieval, domain-specific authority, drafting, revision, review, and "
            "State maintenance. A chapter begins with: \"Write Chapter X. Follow the "
            "repository instructions.\" The agent retrieves relevant context selectively "
            "instead of loading everything.\n\n"
            "The instructions distinguish established facts, future plans, reference "
            "canon, and derived State. State serves as constraint memory, including "
            "current continuity and reveal boundaries, rather than creative source "
            "material. The agent updates materially affected State after drafting. "
            "Major contradictions and consequential new canon require human review; "
            "I review, edit, redirect, reject, or request revisions before accepting "
            "chapters."
        ),
        "outcome": (
            "At the time of this case study, the repository held approximately "
            "29 manuscript chapters, 164,700 manuscript words, 541 numbered "
            "narrative planning beats, 37 world-reference files, 8 character-reference "
            "files, 10 State files, and a substantial repository-level agent "
            "instruction specification. The long-running project was maintained "
            "with repository-contained context and relatively little dependence "
            "on individual chat sessions."
        ),
        "lessons": (
            "Durable context can live outside chat history. Different kinds of "
            "information need distinct sources of authority and selective retrieval. "
            "Context also needs structure and lifecycle rules: State summaries help "
            "with continuity but can drift unless maintained. Human judgment remains "
            "necessary for creative direction and genuine ambiguity, while "
            "natural-language agent instructions remain probabilistic rather than "
            "enforced."
        ),
        "status": "experiment",
        "live_url": "",
        "source_url": "",
        "screenshots": (),
    },
)
