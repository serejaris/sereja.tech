# Block 1: LLM Writing Pipelines

## Sources

### 1. [Chain complex prompts for stronger performance - Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts)
**Relevance:** high
**Key ideas:**
- Prompt chaining breaks complex tasks into sequential subtasks (Research → Outline → Draft → Edit → Format)
- Each subtask gets Claude's full attention, improving accuracy and clarity vs single-prompt approach
- Enables iterative content creation pipelines with better traceability
**Connection to skills:** Directly applicable to blog-post workflow which uses multi-step generation (research → outline → draft → deaify → publish)

### 2. [Building Generative AI prompt chaining workflows with human in the loop - AWS](https://aws.amazon.com/blogs/machine-learning/building-generative-ai-prompt-chaining-workflows-with-human-in-the-loop)
**Relevance:** high
**Key ideas:**
- Prompt chaining speeds up process through parallelization and model specialization
- Better output through focused prompts with more relevant context
- Less development time through easier iterative refinement of smaller prompts
**Connection to skills:** Validates approach in deaify and atom-generation where specialized prompts handle distinct phases (detection → rewrite → verification)

### 3. [LLM Chaining - Techniques and Best Practices - Mirascope](https://mirascope.com/blog/llm-chaining)
**Relevance:** high
**Key ideas:**
- Sequential chains for progressive processing (chunk-by-chunk summarization)
- Parallel chains for simultaneous execution (sentiment analysis + classification)
- Conditional chains with if-else logic for dynamic routing
**Connection to skills:** Parallel chains relevant for future optimization of blog-post (research + outline generation in parallel); conditional chains for quality gates

### 4. [Prompt Chaining - Vellum Workflows SDK](https://docs.vellum.ai/developers/workflows-sdk/tutorials/prompt-chaining)
**Relevance:** medium
**Key ideas:**
- Blog generation chain: TopicResearch → OutlineCreation → ContentGeneration → FinalOutput
- Each node has specialized role with rated outputs feeding into next stage
- SDK approach allows programmatic workflow construction
**Connection to skills:** Mirrors blog-post skill architecture; rating mechanism could improve atom selection quality

### 5. [The Architecture of Intelligence: Multi-Agent LLMs - Medium](https://medium.com/@gafowler/the-architecture-of-intelligence-how-multi-agent-llms-collaborate-to-write-evaluate-and-refine-3fa1ffda7680)
**Relevance:** high
**Key ideas:**
- Specialized agent roles: Planner, Prompt Engineer, Executor, Critic, Optimizer, Memory
- Critic Agent evaluates outputs and flags issues before proceeding
- Memory Agent maintains context and stores reusable instructions
**Connection to skills:** Critic agent concept directly applicable to deaify skill (detect AI patterns → provide feedback → rewrite). Memory agent relevant for atom-generation reusability

### 6. [How we built our multi-agent research system - Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
**Relevance:** high
**Key ideas:**
- Orchestrator-worker pattern with lead agent coordinating parallel subagents
- Iterative research loop: lead agent synthesizes results, decides if more research needed
- Dynamic spawning of specialized subagents based on evolving needs
**Connection to skills:** Research phase in blog-post could use parallel subagents for different aspects (technical docs, examples, best practices)

### 7. [Multi-Agent System Patterns - Medium](https://medium.com/@mjgmario/multi-agent-system-patterns-a-unified-guide-to-designing-agentic-architectures-04bb31ab9c41)
**Relevance:** high
**Key ideas:**
- Four key dimensions: Control (centralized vs decentralized), Execution (sequential vs parallel), Coordination (agents as tools vs graph-based), Interaction (communication protocols)
- Patterns are composable and can be mixed
- Hybrid orchestration balances control and autonomy
**Connection to skills:** Current skills use centralized sequential pattern; could evolve to hybrid with parallel execution for independent subtasks

### 8. [Multi-Agent Reference Architecture - Microsoft](https://microsoft.github.io/multi-agent-reference-architecture/docs/reference-architecture/Reference-Architecture.html)
**Relevance:** medium
**Key ideas:**
- Orchestrator (Semantic Kernel) manages request flow and delegates to specialized agents
- Classifier routes requests to appropriate agent using tiered approach (NLU → SLM → LLM)
- Agent Registry manages discovery and lifecycle
**Connection to skills:** Classifier pattern could route content types (blog vs lesson vs documentation) to specialized generation agents

### 9. [Prompt Chaining vs. Chain of Thought - AirOps](https://www.airops.com/blog/prompt-chaining-vs-chain-of-thought)
**Relevance:** high
**Key ideas:**
- Prompt chaining: multiple prompts for multi-stage tasks (drafting → critiquing → fact-checking)
- Chain of thought: step-by-step reasoning within single prompt
- Use prompt chaining when iterative refinement is essential
**Connection to skills:** Confirms deaify should use prompt chaining (detect → rewrite) rather than CoT; blog-post benefits from chaining over monolithic prompt

### 10. [Self-Refine: Iterative Refinement with Self-Feedback - arXiv](https://arxiv.org/abs/2303.17651)
**Relevance:** high
**Key ideas:**
- Three-step iterative loop: Generate → Feedback → Refine (repeats until satisfactory)
- Same LLM provides feedback on its own output, no supervised data needed
- Improves task performance by ~20% on average vs one-shot generation
**Connection to skills:** Core technique for deaify skill (initial draft → detect AI patterns → rewrite based on feedback); could add explicit iteration limit

### 11. [Automated Content Quality Checking - Acrolinx](https://www.acrolinx.com/wp-content/uploads/2024/07/acrolinx-automated-content-quality-checking-brochure.pdf)
**Relevance:** medium
**Key ideas:**
- Quality gates block publication until content meets writing standards
- Integrates into generative AI process to check content as generated
- Can regenerate content if it doesn't meet standards
**Connection to skills:** Quality gates concept applicable to blog-post final validation; could add automated checks before publishing

### 12. [Evaluating LLM Content Quality with Automated Metrics - HashMeta](https://www.hashmeta.ai/blog/evaluating-llm-content-quality-with-automated-metrics-a-comprehensive-guide)
**Relevance:** high
**Key ideas:**
- Automated metrics: Perplexity, BLEU/ROUGE, BERTScore, Hallucination Detection
- Three-phase evaluation: pre-generation (input validation), real-time (during generation), post-generation (final checks)
- Balance automation with human-in-the-loop oversight
**Connection to skills:** Post-generation metrics could validate deaify output quality; hallucination detection critical for fact-heavy blog content

### 13. [Long context prompting tips - Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips)
**Relevance:** high
**Key ideas:**
- Place long documents (20K+ tokens) at beginning of prompt before query/instructions
- Structure multiple documents with XML tags for clarity
- Ground responses in quotes from source documents before analysis
**Connection to skills:** html-lesson skill works with long transcripts/sessions; placing full session at top before instruction improves recall

### 14. [Prompt engineering for Claude's long context window - Anthropic](https://www.anthropic.com/news/prompting-long-context)
**Relevance:** high
**Key ideas:**
- Extract reference quotes into scratchpad before answering improves accuracy
- Contextual examples (related to document) outperform generic examples
- More examples improve performance for long-context Q&A
**Connection to skills:** blog-post research phase could use scratchpad for quote extraction; contextual examples in prompts improve output relevance

### 15. [Self-Refine Prompting - Learn Prompting](https://learnprompting.org/docs/advanced/self_criticism/self_refine)
**Relevance:** high
**Key ideas:**
- Iterative improvement workflow: Initial output → Feedback → Refinement (repeat)
- Inspired by human writing process of iterative draft refinement
- Simple three-step process applicable to any content generation task
**Connection to skills:** Exact pattern used in deaify (generate → critique for AI patterns → refine); formalizes the human-like revision process

### 16. [Iterative Refinement Chains - RunPod](https://www.runpod.io/blog/iterative-refinement-chains-with-small-language-models)
**Relevance:** medium
**Key ideas:**
- Breaks "cognitive overload" of monolithic prompts into compartmentalized calls
- ProsePolisher pattern: Architect (blueprint) → Creative Consultants (injection) → Editor (refinement)
- Validated by Self-Refine framework (Generator → Critic → Refiner)
**Connection to skills:** Validates breaking blog-post into specialized roles; prevents single-prompt cognitive overload in complex content tasks

### 17. [How to Build a Self-Refining Content Agent - LarAgent](https://blog.laragent.ai/how-to-build-a-self-refining-content-agent-with-laragent/)
**Relevance:** high
**Key ideas:**
- Supervising pattern: Writer agent drafts, Reviewer agent evaluates with structured scores
- Loop continues until quality threshold (85/100) or max iterations
- Reviewer provides specific, actionable feedback using structured output
**Connection to skills:** Could enhance deaify with scoring mechanism (AI-ness score) and iteration limit; structured feedback improves rewrite quality

### 18. [AI Review Article Writer Section Workflow - reckoning.dev](https://reckoning.dev/posts/ai-review-writer-05-section-writing)
**Relevance:** medium
**Key ideas:**
- Expert writing workflow: drafting → reviewing → refinement (non-linear)
- Quality review loop evaluates against academic standards
- Section integration combines subsections with LLM-generated connective content
**Connection to skills:** Blog-post could adopt section-by-section generation with integration phase; quality review loop ensures coherence before moving to next section

## Summary

### Top 5 Insights

1. **Prompt chaining outperforms monolithic prompts** - Breaking complex writing tasks into sequential specialized prompts (research → outline → draft → edit) gives each phase full LLM attention, improving accuracy by 20%+ and making refinement easier

2. **Self-refine loop is fundamental to quality** - The pattern of Generate → Feedback → Refine (iterating until quality threshold) mirrors human writing and consistently improves output. This is the core of effective AI writing workflows

3. **Multi-agent architectures enable specialization** - Dedicated agents for planning, execution, criticism, and memory create better outputs than single-agent systems. Critic agents are especially valuable for quality gates

4. **Parallel execution reduces latency** - Independent subtasks (like multiple research angles) can run simultaneously. Orchestrator-worker pattern allows dynamic spawning of specialized subagents

5. **Long-context tips are critical for document-heavy tasks** - Placing long content at prompt beginning, using XML structure, and grounding responses in extracted quotes dramatically improves recall and accuracy

### Recurring Patterns

- **Separation of concerns** - Best workflows isolate generation, evaluation, and refinement into distinct steps rather than trying to do everything in one prompt
- **Iterative loops with exit conditions** - Quality thresholds (scores) or max iteration limits prevent infinite refinement while ensuring minimum quality
- **Structured output for feedback** - Reviewers/critics provide actionable feedback in structured formats (JSON, XML) rather than free-form text
- **Context management is critical** - Memory agents, scratchpads, and XML-tagged documents prevent context loss in multi-step workflows
- **Hybrid control** - Most effective systems balance centralized orchestration with decentralized agent autonomy

### Applicable to Projects

**deaify skill:**
- Add explicit quality scoring (AI-ness percentage) with threshold exit condition
- Implement structured feedback format for detected patterns
- Consider max iteration limit (3-5 rounds) to prevent excessive refinement cost

**blog-post skill:**
- Enhance research phase with parallel subagents for different content angles
- Add quality review loop between draft and final output with scoring
- Implement scratchpad technique for quote extraction from research sources
- Consider section-by-section generation with integration phase for longer articles

**html-lesson skill:**
- Apply long-context tips (place full transcript at beginning, XML structure)
- Use quote-grounding technique: extract relevant transcript sections before generating lesson content
- Add contextual examples specific to the transcript domain

**General improvements:**
- Implement orchestrator pattern to route content types to specialized generation agents
- Build reusable critic agent that works across different content types
- Add automated quality metrics (hallucination detection, coherence scoring) as final gate
- Create memory system for reusable instructions and patterns across skills
