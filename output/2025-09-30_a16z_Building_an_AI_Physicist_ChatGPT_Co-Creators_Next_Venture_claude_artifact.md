**Guest:** Doge Koksoy and Liam Fedus (Co-founders of Periodic Labs; Koksoy was co-creator of ChatGPT at OpenAI, Fedus led physics teams at DeepMind)

**Key Quote:**
***"Science is by its nature iterative. Even the smartest humans tried many times before they discovered the things they discovered. If LLMs aren't iterating on science with real experiments, they won't discover science."***

**Contents Covered:**
1. Building an AI physicist with experimental verification in the loop
2. Why current LLMs fail at physics despite scaling laws
3. High-temperature superconductivity as the north star goal
4. The necessity of physical labs for AI training vs digital-only approaches
5. Team composition bridging ML and physical sciences
6. Commercial applications in advanced manufacturing and materials
7. Mid-training techniques for domain-specific knowledge injection
8. Academic partnerships and grant programs
9. Scaling laws and domain transfer limitations
10. Powder synthesis and autonomous experimentation

**Detailed Analysis:**

## 1. Building an AI Physicist with Experimental Verification

***"We're taking these precursor technologies and saying if you care about advancing science, we need to have experiment in the loop. That becomes our reward function for our agents."***

Periodic Labs is developing a frontier AI research lab that uses large language models to advance physics and chemistry through tight integration with experimental verification. The core innovation involves replacing traditional reward functions used in AI training - like math graders and code validators - with **physically grounded reward functions** derived from actual laboratory experiments. This approach treats nature itself as the reinforcement learning environment, where experimental results provide the ground truth for training AI systems.

The system architecture involves giving AI agents access to tools beyond typical programming interfaces. These agents can utilize **quantum mechanics simulators** to model different physical systems, but critically, all predictions and simulations are validated against real experimental data generated in Periodic's laboratories. This creates a feedback loop where the AI learns not just from theoretical models or published literature, but from direct interaction with physical reality through iterative experimentation.

## 2. Why Current LLMs Fail at Physics Despite Scaling Laws

***"Scaling laws empirically seem to continue to hold, but there's a question of what is this y-axis. The test distribution for internet-trained models is very different from what we're talking about."***

Current language models demonstrate predictable scaling properties when trained on internet data, showing power law improvements in performance as compute and data increase. However, these improvements are **domain-specific** - a model trained on internet text and code won't automatically cure cancer or discover new materials, regardless of scale. The knowledge required for breakthrough physics discoveries simply doesn't exist in current training datasets.

The problem extends beyond mere data availability. Published scientific literature suffers from **systematic biases**: negative results are rarely published despite their scientific value, reported physical properties often span multiple orders of magnitude due to measurement uncertainties, and the iterative nature of scientific discovery isn't captured in static papers. When training on such noisy, incomplete data, models can at best replicate the existing distribution of knowledge without achieving deeper understanding of underlying physics.

**In-domain versus out-of-domain generalization** follows different power laws. While both improve monotonically with scale, the slope of improvement for out-of-domain tasks can be so small that centuries of compute might be needed to achieve meaningful progress. This fundamental limitation means that to accelerate scientific discovery, training data must be specifically targeted toward the desired domain rather than hoping for emergence from general scaling.

## 3. High-Temperature Superconductivity as the North Star

***"If we could find a 200 Kelvin superconductor, even before we make any product with it, that in itself says so much about the universe that we didn't know yet."***

High-temperature superconductivity serves as Periodic's primary technical goal, with current records at **135 Kelvin at ambient pressure**. This choice is strategic for multiple reasons: superconductivity represents a phase transition that's robust to many experimental details that cannot yet be simulated, making it more tractable than properties dominated by defects or microstructure. The phenomenon unites both career physicists and non-specialists in shared excitement about its potential impact.

Achieving higher temperature superconductivity requires mastering numerous foundational capabilities: **autonomous synthesis, autonomous characterization, accurate simulation of quantum mechanical systems**, and integration of literature knowledge with experimental results. Each sub-goal represents a significant technical achievement that would benefit the broader scientific community. The pursuit forces development of generalizable tools and methods applicable across materials science, chemistry, and condensed matter physics.

## 4. The Necessity of Physical Labs for AI Training

***"Humans won't discover anything important if put in a room without any chance to iterate on something. We feel like the important thing to teach these LLMs is the method of scientific inquiry."***

Periodic operates physical laboratories focused on **powder synthesis** - mixing powders of existing materials and heating them to specific temperatures to create new materials. This method, while simple enough for robotic automation at the level of coffee-making robots, can discover superconductors, magnets, and other technologically critical materials. The lab generates high-throughput, high-quality experimental data that serves as ground truth for AI training.

The laboratory approach addresses three critical gaps in current AI training: **noisy published data** with formation enthalpy labels too unreliable for predictive modeling, absence of negative results that provide crucial learning signals, and the fundamental need for iterative experimentation to collapse epistemic uncertainty. Without actual experiments, models cannot distinguish between genuine physical constraints and artifacts of incomplete or incorrect literature data.

Physical verification creates a fundamentally different training paradigm. Instead of optimizing against static datasets, the AI system learns through active experimentation, receiving immediate feedback about the accuracy of its predictions. This mirrors how human scientists actually work - through cycles of hypothesis, experiment, and refinement rather than pure theoretical reasoning.

## 5. Team Composition Bridging ML and Physical Sciences

***"These group of physicists, chemists, simulation experts and some of the best machine learning researchers in the world have never been part of one concerted effort."***

Periodic's team of approximately 30 people represents an unprecedented convergence of expertise. The organization requires world-class talent across multiple pillars: **LLM expertise** covering mid-training, reinforcement learning, and infrastructure; **experimental expertise** spanning solid-state chemistry, solid-state physics, and automation; and **simulation capabilities** encompassing theoretical physics and computational modeling. Each domain contains fractal sub-specializations requiring deep expertise.

Cultural integration happens through structured knowledge transfer. Weekly teaching sessions feature LLM researchers explaining reinforcement learning loops and data cleaning techniques, while physicists and chemists teach quantum mechanics, materials science, and the history of scientific discovery. The team maintains a **"no stupid questions" culture** that encourages cross-domain learning. Bridge personnel who understand multiple domains serve as translators between different technical cultures.

The knowledge gap paradox means that even expert physicists have more to learn than they know, making the learning curve for newcomers relatively comparable. The team actively seeks individuals who combine deep curiosity with pragmatic solution-orientation, world-class expertise in at least one dimension, and a sense of urgency about accelerating scientific discovery.

## 6. Commercial Applications in Advanced Manufacturing

***"There's so many industries like space, defense, semiconductors where they're dealing with iteration of materials and physics as part of their workflow."***

Periodic targets industries with massive R&D budgets that require materials innovation: **space, defense, semiconductors, and advanced manufacturing**. These sectors face common challenges: loss of senior expertise through retirement, need for AI strategy integration, lengthy iteration cycles for materials development, and complex workflows involving literature review, simulation, and experimentation. The company positions itself as an intelligence layer to accelerate these workflows.

The commercial strategy follows a land-and-expand model, solving well-scoped critical problems with clear evaluation metrics rather than attempting wholesale transformation of manufacturing processes. Initial engagements focus on **automating simulations** that currently require extensive training, integrating simulation results into design pipelines, and unifying disparate data sources. Success metrics are concrete: improved material properties like ductility, toughness, and strength that directly impact product performance.

Revenue generation comes from becoming the co-pilot for engineers and researchers in advanced industries, dramatically reducing iteration time and improving solution quality. The technology addresses the gap between current retrieval-based AI tools and the deep understanding required for materials innovation.

## 7. Mid-Training Techniques for Domain-Specific Knowledge

***"Mid-training is basically taking new data, new knowledge that's not in the model and you continue pre-training. The goal is to put a lot of knowledge into the model that doesn't exist before."***

Mid-training represents a critical innovation for injecting domain-specific knowledge between pre-training and post-training phases. This technique addresses the **knowledge cutoff problem** by incorporating fresh experimental data, simulation results, and domain expertise that doesn't exist in standard internet training corpora. For Periodic, this includes crystal structures, synthesis recipes, material properties, and experimental procedures.

The challenge extends beyond simple data mixing. Effective mid-training requires ensuring that different data distributions - simulation data, experimental results, theoretical calculations - are properly connected so that inclusion of one dataset improves performance on others. This creates **genuine generalization** rather than isolated pockets of knowledge. The process transforms general language models into expert systems for physics and chemistry.

Customer deployments face unique challenges around data privileges and access control. While retrieval systems can match user permissions, pre-training or mid-training on proprietary data requires careful bucketing of knowledge into different model versions. Moving beyond retrieval to proper training with **high-compute reinforcement learning** represents a fundamental shift in how industrial R&D organizations can leverage AI.

## 8. Academic Partnerships and Grant Programs

***"So much of the simulation tooling we use has been developed in academia. We want to enable some of this amazing work going on in academia."***

Periodic maintains deep connections with academic research through two major initiatives. An **advisory board** includes leading experts like Z.X. Shen from Stanford for experimental superconductivity, Steve Kivelson for theoretical physics, Mercouri Kanatzidis from Northwestern for synthesis expertise, and Chris Wolverton for high-throughput density functional theory calculations. These advisors ensure alignment with long-term research directions and government funding priorities.

A grant program supports academic work that advances LLMs, agents, synthesis methods, materials discovery, and physics modeling. This recognizes that certain fundamental research is best conducted in university settings while still benefiting industrial applications. Academic partnerships provide critical insights into **proper scientific reasoning strategies** - such as thinking in terms of symmetries rather than brute-force calculation - that industry teams might miss.

The symbiotic relationship sees academia developing fundamental tools like quantum mechanics simulators and novel synthesis methods, while industry provides computational resources for large-scale simulations. Recent examples include major simulation work from Microsoft, DeepMind, and Meta built on academic foundations.

## 9. Scaling Laws and Domain Transfer Limitations

***"As you increase the size of your training set, in-domain performance improves as a power law, out-of-domain performance also improves as a power law, but depending on how far you are from the training distribution, that power law might have such a small slope that it's basically useless."***

Research on vision models and other domains confirms that while in-domain and out-of-domain generalization are monotonically correlated, the relationship is **non-linear**. A model achieving breakthrough performance on coding tasks won't automatically excel at materials discovery - the knowledge and iterative experience simply don't transfer. This fundamental limitation means targeted optimization toward specific scientific domains is essential rather than hoping for emergence from general scaling.

The most effective approach involves making target tasks as close as possible to the training distribution by iteratively updating training data based on experimental results. This creates a **tight feedback loop** between model predictions and physical reality, progressively improving the alignment between training and deployment distributions. The strategy represents a "beeline" toward specific scientific goals rather than hoping for serendipitous emergence.

Domain transfer between related physics subfields - from superconductivity to magnetism, for instance - shows promise but differs fundamentally from transfer to unrelated domains like fluid mechanics. Understanding these **generalization boundaries** is crucial for creating repeatable processes that can systematically advance through different scientific domains.

## 10. Powder Synthesis and Autonomous Experimentation

***"You take powders of existing materials, you mix them and you heat them up to certain temperature and it becomes a new material. A robot that's basically at the level of a coffee-making robot can mix powders and put it in a furnace."***

Powder synthesis represents an ideal starting point for autonomous experimentation due to its relative simplicity and broad applicability. This technique can produce **superconductors, magnets, and various technologically important materials** while being amenable to robotic automation. The process provides clear, measurable outcomes - such as superconducting transition temperatures - that serve as unambiguous reward signals for AI training.

The autonomous lab setup enables high-throughput experimentation with consistent quality control, generating the volume of data needed for effective machine learning. Unlike human researchers who might conduct dozens of experiments, automated systems can perform hundreds or thousands of iterations, exploring parameter spaces systematically. This scale advantage is crucial for discovering materials with properties at the edge of what's physically possible.

Success metrics are straightforward and unhackable: either a material exhibits superconductivity at a given temperature or it doesn't. Properties like **ductility, toughness, and strength** can be directly measured and optimized. This creates a tight coupling between AI predictions and physical outcomes, ensuring that model improvements translate directly to real-world materials discovery rather than merely better performance on benchmark datasets.