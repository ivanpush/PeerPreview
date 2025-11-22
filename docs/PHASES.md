# Development Phases

## Phase 0: Foundation (Day 1) ✅
- [x] Initialize monorepo structure
- [x] Set up Docker Compose
- [x] Create Pydantic data models
- [x] Implement PDF parser with pymupdf4llm
- [x] Build section splitter
- [x] Create FastAPI endpoints
- [x] Build upload UI with Next.js

## Phase 1: Core Agents (Days 2-3)
- [ ] **LLM Service Layer**
  - [ ] Multi-provider abstraction (Claude, OpenAI, Groq)
  - [ ] Fallback chain implementation
  - [ ] Cost tracking
- [ ] **Base Agent Architecture**
  - [ ] BaseAgent abstract class
  - [ ] AgentContext with indices
  - [ ] Parallel execution with asyncio.gather
- [ ] **Priority Agents**
  - [ ] MethodsReviewer (IRB, sample size, stats)
  - [ ] ResultsReviewer (figures, N consistency)

## Phase 2: Specialized Agents (Days 4-5)
- [ ] **CrossDocConsistency**
  - [ ] Use pre-computed indices
  - [ ] Find N contradictions
- [ ] **CitationPolice**
  - [ ] Mock Semantic Scholar responses
  - [ ] Lazy/imprecise detection logic
- [ ] **FigureAgent**
  - [ ] Dangling/orphaned detection
  - [ ] Caption-text consistency
- [ ] **Demo Fixtures**
  - [ ] Create demo paper with known issues
  - [ ] Pre-compute responses for DEMO_MODE

## Phase 3: Complete Pipeline (Days 6-7)
- [ ] **Remaining Reviewers**
  - [ ] AbstractReviewer
  - [ ] IntroductionReviewer
  - [ ] DiscussionReviewer
- [ ] **Result Aggregation**
  - [ ] ReviewOrchestrator
  - [ ] Issue deduplication
  - [ ] Grouped output (4 buckets)
- [ ] **Frontend Results**
  - [ ] Quote-based highlighting
  - [ ] Filter toggles
  - [ ] Progress tracking

## Phase 4: Polish & Demo (Days 8-10)
- [ ] **UI Polish**
  - [ ] Landing page
  - [ ] Real-time agent status
  - [ ] Issue cards by severity
- [ ] **Export**
  - [ ] Markdown report
  - [ ] JSON export
- [ ] **Testing**
  - [ ] End-to-end tests
  - [ ] Performance optimization
- [ ] **Demo Prep**
  - [ ] Demo script
  - [ ] Backup video

## Phase 5: Advanced Features (Days 11-14)
- [ ] **Track B Suggestions**
  - [ ] Style improvements
  - [ ] Flow suggestions
- [ ] **Real Semantic Scholar**
  - [ ] API integration
  - [ ] DOI extraction
- [ ] **Figure Vision** (Optional)
  - [ ] GPT-4V integration
  - [ ] Caption-image verification

## Success Metrics
- [ ] All 8 agents working
- [ ] <90 second processing
- [ ] Track A precision >90%
- [ ] Demo without errors