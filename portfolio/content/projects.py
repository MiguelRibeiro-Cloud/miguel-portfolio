"""Public case-study content synchronized by the seed_portfolio command."""

PROJECTS = (
    {
        "slug": "standardized-reporting-workflow",
        "kind": "professional",
        "title": "Standardized Reporting Workflow",
        "summary": (
            "An Excel/VBA ETL and reporting automation for Cisco Asset Management "
            "that evolved into Python-backed processing in an internal application."
        ),
        "problem": (
            "Reporting depended on multiple manual deliverables and scattered data "
            "sources. The process involved repeated work, inconsistent outputs, "
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
            "A pooled delivery model created a need to preserve operational "
            "knowledge and retrieve relevant context. That information was "
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
            "The application reached a working Azure deployment, combining "
            "location-specific reviews, interactive mapping, passwordless "
            "authentication, SQL-backed persistence, and AI-assisted functionality "
            "in a live full-stack application."
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
)
