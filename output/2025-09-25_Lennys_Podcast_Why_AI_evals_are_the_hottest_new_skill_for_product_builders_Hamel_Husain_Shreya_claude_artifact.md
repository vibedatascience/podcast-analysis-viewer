**Guest:** Hamel Husain & Shreya Shankar (AI researchers and educators who teach the definitive online course on evals, having trained over 2,000 PMs and engineers across 500 companies including teams from OpenAI and Anthropic)

**Key Quote:**
***"To build great AI products, you need to be really good at building evals. It's the highest ROI activity you can engage in."***

**Contents Covered:**
1. What evals are and why they're becoming essential for AI product builders
2. The systematic process of error analysis for AI applications
3. Open coding and axial coding techniques for categorizing errors
4. Building and validating LLM-as-judge evaluators
5. Common misconceptions and debates around evals
6. The relationship between evals, A/B testing, and product requirements
7. Practical tips for implementing evals in production systems
8. Cost-benefit analysis of different evaluation approaches

**Detailed Analysis:**

## 1. Understanding Evals: The New Essential Skill

***"Evals is a way to systematically measure and improve an AI application. It really is at its core data analytics on your LLM application in a systematic way of looking at that data."***

Evals represent a fundamental shift in how product teams approach AI quality assurance. Unlike traditional software testing, evals encompass a broad spectrum of measurement techniques designed specifically for stochastic AI systems. The concept extends far beyond simple unit tests to include comprehensive data analysis, online monitoring, and systematic error tracking. This approach becomes critical because AI applications operate with much larger surface areas and inherent unpredictability compared to deterministic software systems.

The rise of evals as a critical skill marks a rare emergence of an entirely new competency requirement for product builders. Two years ago, the term was virtually unknown outside specialized AI research circles. Now, major AI labs report it as their most important skill for product development. The chief product officers of both Anthropic and OpenAI have publicly stated that evals are becoming the most crucial new capability for their teams. This rapid adoption reflects the unique challenges of building reliable AI products where traditional testing methods fall short.

## 2. The Error Analysis Framework

***"Looking at data is the most powerful activity that you can engage in. It's the highest ROI activity... Everyone that does this immediately gets addicted to it."***

The foundation of effective evals begins with **error analysis** - a structured approach to understanding how and why AI applications fail. This process starts with examining individual traces (detailed logs of AI interactions) and writing informal notes about observed problems. The methodology draws from established machine learning practices that have existed for decades, as evidenced by Andrew Ng's teachings from over eight years ago.

The process involves several key stages. First, practitioners examine at least 100 traces manually, writing "open codes" - informal notes about the first error observed in each interaction. These notes should be detailed enough for later categorization but don't need to follow any rigid format. The goal is to achieve **theoretical saturation** - the point where new error types stop emerging, typically occurring after reviewing 40-100 traces depending on application complexity.

After collecting open codes, practitioners use LLMs to synthesize them into "axial codes" - categorical labels representing distinct failure modes. This synthesis step transforms messy, informal observations into actionable categories like "human handoff issues," "formatting errors," or "conversational flow problems." The power of this approach lies in its simplicity: basic counting of categorized errors reveals the most prevalent issues, providing clear priorities for improvement efforts.

## 3. The Benevolent Dictator Principle

***"You can appoint one person whose taste that you trust... You don't want to make this process so expensive that you can't do it."***

One of the most practical insights for implementing evals is the **benevolent dictator** concept. Rather than creating committees or seeking consensus for every evaluation decision, organizations should designate a single domain expert to make judgment calls during the error analysis phase. This person should possess deep domain expertise - a legal expert for law applications, a medical professional for healthcare products, or often the product manager for general applications.

This approach dramatically reduces the overhead and complexity of the evaluation process. Many teams become paralyzed trying to achieve perfect consensus on every error classification, making the process so expensive and time-consuming that it becomes impractical. The benevolent dictator model recognizes that **perfect agreement isn't necessary for actionable insights**. The goal is progress and improvement, not perfection. This person's decisions guide the initial error categorization, which can be refined over time as patterns become clearer.

## 4. Building LLM-as-Judge Evaluators

***"The beautiful thing about LLM judge is you can use them in unit tests... but you could also use it online for monitoring. You can sample thousand traces every day, run your LLM judge on real production traces and see what the failure rate is."***

LLM-as-judge represents a sophisticated approach to automated evaluation where an AI model evaluates the outputs of another AI system. These judges are designed to evaluate **single, specific failure modes** with binary pass/fail outputs, making them far more reliable than attempting broad quality assessments. The narrow scope ensures that the judge's task remains tractable and accurate.

Creating an effective LLM judge requires careful validation against human judgment. Practitioners must create a confusion matrix comparing the judge's assessments with human evaluations, paying special attention to false positives and false negatives. **Simple agreement percentages are misleading** - a judge that always returns "pass" might achieve 90% agreement if errors only occur 10% of the time. The validation process involves iterating on the judge prompt until alignment with human judgment reaches acceptable levels.

The judge prompt itself becomes a living product requirements document, encoding specific business logic about acceptable behavior. For example, a real estate AI assistant's handoff judge might specify exact conditions requiring human intervention: explicit customer requests, policy-mandated transfers, sensitive resident issues, or data unavailability. These prompts evolve based on actual observed failures rather than hypothetical requirements, making them far more effective than traditional specifications.

## 5. The Relationship Between Evals and Product Requirements

***"Evals are the new PRDs... This is exactly what a product requirements document should be - this eval judge that's telling you exactly what it should be and it's automatic and running constantly."***

Evals represent an evolution of traditional product requirements documentation. While PRDs describe intended behavior upfront, eval judges encode discovered requirements based on actual usage patterns and failure modes. This creates a **feedback loop where product understanding deepens through systematic observation** rather than upfront speculation.

The process doesn't replace traditional product planning but enhances it significantly. Teams still need initial product vision and requirements to guide development. However, the eval process reveals requirements that couldn't have been anticipated - edge cases, unexpected user behaviors, and emergent failure patterns that only become visible through real-world usage. The eval judges then codify these discoveries into automated tests that continuously validate product behavior.

This approach is particularly powerful because **requirements drift is inevitable in AI products**. Research shows that even expert practitioners can't fully specify quality criteria upfront. Their understanding of "good" versus "bad" outputs evolves as they review more examples. Evals provide a systematic way to capture this evolving understanding and operationalize it through automated testing.

## 6. Common Misconceptions and Anti-Patterns

***"The top misconception is 'We live in the age of AI. Can't the AI just eval it?' But it doesn't work... Humans will still have jobs."***

Several critical misconceptions plague eval implementation. The most damaging is the belief that **AI can fully automate the evaluation process from the start**. While LLMs excel at synthesizing and categorizing errors once identified, they lack the context to perform initial error detection. An LLM reviewing a customer service interaction might miss that the AI offered a non-existent feature because it lacks knowledge of actual product capabilities.

Another major anti-pattern is **skipping directly to writing tests without data analysis**. Teams often want to immediately create evaluation suites based on hypothetical failures or requirements. This approach misses actual failure modes that only emerge through systematic observation. The errors discovered through data analysis - garbled text message handling, inappropriate conversation flows, missing handoffs - are often completely different from what teams initially expected.

The **over-reliance on generic evaluation metrics** represents another common failure. Tools offering pre-built evaluators for "hallucination scores" or "coherence ratings" provide limited value for specific applications. A handoff error in a real estate application has no correlation with general language model benchmarks like MMLU scores or math problem-solving abilities. Effective evals must be tailored to specific product requirements and failure modes.

## 7. The Eval Implementation Process

***"For most products, you do this process once and then you build on it... People do this like once a week and you can do all of this in like 30 minutes."***

The initial eval implementation typically requires **3-4 days of focused effort** for the first round of comprehensive error analysis, categorization, and judge creation. This includes reviewing traces, creating axial codes, building initial LLM judges, and validating them against human judgment. While this upfront investment might seem substantial, it's a one-time cost that yields continuous benefits.

After initial setup, maintenance becomes remarkably lightweight - typically **30 minutes weekly** to review new error patterns and refine evaluators. Most applications require only **4-7 LLM judge evaluators** for comprehensive coverage, as many errors can be fixed through simple prompt improvements rather than requiring ongoing evaluation. The key is prioritizing evaluators for persistent, business-critical failure modes rather than attempting exhaustive coverage.

Teams should **build custom tools to reduce friction** in the evaluation process. Simple web applications for reviewing traces, automated categorization pipelines, and dashboard visualizations can be created in hours using AI-assisted coding tools. The investment in tooling pays dividends by making evaluation a natural part of the development workflow rather than a burdensome additional process.

## 8. The Business Impact of Systematic Evaluation

***"The goal here is to make your product better, which will make your business more successful. This isn't just a little exercise to catch bugs... this is the way to make AI products better."***

Systematic evaluation directly drives business value by improving the core user experience of AI products. Since the AI interaction often **is** the product, every improvement in response quality, error reduction, or conversation flow directly enhances customer satisfaction and retention. Companies implementing rigorous eval processes report dramatic improvements in product quality within weeks of adoption.

The competitive advantage of strong eval practices compounds over time. Organizations with mature eval processes can **iterate faster and with more confidence** than competitors relying on ad-hoc testing. They catch regressions before deployment, identify improvement opportunities systematically, and maintain consistent quality even as they scale. This creates a flywheel effect where better evaluation leads to better products, which generate more usage data, enabling even better evaluation.

The cost optimization benefits are equally significant. Through systematic evaluation, teams can identify opportunities to **replace expensive model calls with cheaper alternatives** while maintaining quality. By understanding exactly which interactions require advanced capabilities versus simple responses, organizations can optimize their AI spend without compromising user experience. Some teams report cost reductions of 50% or more through eval-driven optimization while actually improving product quality.