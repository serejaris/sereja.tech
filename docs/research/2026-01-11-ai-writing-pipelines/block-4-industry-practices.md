# Block 4: Industry Practices

## Sources

### 1. [Common workflows - Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/common-workflows)
**Relevance:** high
**Key ideas:**
- Anthropic documents complete developer workflows: understanding codebases, fixing bugs, refactoring, using specialized subagents, safe code analysis in Plan Mode
- Plan Mode enables read-only exploration for complex multi-step changes before making edits
- Subagents provide task-specific capabilities (code review, debugging)
**Who:** Anthropic
**What works:** Structured workflow patterns with safety modes, specialized agents for different development phases

### 2. [Automate Your Documentation with Claude Code & GitHub Actions](https://medium.com/@fra.bernhardt/automate-your-documentation-with-claude-code-github-actions-a-step-by-step-guide-2be2d315ed45)
**Relevance:** high
**Key ideas:**
- Two workflows: PR-triggered docs updater (updates docs when code changes) and scheduled docs maintainer (daily review)
- Uses Claude Sonnet 4.5 via GitHub Actions to analyze code diffs and commit documentation updates
- Consolidates 24-hour commit history into single documentation updates
**Who:** Anthropic + individual practitioner
**What works:** Automated documentation maintenance tied to code changes, scheduled reviews for consistency

### 3. [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
**Relevance:** high
**Key ideas:**
- Use `claude.files` for persistent context (common commands, style guidelines, repository etiquette)
- Tool management via `/permissions` command controls what actions Claude can take
- Multi-Claude workflows for parallel execution, headless mode for automation
**Who:** Anthropic Engineering
**What works:** Context files for consistency, permission-based tool control, automation-first approach

### 4. [Run, iterate, and scale your course content creation - Disco](https://www.disco.co/cohort-based-course-playbook-chapter/course-content-creation)
**Relevance:** medium
**Key ideas:**
- Disco AI generates entire modules (titles, images, content) from prompts
- Content duplication and customization for scaling across cohorts
- Focus on net-new content generation using AI as baseline
**Who:** Disco (cohort-based learning platform)
**What works:** AI-generated baseline content that instructors edit, template cloning for scale

### 5. [5 tips for structuring your cohort-based course - Teachable](https://teachable.com/blog/structuring-cohort-based-courses)
**Relevance:** medium
**Key ideas:**
- Start with basics so everyone starts on same page
- Create syllabus for expectations and timeline tracking
- Incorporate feedback from initial runs to improve content
**Who:** Teachable (course platform)
**What works:** Iterative improvement based on student feedback, structured syllabi for consistency

### 6. [12 predictions for tech comm in 2026](https://idratherbewriting.com/blog/tech-comm-predictions-for-2026)
**Relevance:** high
**Key ideas:**
- AI productivity boost stabilizes at ~1.5x factor (validation overhead limits velocity)
- Shift from beautiful docs sites to AI-powered conversational interfaces
- NotebookLM as RAG backend for documentation chatbots
**Who:** Tom Johnson (I'd Rather Be Writing blog)
**What works:** Realistic AI expectations (1.5x not 10x), conversational AI on docs sites, RAG for accuracy

### 7. [Top 7 AI Tools for Technical Writing in 2026](https://document360.com/blog/ai-tools-for-technical-writing/)
**Relevance:** medium
**Key ideas:**
- Modern workflow uses stack of specialized tools, not single tool like ChatGPT
- Focus on deep product integration over generic chatbots
- Tools span content generation, editing, research, visualization, SEO, plagiarism checking
**Who:** Document360 (documentation platform)
**What works:** Specialized tool stacks for different phases, deep product integration

### 8. [Best Technical Writing Tools & Software in 2026](https://ferndesk.com/blog/best-technical-writing-tools)
**Relevance:** high
**Key ideas:**
- AI Documentation Agents continuously monitor codebases, support tickets, changelogs
- Proactively identify gaps by analyzing customer questions
- Generate drafts for human review, not auto-publish
**Who:** Ferndesk (technical writing tools)
**What works:** Continuous monitoring for documentation gaps, human-in-loop for quality, multi-source analysis

### 9. [Top AI Writing Tools in 2026: Best AI for Writing](https://www.empler.ai/blog/top-ai-writing-tools-in-2026-best-ai-for-writing)
**Relevance:** high
**Key ideas:**
- Shift to agentic AI platforms managing entire content lifecycles
- Agent teams handle research, strategy/briefing, writing, optimization steps
- Multi-step processes automated via specialized agents
**Who:** Empler AI (agentic platform)
**What works:** Agent teams for different workflow stages, end-to-end lifecycle automation

### 10. [AI Editor Writing Guide (2025): Draft, Rewrite, and Polish Like a Pro](https://skywork.ai/blog/how-to-ai-editor-writing-guide-2025/)
**Relevance:** high
**Key ideas:**
- Three-stage workflow: Draft Fast (outline-first, section-by-section), Rewrite for Clarity (substantive edit rubric), Polish (line edits)
- Quality gates before proceeding (checking reader questions, required facts, tone match)
- Critique-revise loops for structure, evidence, flow
**Who:** Skywork AI
**What works:** Structured three-stage process with quality gates, rubric-based evaluation, iterative improvement

### 11. [My AI Writing Process: How I Use Different Tools at Each Stage](https://bronwynnepowell.com/ai-writing-process/)
**Relevance:** high
**Key ideas:**
- Six-stage workflow: Brainstorm (ChatGPT), Outline (human-only), Research (Perplexity/ChatGPT with manual verification), Draft (human writes), Edit (human-led with Grammarly), Optimize (AI for formatting/SEO)
- Human control at critical stages (outline, draft, edit)
- AI for ideation and optimization, not core content
**Who:** Bronwynne Powell (individual creator)
**What works:** Human-led at critical stages, AI as assistant not replacement, manual source verification

### 12. [From panic to power: How AI is changing my Technical Writing workflow](https://medium.com/softserve-technical-communication/from-panic-to-power-how-ai-is-changing-my-technical-writing-workflow-f726250a6fa1)
**Relevance:** high
**Key ideas:**
- AI moved from experiments (early 2023) to trusted partner (mid-2025) for drafting, compliance review, planning, multimedia
- Mastering prompt engineering crucial (Zero-shot, Few-shot, Chain-of-thought, Reverse prompting)
- Toolbox expansion beyond single LLM to specialized tools
**Who:** SoftServe Technical Communication
**What works:** Prompt engineering mastery, multiple specialized tools, AI for drafting and compliance

### 13. [Workflow: From Raw Notes to Publication with an AI Writing Editor](https://skywork.ai/blog/how-to-turn-raw-notes-into-publishable-article-ai-writing-editor-guide/)
**Relevance:** high
**Key ideas:**
- 8-phase workflow: Tidy notes (30-60min), Draft fast (45-90min), Structural edit (30-60min), Line edit (20-40min), Format/style (10-20min), Fact-check (20-40min), SEO optimize (15-30min), Final review (10-15min)
- Section-by-section drafting grounded with provided sources
- Insert first-hand experience to differentiate from pure AI content
**Who:** Skywork AI
**What works:** Time-boxed phases for predictability, source grounding, human experience integration

### 14. [The Year AI Changed Technical Writing: Key Lessons & What's Next](https://www.linkedin.com/pulse/year-ai-changed-technical-writing-key-lessons-whats-next-bw6vc)
**Relevance:** high
**Key ideas:**
- 2025 adoption: style guide compliance, terminology consistency, grammar, alt-text, SEO metadata
- Editors prefer human-in-the-loop for reviewing AI content
- Re-engineered processes with AI as core capability, not just prompt engineering
**Who:** Technical writing community (LinkedIn)
**What works:** Human-in-the-loop reviews, process re-engineering with AI at core, validation against hallucinations

### 15. [How I Built an AI Content Workflow System to Automate My Creative Process](https://medium.com/@elosarah85/how-i-built-an-ai-content-workflow-system-to-automate-my-creative-process-fffaad970ae0)
**Relevance:** high
**Key ideas:**
- Six specialized agents: Research (Tavily API), Writer (uses past samples), Evaluator (quality control scoring), Editor (refinement), Optimizer (SEO/formatting), Scheduler (multi-platform)
- Evaluator scores on Authenticity, Quality, Completeness, Depth (must score 7.0+)
- Agent-based pipeline with quality gates
**Who:** Elo Sarah (indie creator)
**What works:** Specialized agents for each stage, quality scoring system, multi-platform scheduling

### 16. [CreatorOS - CORE System](https://coresystem.io/creatoros/)
**Relevance:** medium
**Key ideas:**
- Notion-based system for managing blog, video, podcast, newsletter production
- Content channel dashboards, templates, checklists, ideation/validation systems
- Super-charged with Core AI for workflow scaling
**Who:** CORE System (Notion template)
**What works:** Centralized management in Notion, dedicated templates per channel, AI workflows integration

### 17. [What is content automation, and how to build your first workflow](https://podcastle.ai/blog/content-automation-workflow/)
**Relevance:** medium
**Key ideas:**
- Content automation for planning, creation, repurposing, publishing, updates
- Focus on offloading repetitive tasks so creators focus on strategy
- Common workflows: long-form to social posts, transcripts to blog posts
**Who:** Podcastle (content automation)
**What works:** Repurposing workflows (long-form to short-form), automation of repetitive tasks, creator focus on strategy

### 18. [Automate WordPress Publishing with n8n and OpenAI](https://vicky.dev/automate-wordpress-publishing-with-n8n/)
**Relevance:** high
**Key ideas:**
- Fully automated system: fetch content (GNews API), check duplicates (Google Sheets), generate article (GPT-4o-mini), publish (WordPress REST API)
- Scales to 720+ articles monthly, transforming 20-30 hour weekly task to monitoring
- Every 2 minutes cycle with tracking to prevent duplicates
**Who:** Vicky.dev (indie developer)
**What works:** High-frequency automated publishing, duplicate prevention, API-driven workflow, massive scale (720+ articles/month)

### 19. [How Notion develops world-class AI features](https://braintrust.dev/blog/notion)
**Relevance:** high
**Key ideas:**
- Old workflow: JSONL files in git, expensive human evaluation
- New workflow with Braintrust: curate targeted datasets, tie to scoring functions (heuristic, LLM-as-judge, human), run experiments, review changes, merge
- Version datasets from real-world usage and hand-written examples
**Who:** Notion
**What works:** Dataset versioning, multiple scoring methods (heuristic/LLM/human), experiment-driven development

### 20. [Vercel Workflow Development Kit](https://vercel.com/docs/workflow)
**Relevance:** medium
**Key ideas:**
- Workflow platform for building apps and agents that pause, resume, maintain state
- Workflows are stateful functions coordinating multi-step logic over time
- Steps are durable units surviving failures, Hooks wait for external events
**Who:** Vercel
**What works:** Stateful workflows with pause/resume, durable steps, event-driven architecture

### 21. [Workflow Builder: Build your own workflow automation platform](https://vercel.com/blog/workflow-builder-build-your-own-workflow-automation-platform)
**Relevance:** high
**Key ideas:**
- Open-source template with visual editor, execution engine, infrastructure
- AI-powered text-to-workflow generation (natural language to executable workflows)
- Agentic workflows for multi-step, cross-system processes
**Who:** Vercel
**What works:** Natural language workflow creation, visual editor for non-technical users, open-source foundation

### 22. [BARTScore: Evaluating Generated Text as Text Generation](https://papers.nips.cc/paper/2021/hash/e4d2b6e6fdeca3e60e0f1a62fee3d9dd-Abstract.html)
**Relevance:** medium
**Key ideas:**
- Evaluation metric using pre-trained sequence-to-sequence models like BART
- Flexibly evaluates informativeness, fluency, factuality perspectives
- Outperforms existing metrics in many test settings
**Who:** Academic research (NeurIPS 2021)
**What works:** Multi-perspective evaluation (informativeness/fluency/factuality), pre-trained model leverage

### 23. [A list of metrics for evaluating LLM-generated content - Microsoft](https://learn.microsoft.com/en-us/ai/playbook/technology-guidance/generative-ai/working-with-llms/evaluation/list-of-eval-metrics)
**Relevance:** high
**Key ideas:**
- Reference-based metrics: BLEU, ROUGE, METEOR, BERTScore (compare to ground truth)
- Reference-free metrics: evaluate based on context/source without ground truth
- Multiple metric types for different evaluation needs
**Who:** Microsoft
**What works:** Comprehensive metric taxonomy, reference-based and reference-free options, clear categorization

### 24. [Evaluating AI-Generated Content - Walturn](https://www.walturn.com/insights/evaluating-ai-generated-content)
**Relevance:** medium
**Key ideas:**
- Traditional metrics (BLEU, ROUGE, METEOR) rely on n-gram overlap
- Semantic similarity metrics (BERTScore, GPTScore) use transformer models
- Perplexity quantifies language model prediction quality
**Who:** Walturn
**What works:** Combination of traditional and semantic metrics, perplexity for fluency measurement

### 25. [Evaluating LLM Content Quality with Automated Metrics - HashMeta](https://www.hashmeta.ai/blog/evaluating-llm-content-quality-with-automated-metrics-a-comprehensive-guide)
**Relevance:** high
**Key ideas:**
- Perplexity/entropy for text predictability and fluency
- BLEU/ROUGE for reference comparison
- BERTScore for semantic meaning beyond word matches
- Factuality and hallucination detection tools
**Who:** HashMeta AI
**What works:** Multi-metric approach (fluency + reference + semantic + factuality), hallucination detection integration

### 26. [The AI Writing Tools Actually Ranking Pages in 2026](https://medium.com/@SophiaQuantum/the-ai-writing-tools-actually-ranking-pages-in-2026-cfeb1e087e60)
**Relevance:** high
**Key ideas:**
- Winning content: precise search intent matching, deep coverage without fluff, understandable structure, rapid updating
- Strong trust signals: original insights, citations, real examples, clear authorship
- Natural language avoiding generic AI phrasing
**Who:** Sophia Quantum (SEO analyst)
**What works:** Search intent precision, trust signals (citations/examples), natural language, rapid iteration

### 27. [Content Performance Metrics That Matter - Acrolinx](https://www.acrolinx.com/blog/most-relevant-content-performance-metrics/)
**Relevance:** high
**Key ideas:**
- Essential metrics: efficiency gains (time saved), consistency (brand voice alignment), compliance (regulatory requirements)
- Audience engagement comparison (AI vs human content performance)
- Content accuracy verification due to hallucination risks
**Who:** Acrolinx (content quality platform)
**What works:** Efficiency + consistency + compliance metrics, AI vs human performance comparison, accuracy verification

### 28. [Evaluating the quality of generative AI output - Clarivate](https://clarivate.com/academia-government/blog/evaluating-the-quality-of-generative-ai-output-methods-metrics-and-best-practices/)
**Relevance:** high
**Key ideas:**
- Key dimensions: Relevance (addresses query), Accuracy/Faithfulness (supported by sources), Clarity/Structure (readable and logical), Bias detection
- Focus on multi-dimensional quality assessment
- Academic workflow context with emphasis on source fidelity
**Who:** Clarivate (academic/research)
**What works:** Multi-dimensional framework (relevance/accuracy/clarity/bias), source-grounded evaluation

### 29. [AI Content Score: The New Standard - Conductor](https://www.conductor.com/blog/ai-content-score-release/)
**Relevance:** high
**Key ideas:**
- Two core pillars: Comprehensive Topical Coverage and Precise Intent Alignment
- Score 0-100 broken into actionable components
- Focus on depth, authority, satisfying user intent (what search engines and LLMs value)
**Who:** Conductor (SEO platform)
**What works:** Intent alignment scoring, topical coverage depth, actionable component breakdown

### 30. [Human-Aligned Long-Form Evaluation (HALF-Eval) - Amazon Science](https://assets.amazon.science/4a/de/85b797d4482a80bcbc9d6151167a/human-aligned-long-form-evaluation-half-eval-framework-for-assessing-ai-generated-content-and-improvement.pdf)
**Relevance:** high
**Key ideas:**
- Two-stage: Checklist Evaluation (creativity, interest, coherence, relevance) then ML Aggregation
- Checklists initially by humans (training), later by LLM-as-Judge
- Regression models synthesize scores into holistic quality rating (1-10) and binary classification
**Who:** Amazon Science
**What works:** Structured checklists for key dimensions, human-LLM hybrid evaluation, holistic score synthesis

## Summary

### Top 5 Insights

1. **AI productivity boost has stabilized at ~1.5x, not 10x** - Companies have moved past initial hype to realistic expectations. Validation overhead and manual review requirements limit velocity gains, but 1.5x improvement is sustainable and meaningful.

2. **Shift from monolithic LLMs to specialized agent systems** - Most successful implementations use multiple specialized agents (research, writing, evaluation, optimization) rather than single general-purpose models. Each agent has specific responsibilities and quality gates.

3. **Human-in-the-loop remains critical for quality** - All production systems maintain human control at critical stages: outline creation, content verification, final approval. AI generates drafts and handles optimization, humans ensure accuracy and authenticity.

4. **Multi-dimensional evaluation frameworks replace single metrics** - Companies use combinations of automated metrics (BLEU/ROUGE/BERTScore for technical quality), LLM-as-judge (for relevance/coherence), and human review (for authenticity/trust). No single metric captures full quality.

5. **Documentation automation tied to code changes works in production** - Anthropic and others successfully automate documentation updates by monitoring code diffs, analyzing changes, and generating/updating docs automatically with human review checkpoints.

### Company Patterns

**Anthropic:**
- Context files (`claude.files`) provide persistent guidelines across sessions
- Dual workflow: PR-triggered updates + scheduled maintenance
- Plan Mode for safe exploration before edits
- Permission-based tool control for safety

**Notion:**
- Moved from manual JSONL + expensive human eval to versioned datasets with Braintrust
- Three evaluation methods: heuristic rules, LLM-as-judge, human review
- Experiment-driven development with dataset versioning from real usage

**Vercel:**
- Stateful workflows with pause/resume capabilities
- Text-to-workflow generation (natural language to executable)
- Visual editor for non-technical team members
- Durable steps that survive failures

**Microsoft:**
- Comprehensive metric taxonomy: reference-based (BLEU/ROUGE/METEOR) + reference-free
- Multi-metric evaluation approach for different quality aspects
- Clear categorization of evaluation methods

**Amazon:**
- Two-stage HALF-Eval: structured checklists → ML aggregation
- Dimensions: creativity, interest, coherence, relevance
- Human training data → LLM-as-judge automation
- Holistic scoring (1-10) + binary classification

**Conductor (SEO):**
- AI Content Score focuses on topical coverage depth + intent alignment
- 0-100 score with actionable component breakdown
- Optimizes for both search engines and LLMs (dual visibility)

### Creator Patterns

**Solo Creators (Elo Sarah, Vicky.dev, Bronwynne Powell):**
- Six-agent pipeline: Research → Writer → Evaluator → Editor → Optimizer → Scheduler
- Quality scoring gates (minimum 7.0/10 on authenticity/quality/completeness/depth)
- High-frequency automation (720+ articles/month possible)
- API-driven workflows (GNews → GPT-4o-mini → WordPress)
- Human writes core content, AI handles ideation and optimization

**Content Creators (Podcastle, CreatorOS):**
- Focus on repurposing workflows (long-form → social posts)
- Notion-based centralized management systems
- Template-driven production per channel (blog/video/podcast)
- Automation of repetitive tasks, creator focus on strategy

**Technical Writers (SoftServe, Skywork):**
- Three-stage workflow: Draft Fast → Rewrite for Clarity → Polish
- Time-boxed phases (30-90min per stage) for predictability
- Prompt engineering mastery (Zero-shot, Few-shot, Chain-of-thought)
- Source grounding + first-hand experience for authenticity

### Quality Metrics

**Technical Quality (Automated):**
- BLEU/ROUGE/METEOR: n-gram overlap with references
- BERTScore/GPTScore: semantic similarity via embeddings
- Perplexity: text predictability and fluency
- ContrastScore: multi-perspective evaluation (2025 research)

**Content Quality (Multi-dimensional):**
- Relevance: addresses search query/user intent
- Accuracy/Faithfulness: supported by sources, no hallucinations
- Clarity/Structure: readable, logical organization
- Bias detection: inappropriate or exclusionary content

**Production Quality (Business Metrics):**
- Efficiency gains: time saved in creation/editing/approvals
- Consistency: brand voice and terminology alignment
- Compliance: regulatory requirements met
- Audience engagement: time on page, bounce rates (AI vs human)

**SEO/Visibility (2026 Focus):**
- Topical coverage depth (not just keyword matching)
- Intent alignment precision (buying/learning/comparing)
- Trust signals: citations, real examples, clear authorship
- Natural language (avoiding generic AI phrasing)
- LLM citation rates (visibility in AI responses)

**Holistic Scoring (Amazon HALF-Eval):**
- Creativity, interest, coherence, relevance checklists
- 1-10 holistic quality rating
- Binary high/low quality classification
- Human-aligned judgment via trained models

### Applicable to Projects

**For HSL Course Content:**
- Implement three-stage workflow: Draft Fast (outline + sections) → Rewrite (substantive edit) → Polish (line edits)
- Use quality gates between stages: check for reader questions answered, required facts included, tone match
- Time-box each phase for predictability (60min draft, 30min edit, 20min polish)
- Insert first-hand coding experience to differentiate from pure AI content
- Track efficiency metrics: time per lesson, consistency with course voice

**For Blog Articles:**
- Adopt six-agent pipeline: Research (gather sources) → Writer (draft) → Evaluator (score quality) → Editor (refine) → Optimizer (SEO) → Publisher
- Implement scoring system: minimum 7.0/10 on authenticity, technical accuracy, completeness, depth before publishing
- Use multi-dimensional evaluation: BLEU for technical quality, LLM-as-judge for coherence, human review for authenticity
- Add trust signals: code examples, citations, project screenshots, clear authorship
- Track SEO metrics: topical coverage depth, intent alignment, natural language score

**For Documentation:**
- Set up PR-triggered doc updates (analyze code diff → update relevant docs)
- Add scheduled maintenance workflow (daily review of changes → consolidated updates)
- Use context files for persistent guidelines (terminology, style, repository conventions)
- Implement permission-based tool control for safety
- Track consistency metrics: brand voice alignment, terminology compliance

**For Content Repurposing:**
- Build automation: stream recording → transcript → blog post → social snippets
- Use Notion as centralized content hub with channel-specific templates
- Create repurposing workflows: 90min video → 10min article → 5x Twitter threads
- Track efficiency: hours saved per repurposed piece

**General System Design:**
- Prefer specialized agents over single general model
- Maintain human-in-the-loop at critical stages (outline, verification, approval)
- Use multiple evaluation methods: automated + LLM-judge + human
- Version datasets and track real-world usage for improvement
- Focus on 1.5x realistic gains, not 10x hype
