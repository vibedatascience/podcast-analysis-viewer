**Guest:** Patrick Hsu (Founder of Arc Institute, elite AI investor focused on synthetic biology, brain-computer interfaces, and robotics - working to accelerate scientific progress through foundation models and virtual cells)

**Key Quote:**
***"If we could figure out how to model the fundamental unit of biology, the cell, then from that we should be able to build."***

**Contents Covered:**
1. Why science is slow and Arc Institute's approach to acceleration
2. Virtual cell models and their potential to transform drug discovery
3. Comparison between AI progress in language/images vs biology
4. The gap between GPT-1 and GPT-3 moments for biological AI
5. Perturbation prediction and drug target identification
6. Bottlenecks in pharma: capital intensity, clinical trials, and success rates
7. The impact of GLP-1s and large patient population drugs
8. AI applications in drug discovery: hype vs hope vs heft
9. Investment focus areas: synthetic biology, BCIs, and robotics
10. Virtual Cell Challenge competition and open science initiatives

**Detailed Analysis:**

## 1. The Systemic Slowness of Science

***"It's this weird Gordian knot that ultimately comes down to incentives."***

Science moves slowly due to multiple interconnected factors that create a complex web of inefficiencies. The fundamental issue stems from how science funding operates, where individual research groups need to publish their own papers and make their own discoveries, creating silos rather than collaboration. The training system reinforces these divisions by rewarding individual achievement over collective progress. Modern scientific problems increasingly require multidisciplinary approaches - combining computational biology, genomics, chemical biology, molecular glues, neuroscience, and immunology - yet most research groups or companies struggle to excel at more than two disciplines simultaneously.

The Arc Institute was founded as an organizational experiment to address these structural problems. By bringing together five distinct scientific domains under one physical roof, the institute aims to increase "collision frequency" between disciplines. While universities theoretically unite multiple fields, the physical distribution across campuses and competing incentive structures prevent true collaboration. Arc's approach involves creating flagship projects that require contributions from multiple disciplines, such as finding Alzheimer's drug targets and developing virtual cell models. The goal is to enable work on problems that would be impossible for any single group to tackle alone.

## 2. Virtual Cells as the Next AlphaFold Moment

***"We want to get to that point with virtual cells where anytime you want to work with a cell, you're just going to use this algorithm."***

Virtual cell models represent the next frontier in computational biology, aiming to achieve for cellular biology what AlphaFold accomplished for protein structure prediction. The concept centers on **perturbation prediction** - understanding how cells transition between different states when subjected to various interventions. Every cell exists on a manifold of possible states: heart cells, blood cells, lung cells can become inflamed, apoptotic, cell cycle arrested, stressed, or metabolically starved. The key insight is that drug discovery fundamentally involves moving cells along this manifold from disease states to healthy states.

The practical implementation involves training models to predict which perturbations (drugs, genetic modifications, environmental changes) will shift a cell from state A to state B. This directly addresses drug discovery's core challenge: finding the right interventions to correct disease states. Complex diseases often require multiple coordinated perturbations rather than single targets - moving from accidental polypharmacology to purposeful combinatorial manipulation. The models would suggest sequences of changes: "first these three modifications, then these two, then these six" to achieve desired cellular transitions.

Success would mean creating a co-pilot for wet lab biologists, helping them decide which experiments to run among countless possibilities. The ultimate goal is **in silico target identification** - computationally discovering new drug targets and the compositions needed to modulate them, potentially enabling a vertically integrated AI-powered pharmaceutical company.

## 3. Why Biology Lags Behind Language and Image AI

***"Natural language and video modeling is easier than modeling biology. We don't speak the language of biology."***

The dramatic progress in language and image AI compared to biological applications stems from a fundamental difference in human intuition and data interpretation. When training language or image models, developers possess native understanding - they speak languages fluently and interpret images naturally. This enables rapid evaluation of model outputs and quick iteration cycles. In contrast, biological data like DNA sequences or protein interactions represent foreign languages that even experts struggle to interpret intuitively.

The iteration cycle in biology requires **"lab in the loop"** validation - actual wet lab experiments to test model predictions against experimental ground truth. While AI researchers can evaluate GPT outputs instantly, biological predictions require growing cells, conducting assays, and measuring outcomes over days or weeks. This dramatically slows the feedback loop essential for model improvement.

Additionally, biological measurement presents unique challenges. We cannot measure all relevant biological components with current technology - metabolites, spatial dynamics, and many protein interactions remain difficult to capture at scale. The field must work with incomplete data, using RNA as a "lower resolution mirror" for protein activity. While individual RNA measurements may poorly reflect protein states, massive scale data collection (Arc plans to generate **one billion perturbed single cells**) can capture echoes of protein signaling in transcriptional states.

## 4. Current State: Between GPT-1 and GPT-2

***"Most people would agree we're somewhere between GPT-1 and GPT-2."***

The current state of biological AI models sits at an early but promising stage, comparable to the transition between GPT-1 and GPT-2 in language models. The excitement stems not from current capabilities but from achieving GPT-1 level functionality and observing clear scaling laws that suggest improvement paths. Arc's EVO DNA foundation models generate what researchers describe as "blurry pictures of life" - genome sequences that wouldn't produce viable organisms if synthesized, but show meaningful biological patterns.

The GPT-3 moment for biology will arrive when models can **rediscover Nobel Prize-winning biology**. Key benchmarks include: predicting that the four Yamanaka factors can reprogram fibroblasts into stem cells (2009 Nobel Prize), discovering differentiation factors like neurogenin-2 or ASCL1 that convert stem cells into neurons, and recapitulating mechanisms of FDA-approved drugs. These represent "textbook examples" that any credible biological model should reproduce, moving beyond current ML benchmarks focused on technical metrics like mean absolute error.

The path forward requires full-stack development: curating public data, generating massive internal datasets, building benchmarks, training new architectures, and iterating based on experimental validation. Progress depends on three categories of advancement: **invention** (creating new measurement technologies), **engineering** (improving existing tools), and **scaling** (massively expanding data generation). Some technologies like single-cell transcriptomics are scale-ready today, while others like spatial and temporal measurements still require fundamental invention.

## 5. Pharmaceutical Industry Bottlenecks and Solutions

***"We have 90% of drugs failing in clinical trials. That means two things: we're targeting the wrong target, or the drug matter doesn't do the job."***

The pharmaceutical industry faces a crisis of capital intensity and low success rates that virtual cell models could help address. Drug development fails for two primary reasons: incorrect target selection (pursuing biological mechanisms that don't actually drive disease) or inadequate drug design (molecules that can't properly modulate the intended target). Current approaches circle the wagons around well-validated mechanisms with small patient populations, resulting in low expected value despite high development costs.

The GLP-1 revolution demonstrates the massive value creation possible when addressing large patient populations - **over a trillion dollars** in market cap added to Eli Lilly and Novo Nordisk, exceeding the combined value of all biotech companies started in the past 40 years. This success has culturally shifted industry ambition toward tackling endemic problems affecting millions rather than rare diseases affecting thousands.

Three key improvements could transform the industry: **reducing capital intensity** through better success rates, **compressing timelines** especially in clinical development, and **increasing effect sizes** by targeting the right biology more precisely. The challenge remains that even with perfect computational models for drug design, physical testing in animals and humans creates unavoidable bottlenecks. Some trials inherently require extended timeframes - cancer drugs must demonstrate survival benefits, longevity interventions need lifetime studies.

## 6. The Manufacturing and Regulatory Challenge

***"Even if we can solve the designing part, we still need to make these things physically and test them in animals and people."***

The contrast between the U.S. as a nation of lawyers versus China as an engineering state manifests clearly in drug development challenges. From 1980 to 2020, all Democratic presidential candidates attended law school, while China's leadership consists primarily of engineers. This philosophical difference echoes through FDA regulatory requirements and the complex approval processes that slow drug development.

Even with perfect AI-designed molecules - "a trillion binders in silico with exquisite drug matter" - the physical requirements remain daunting. Drugs must progress through mice, rats, monkeys, and finally humans, with each step taking months to years. Increasingly, companies explore running Phase 1 trials overseas to build data packages for domestic Phase 2 efficacy trials, but this represents incremental rather than transformative change.

Virtual cells might suggest highly specific requirements like "target this GPCR only in heart tissue, not anywhere else" - but current drug chemistry cannot achieve such tissue-specific targeting. This creates a **"Russian nesting doll of complexity"** requiring advances in understanding, perturbation capabilities, and safety assessment. Novel chemical biology approaches must be invented to enable tissue or cell-type specific drug delivery.

## 7. AI in Drug Discovery: Hype, Hope, and Heft

***"There's hype in toxicity prediction models, hope in protein design, and heft in pathology AI prediction models."***

The landscape of AI applications in drug discovery shows clear differentiation between overpromised capabilities and genuine breakthroughs. **Hype** surrounds toxicity prediction models that claim to predict drug safety from molecular structures alone - a problem too complex for current approaches. Multimodal biological models combining molecular, spatial, and other data layers also remain largely aspirational despite significant investment and attention.

**Hope** centers on protein-related applications, building on AlphaFold's success. Protein design, binding prediction, and structural biology applications show genuine promise with improving capabilities. The ability to computationally dock small molecules to every protein in the proteome for off-target prediction represents tangible progress toward safer drug design.

**Heft** already exists in pathology and radiology AI that automates expert analysis, and in administrative applications like regulatory filing generation. These "boring but important" uses provide immediate value without requiring breakthrough science. Within a few years, AI will become as native to the drug discovery stack as the internet or phones - not a differentiator but essential infrastructure. The key remains connecting design capabilities to safety and efficacy prediction through iterative lab validation.

## 8. Investment Focus: Biology, BCIs, and Robotics

***"There are a few things that if we get them right in our lifetime will fundamentally change the world."***

Three technological domains stand poised to fundamentally transform human experience within our lifetimes. **Synthetic biology** promises interventions for sleep, longevity, and metabolic health that could rival GLP-1s' impact. **Brain-computer interfaces** will enable direct neural control and enhancement, moving from medical applications to augmentation. **Robotics** - both industrial and consumer - will scale physical labor in unprecedented ways, addressing fundamental economic constraints.

Success requires assembling teams with the right combination of technical innovation, product intuition, and business acumen - a "RPG dice roll" where founders start with different base stats. Technical brilliance without commercial thinking fails as often as commercial expertise without product sense. The key is identifying ideas that "must happen in the world" and finding the right people at the right time to execute them - creating outcomes that literally wouldn't exist without specific intervention.

Current investments reflect this philosophy: Newman for longevity, Nudge for brain-computer interfaces, The Bot Company for robotics. Each represents a bet on inevitable technological progress that requires specific teams and timing to manifest. The opportunity lies not in predicting far-future science fiction but in executing on important ideas whose time has come.

## 9. The Agent Revolution and New Architectures

***"Agents do real work. Compared to SaaS companies that came before, agents replace real productivity."***

The transformation from software-as-a-service to autonomous agents represents a fundamental shift in economic value creation. While SaaS companies competed for limited software budgets, agents can attack the much larger services economy by replacing actual human labor. Computer-use agents currently trail coding agents by approximately a year but will follow similar improvement trajectories - progressing from minutes of error-free work to hours to days of autonomous operation.

The current transformer architecture, dating to 2017, appears due for disruption based on deep learning's historical eight-year innovation cycles. Numerous overlooked papers from machine learning's golden age (2009-2015) with fewer than 30 citations contain potentially transformative ideas that couldn't be properly tested at the scale of that era. As compute costs decline, these concepts can be revisited at 1B, 7B, 35B, and 70B parameter scales where scaling laws might suddenly emerge.

New super-intelligence labs have opportunities beyond what established foundation model companies pursue, as incumbents increasingly become applied AI companies focused on product development and revenue generation. Research groups like Sakana AI, founded by Attention Is All You Need co-author Llion Jones, explore model merging and evolutionary selection approaches that could unlock new capabilities. The frontier lies in moving beyond RL gyms to discover novel learning paradigms and reward signals.

## 10. The Virtual Cell Challenge and Open Science

***"We created our own virtual cell challenge with $100,000 prizes. I just want this thing to exist in the world."***

Following AlphaFold's emergence from the CASP protein folding competition, Arc Institute launched the Virtual Cell Challenge to catalyze similar breakthroughs in cellular modeling. The competition, sponsored by NVIDIA, 10X Genomics, and Ultima, offers $100,000 in prizes for perturbation prediction models that can accurately forecast cellular responses to interventions.

The challenge represents a commitment to open science and transparent capability assessment. By establishing clear benchmarks and annual evaluations, the competition can track progress toward the "ChatGPT moment" for biology. The initiative welcomes participants from all backgrounds - both bio-ML experts and engineers from other domains - recognizing that breakthrough insights often come from unexpected directions.

The ultimate goal transcends any single institution's success. Whether Arc or another group achieves virtual cell capabilities matters less than ensuring this transformative technology comes to exist. This philosophy of putting scientific progress above institutional glory exemplifies the collaborative approach needed to accelerate discovery and "make science faster" for humanity's benefit.