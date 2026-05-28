# A. Core questions (2016–2021)

### A1) Trump: media sentiment vs US market volatility

**Question:** How did media sentiment towards Donald Trump evolve from the 2016 campaign through the end of his presidency (2016–2020), and how did it align with volatility spikes in VIX / S&P 500 drawdowns around major events (election night, travel ban, trade-war escalations, impeachment, COVID crash)?
**Checks:** weekly sentiment series + event windows + changepoints on sentiment and VIX.

### A2) Facebook / Cambridge Analytica: shift to “techlash” + stock drawdowns

**Question:** How did Facebook coverage shift from innovation/growth framing to privacy/regulation framing around the Cambridge Analytica scandal (2016–2019), and how did this correspond to FB stock drawdowns?
**Checks:** topic-share change pre/post March–April 2018 + sentiment drift + event overlay.

### A3) COVID-19: tone + topic evolution across phases

**Question:** How did media tone and dominant themes around COVID-19 evolve from outbreak (late 2019/early 2020) to vaccine rollout (2021), and how did health vs economy vs civil-liberty frames compete over time?
**Checks:** phase segmentation + topic distribution by phase + sentiment by frame.

### A4) Greta Thunberg / youth climate activism: framing across regions

**Question:** How did media coverage of Greta Thunberg and youth climate activism evolve (2018–2021), and how did framing differ by region/outlet type (personalization vs policy vs skepticism/backlash)?
**Checks:** region inference reliability + topic-by-region + sentiment-by-topic×region.

### A5) Crypto cycles: tone/themes vs BTC market phases

**Question:** How did media tone and themes around Bitcoin/crypto change across the 2017 bull run, 2018 crash, and 2020–2021 bull market, and how did topic shifts align with BTC turning points?
**Checks:** phase detection from BTC price + topic modeling per phase + sentiment per phase/topic.

### A6) Tesla/EV mainstreaming: hype vs safety vs market acceptance

**Question:** How did media sentiment towards Tesla/EVs evolve (2016–2021), especially around Autopilot accidents, Model 3 production issues, and S&P 500 inclusion, and how did this align with TSLA price moves?
**Checks:** event-tagging + weekly sentiment + theme spikes around events + price overlay.

### A7) US–China trade war & Huawei/5G: competing frames

**Question:** How did Western media coverage of Huawei and the US–China trade war evolve (2018–2021), and how did security vs economic vs tech-innovation frames compete across regions?
**Checks:** topic-by-region×year + sentiment-by-topic×region.

### A8) Brexit negotiations: coverage tone vs GBP volatility

**Question:** How did media tone and key themes around Brexit evolve from the 2016 referendum through the UK’s exit process (2016–2020), and how did sentiment/topic shifts align with GBP volatility around major milestones (Article 50, deal votes, extensions, withdrawal agreement)?
**External data:** GBP/USD (or GBP/EUR) + implied/realized volatility proxy if available.
**Checks:** milestone windows + changepoints + topic-share evolution.

---

# B. “Hard” multi-hop / tool-composition questions (must resolve indirection first)

### H1) Spouse indirection (Bill Gates → Melinda French Gates) + 2021 divorce

**Question:** How did media coverage of the spouse of the Microsoft co-founder who runs a major philanthropic foundation change around the 2021 divorce announcement?
**Must-do tool steps:** resolve description → person; fetch event date; retrieve and compare pre/post.

### H2) Parent company (Instagram → Facebook/Meta) around Cambridge Analytica

**Question:** How did media sentiment towards the company that owns Instagram change before vs after the Cambridge Analytica scandal?

### H3) Role + other company (SpaceX founder → Tesla) + SEC settlement (2018)

**Question:** How did media coverage of the electric-car company led by the founder of SpaceX change after the 2018 SEC settlement over tweets?

### H4) Movement figurehead (“How dare you” UN 2019 → Greta Thunberg)

**Question:** How did global media coverage of the youth climate activist behind the “How dare you” UN speech change between 2018 and 2021?

### H5) Owner/brand mapping (WhatsApp → Meta) + encryption/data-sharing debate

**Question:** How did media tone towards the company that owns WhatsApp change around the 2016–2017 encryption and data-sharing debates?

### H6) Product → parent company (TikTok → ByteDance) + US ban pressure 

**Question:** How did media tone towards the company that owns TikTok evolve around the 2020–2021 US ban / divestment pressure, and did the dominant framing shift between “national security” vs “tech/consumer product” vs “geopolitics”?
**Must-do tool steps:** resolve TikTok owner → ByteDance; retrieve by entity; segment by key dates.

---

# C. Negative-control / “no real relationship” sanity checks (expected: no robust link)

### N1) Bitcoin vs consumer staples sentiment (Colgate-Palmolive)

**Question:** Did Bitcoin price movements (2016–2021) have any systematic impact on media sentiment towards Colgate-Palmolive?
**Expected:** no robust relationship.

### N2) Oscars vs US bank sentiment

**Question:** Did the number of Oscars won in a year meaningfully affect media sentiment toward major US banks (JPM, BAC, etc.) from 2016–2021?
**Expected:** no robust relationship.

### N3) Zurich weather vs OPEC sentiment

**Question:** Is there any meaningful relationship between daily weather in Zurich and media sentiment towards OPEC decisions (2016–2021)?
**Expected:** none.

### N4) eSports results vs central bank policy coverage

**Question:** Did major eSports tournament results (e.g., LoL Worlds winners) cause measurable shifts in sentiment about Fed/ECB policy (2016–2021)?
**Expected:** none.

---

# D. Counterfactual controls (plausible-sounding, but the event never happened)

These are designed to test whether the system can (a) fail gracefully, (b) verify claims via tools/evidence, and (c) explicitly conclude “this event did not occur / cannot be supported”.

### I1) “Meta rebrand in 2018” (counterfactual)

**Question:** How did media sentiment toward Facebook change after the company rebranded to “Meta” in 2018, and did coverage shift toward “metaverse” framing immediately afterward (2018–2019)?
**Ground truth:** Meta rebrand was not in 2018 → system should reject or correct the premise.

### I2) “Amazon spun off AWS in 2019 IPO” (counterfactual)

**Question:** How did media coverage of Amazon change after it spun off AWS via a separate IPO in 2019, particularly regarding antitrust and valuation framing (2018–2020)?
**Ground truth:** AWS was not spun off / no IPO → system should detect impossibility.

