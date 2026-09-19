(() => {
  "use strict";

  const qs = (sel, root = document) => root.querySelector(sel);
  const qsa = (sel, root = document) => [...root.querySelectorAll(sel)];
  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  // Footer year.
  qsa("[data-year]").forEach(el => { el.textContent = new Date().getFullYear(); });

  // Repository wiring. If no public repository is configured, keep unfinished
  // project plumbing off the recruiter-facing surface entirely.
  const config = window.HYDRA_CONFIG || {};
  const repoLinks = qsa("[data-repo-link]");
  const repoSection = qs("[data-repo-section]");
  if (config.repositoryUrl) {
    repoLinks.forEach(link => {
      link.href = config.repositoryUrl;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.removeAttribute("aria-disabled");
      link.hidden = false;
      if (link.classList.contains("repo-button")) link.textContent = "Open repository ↗";
    });
    if (repoSection) repoSection.hidden = false;
  } else {
    repoLinks.forEach(link => { link.hidden = true; });
    if (repoSection) repoSection.hidden = true;
  }

  // Optional public profile/contact wiring. These stay completely hidden until
  // configured so an unfinished recruiter surface is never advertised.
  const publicLinkGroups = qsa("[data-public-links]");
  const linkedinLinks = qsa("[data-linkedin-link]");
  const contactLinks = qsa("[data-contact-link]");
  let hasPublicLink = false;
  if (config.linkedinUrl) {
    hasPublicLink = true;
    linkedinLinks.forEach(link => {
      link.href = config.linkedinUrl;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.hidden = false;
    });
  }
  if (config.contactEmail) {
    hasPublicLink = true;
    contactLinks.forEach(link => {
      link.href = `mailto:${config.contactEmail}`;
      link.hidden = false;
    });
  }
  publicLinkGroups.forEach(group => { group.hidden = !hasPublicLink; });

  // Mobile navigation.
  const navToggle = qs("[data-nav-toggle]");
  const nav = qs("[data-nav]");
  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    qsa("a", nav).forEach(a => a.addEventListener("click", () => {
      nav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    }));
  }

  // Scroll state + progress meter.
  const header = qs("[data-header]");
  const meter = qs(".scroll-meter span");
  const updateScroll = () => {
    const y = window.scrollY || 0;
    if (header) header.classList.toggle("is-scrolled", y > 18);
    if (meter) {
      const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      meter.style.width = `${Math.min(100, (y / max) * 100)}%`;
    }
  };
  updateScroll();
  window.addEventListener("scroll", updateScroll, { passive: true });

  // Soft cursor glow on pointer devices.
  const glow = qs(".cursor-glow");
  if (glow && window.matchMedia("(pointer:fine)").matches) {
    window.addEventListener("pointermove", (event) => {
      document.documentElement.style.setProperty("--mx", `${event.clientX}px`);
      document.documentElement.style.setProperty("--my", `${event.clientY}px`);
    }, { passive: true });
  }

  // Reveal system.
  const revealEls = qsa("[data-reveal]");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reducedMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(el => el.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(el => observer.observe(el));
  }

  // Architecture explorer.
  const stages = {
    source: {
      kicker: "STAGE 01",
      owner: "OWNER · SOURCE LANE",
      title: "Source Intake",
      summary: "Capture source material without losing the context required to identify and audit it later.",
      question: "What entered the system?",
      preserve: "origin · source identity · arrival context",
      failure: "quarantine unknown or malformed source state",
      output: "normalized source envelope",
      principle: "Do not clean away the evidence needed to explain what arrived."
    },
    identity: {
      kicker: "STAGE 02",
      owner: "OWNER · IDENTITY LANE",
      title: "Identity",
      summary: "Resolve what the object is before downstream stages assume two records refer to the same thing.",
      question: "Which entity or case does this represent?",
      preserve: "canonical IDs · aliases · crosswalk evidence",
      failure: "stop ambiguous or conflicting identity bindings",
      output: "resolved identity with binding evidence",
      principle: "Similarity is not identity. Bind deliberately and keep the proof."
    },
    contract: {
      kicker: "STAGE 03",
      owner: "OWNER · CONTRACT LANE",
      title: "Contracts",
      summary: "Validate shape, semantics, ownership, and derivation rights before a consumer receives the handoff.",
      question: "Is this producer allowed to supply this requirement?",
      preserve: "field ownership · version · authority · derivation rules",
      failure: "BLOCKED_BY_MISSING_AUTHORITY when proof is absent",
      output: "admissible contract-bound handoff",
      principle: "A field being discoverable is not the same as a field being authorized."
    },
    transform: {
      kicker: "STAGE 04",
      owner: "OWNER · TRANSFORM LANE",
      title: "Transform",
      summary: "Apply bounded, inspectable transformations without breaking the connection between input and output.",
      question: "What changed, under which rule?",
      preserve: "input references · transform version · output receipt",
      failure: "reject non-reproducible or out-of-contract mutation",
      output: "canonical transformed object",
      principle: "A transformation should reduce ambiguity, not erase its own history."
    },
    lineage: {
      kicker: "STAGE 05",
      owner: "OWNER · LINEAGE LANE",
      title: "Lineage",
      summary: "Link outputs back to the source, transform, and predecessor state required to reproduce or audit them.",
      question: "Where did this output come from?",
      preserve: "source refs · parent artifacts · stage receipts · hashes",
      failure: "block orphaned or stale lineage references",
      output: "traceable lineage chain",
      principle: "A useful answer should still know the route it took through the system."
    },
    trust: {
      kicker: "STAGE 06",
      owner: "OWNER · TRUST / HISTORY LANE",
      title: "Trust / History",
      summary: "Preserve contradictory evidence, reversals, freshness, and history instead of flattening uncertainty into one value.",
      question: "What agrees, conflicts, reversed, or became stale?",
      preserve: "competing evidence · timestamps · reversals · source context",
      failure: "do not silently delete or overwrite conflict",
      output: "adjudicable evidence state",
      principle: "Raw volume is not truth, and source quality is not a shortcut to truth."
    },
    release: {
      kicker: "STAGE 07",
      owner: "OWNER · RELEASE GATE",
      title: "Release Gate",
      summary: "Make the final handoff contingent on evidence that upstream authority, lineage, and contract requirements remain intact.",
      question: "May this object leave the governed pipeline?",
      preserve: "gate decision · blocker reason · baseline mutation status",
      failure: "quarantine, fail, or block with a named reason",
      output: "released object + machine-readable receipt",
      principle: "A truthful blocker is better than a fake green pipeline."
    }
  };

  const stageList = qs("[data-stage-list]");
  const stagePanel = qs("[data-stage-panel]");
  if (stageList && stagePanel) {
    const fields = {
      kicker: qs("[data-stage-kicker]", stagePanel),
      owner: qs("[data-stage-owner]", stagePanel),
      title: qs("[data-stage-title]", stagePanel),
      summary: qs("[data-stage-summary]", stagePanel),
      question: qs("[data-stage-question]", stagePanel),
      preserve: qs("[data-stage-preserve]", stagePanel),
      failure: qs("[data-stage-failure]", stagePanel),
      output: qs("[data-stage-output]", stagePanel),
      principle: qs("[data-stage-principle]", stagePanel)
    };

    const setStage = (key) => {
      const data = stages[key];
      if (!data) return;
      qsa("[data-stage]", stageList).forEach(button => {
        const active = button.dataset.stage === key;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-selected", String(active));
      });
      Object.entries(fields).forEach(([field, el]) => { if (el) el.textContent = data[field]; });
      stagePanel.animate?.([
        { opacity: .65, transform: "translateY(5px)" },
        { opacity: 1, transform: "translateY(0)" }
      ], { duration: 220, easing: "ease-out" });
    };

    qsa("[data-stage]", stageList).forEach(button => button.addEventListener("click", () => setStage(button.dataset.stage)));
  }

  // Constraint Intelligence explorer.
  const constraintClasses = {
    actual:{kicker:"CLASS 01",title:"Actual constraint",summary:"A binding limit materially restricts feasible throughput, access, capacity, or action.",question:"What is genuinely preventing more of the desired outcome?",evidence:"scope · time window · causal mechanism · competing evidence",failure:"calling correlated friction a causal constraint",value:"prioritized, explainable market constraint case",principle:"A constraint claim should be narrower than the evidence, never broader."},
    inconvenience:{kicker:"CLASS 02",title:"Inconvenience",summary:"Friction is present, but it does not materially bind feasible capacity, access, or throughput.",question:"Does this make execution harder without actually limiting what is feasible?",evidence:"cost of friction · workaround availability · throughput impact",failure:"promoting annoyance or inefficiency into a binding constraint",value:"keeps prioritization from chasing non-binding friction",principle:"Not every problem deserves the word constraint."},
    bottleneck:{kicker:"CLASS 03",title:"Bottleneck",summary:"A specific stage or resource limits end-to-end throughput even when other capacity remains available.",question:"Which stage is setting the ceiling for the whole flow?",evidence:"stage capacity · queue behavior · upstream/downstream slack",failure:"confusing the most visible delay with the throughput-limiting stage",value:"points investigation toward the binding stage",principle:"A bottleneck is a system relationship, not just a slow component."},
    shortage:{kicker:"CLASS 04",title:"Shortage",summary:"Required supply is insufficient relative to the demand, need, or capacity the market is trying to support.",question:"Is a required input unavailable in sufficient quantity, quality, or timing?",evidence:"supply levels · demand context · substitution · duration",failure:"calling high prices alone proof of physical shortage",value:"separates supply scarcity from other pricing and access mechanisms",principle:"Scarcity needs evidence of insufficient supply, not just evidence of pain."},
    pricing:{kicker:"CLASS 05",title:"Pricing pressure",summary:"Cost or price transmission materially changes access, demand, supply behavior, or feasible execution.",question:"Is price itself becoming the mechanism that constrains behavior?",evidence:"price path · elasticity context · substitution · margin or affordability impact",failure:"treating every price increase as a standalone constraint",value:"connects price movement to the behavior it actually limits",principle:"Price is a signal until the evidence shows how it binds."},
    technology:{kicker:"CLASS 06",title:"Technology barrier",summary:"Capability, interoperability, implementation maturity, or technical feasibility limits what can be executed.",question:"Is the limiting factor what the available technology can reliably do?",evidence:"capability boundary · maturity · integration requirements · alternatives",failure:"blaming technology for organizational or process constraints",value:"isolates technical feasibility from adjacent operational friction",principle:"Name the technical boundary, not the frustration around it."},
    regulatory:{kicker:"CLASS 07",title:"Regulatory barrier",summary:"Rules, permits, compliance obligations, or policy boundaries materially limit feasible market action.",question:"Which formal requirement changes what participants are allowed or able to do?",evidence:"jurisdiction · rule text · applicability · effective date · exemptions",failure:"treating rumor, expectation, or general policy climate as a binding rule",value:"links the market effect to the actual governing requirement",principle:"Regulatory claims need scope, jurisdiction, and effective authority."}
  };
  const constraintBrowser = qs("[data-constraint-browser]");
  const constraintPanel = qs("[data-constraint-panel]");
  if (constraintBrowser && constraintPanel) {
    const cFields={kicker:qs("[data-constraint-kicker]",constraintPanel),title:qs("[data-constraint-title]",constraintPanel),summary:qs("[data-constraint-summary]",constraintPanel),question:qs("[data-constraint-question]",constraintPanel),evidence:qs("[data-constraint-evidence]",constraintPanel),failure:qs("[data-constraint-failure]",constraintPanel),value:qs("[data-constraint-value]",constraintPanel),principle:qs("[data-constraint-principle]",constraintPanel)};
    qsa("[data-constraint-class]",constraintBrowser).forEach(button=>button.addEventListener("click",()=>{const data=constraintClasses[button.dataset.constraintClass];if(!data)return;qsa("[data-constraint-class]",constraintBrowser).forEach(item=>{const active=item===button;item.classList.toggle("is-active",active);item.setAttribute("aria-selected",String(active));});Object.entries(cFields).forEach(([field,el])=>{if(el)el.textContent=data[field];});constraintPanel.animate?.([{opacity:.65,transform:"translateY(5px)"},{opacity:1,transform:"translateY(0)"}],{duration:220,easing:"ease-out"});}));
  }

  // End-to-end case study explorer.
  const caseSteps = {
    inputs: {
      kicker: "STAGE 01 / INGEST",
      owner: "OWNER · SOURCE LANES",
      title: "Fragmented source facts",
      summary: "Four source types describe different parts of the same market condition. None of them is allowed to silently become the whole explanation.",
      input: "market event · operations notice · reference identity · historical baseline",
      control: "retain source identity, timestamps, aliases, and raw context",
      retain: "price movement · capacity reduction · canonical hub references · prior operating context",
      output: "normalized source envelopes ready for case binding",
      principle: "Ingest facts first. Interpretation belongs downstream."
    },
    identity: {
      kicker: "STAGE 02 / IDENTITY",
      owner: "OWNER · IDENTITY LANE",
      title: "Bind evidence to the same case",
      summary: "Aliases, facility references, market identifiers, and time windows must resolve before separate facts can be treated as evidence about one market condition.",
      input: "normalized source envelopes + reference crosswalk",
      control: "reject ambiguous aliases and mismatched market / location / window bindings",
      retain: "canonical object identity + alias evidence + rejected candidate context",
      output: "one identity-bound constraint case shell",
      principle: "Evidence cannot agree or conflict until the system proves it refers to the same thing."
    },
    contract: {
      kicker: "STAGE 03 / CONTRACT",
      owner: "OWNER · CONTRACT BOUNDARY",
      title: "Keep each source inside its authority",
      summary: "The market feed can own observed market values. The operations notice can own capacity facts. Reference data can own identity. None of them gets to invent the final causal conclusion.",
      input: "identity-bound source facts + producer contracts",
      control: "validate shape, field ownership, derivation rights, and required evidence",
      retain: "who supplied each fact + which rule allowed the handoff",
      output: "admissible evidence bundle with explicit ownership",
      principle: "Discoverable is not authorized. Availability does not create ownership."
    },
    evidence: {
      kicker: "STAGE 04 / EVIDENCE",
      owner: "OWNER · HISTORY / ADJUDICATION",
      title: "Preserve support, conflict, and limits",
      summary: "Evidence that supports a local throughput bottleneck is kept beside evidence that limits a broader shortage claim. The system does not delete inconvenient facts to make the case cleaner.",
      input: "contract-valid facts + history + competing context",
      control: "preserve contradictions, reversals, freshness, and source scope",
      retain: "supporting evidence + limiting evidence + temporal context",
      output: "adjudicable evidence state",
      principle: "A stronger explanation should survive competing evidence, not erase it."
    },
    classify: {
      kicker: "STAGE 05 / CONSTRAINT MODEL",
      owner: "OWNER · CONSTRAINT SEMANTICS",
      title: "Name the binding mechanism",
      summary: "In this representative case, local transfer capacity is the mechanism that binds. Pricing pressure remains relevant, but the evidence does not justify promoting it to the root constraint or calling the market system-wide short.",
      input: "adjudicable evidence state + constraint taxonomy",
      control: "separate actual constraint, bottleneck, shortage, pricing pressure, technology, regulation, and inconvenience",
      retain: "primary class + nearby alternatives + dimensions + evidence links",
      output: "bottleneck classification with local / current / reversible dimensions",
      principle: "The classification should be narrower than the evidence, never broader."
    },
    release: {
      kicker: "STAGE 06 / RELEASE",
      owner: "OWNER · DOWNSTREAM GATE",
      title: "Emit an inspectable market object",
      summary: "The downstream object carries the classification and enough references to recover the route from source facts through identity, contracts, evidence adjudication, and the release decision.",
      input: "classified constraint case + lineage + gate evidence",
      control: "block release if required authority, lineage, or identity proof is missing",
      retain: "classification + mechanism + evidence references + decision path",
      output: "governed constraint-intelligence object",
      principle: "A useful market output should still be able to explain where it came from."
    }
  };
  const caseBrowser = qs("[data-case-browser]");
  const casePanel = qs("[data-case-panel]");
  if (caseBrowser && casePanel) {
    const fields = {
      kicker: qs("[data-case-kicker]", casePanel), owner: qs("[data-case-owner]", casePanel),
      title: qs("[data-case-title]", casePanel), summary: qs("[data-case-summary]", casePanel),
      input: qs("[data-case-input]", casePanel), control: qs("[data-case-control]", casePanel),
      retain: qs("[data-case-retain]", casePanel), output: qs("[data-case-output]", casePanel),
      principle: qs("[data-case-principle]", casePanel)
    };
    const setCaseStep = (key) => {
      const data = caseSteps[key]; if (!data) return;
      qsa("[data-case-step]", caseBrowser).forEach(btn => {
        const active = btn.dataset.caseStep === key;
        btn.classList.toggle("is-active", active);
        btn.setAttribute("aria-selected", String(active));
      });
      Object.entries(fields).forEach(([field, el]) => { if (el) el.textContent = data[field]; });
      casePanel.animate?.([{opacity:.65,transform:"translateY(5px)"},{opacity:1,transform:"translateY(0)"}],{duration:220,easing:"ease-out"});
    };
    qsa("[data-case-step]", caseBrowser).forEach(btn => btn.addEventListener("click", () => setCaseStep(btn.dataset.caseStep)));
  }

  // Integrity Lab.
  const labRun = qs("[data-lab-run]");
  const labReset = qs("[data-lab-reset]");
  const consoleEl = qs("[data-console]");
  const consoleState = qs("[data-console-state]");
  const receipt = qs("[data-console-receipt]");
  const receiptOutcome = qs("[data-receipt-outcome]");
  const receiptHash = qs("[data-receipt-hash]");

  const scenarioOptions = qsa(".scenario-option");
  scenarioOptions.forEach(label => {
    const input = qs("input", label);
    if (!input) return;
    input.addEventListener("change", () => {
      scenarioOptions.forEach(item => item.classList.toggle("is-selected", qs("input", item)?.checked));
    });
  });

  const scenarioData = {
    valid: {
      outcome: "PASS",
      tone: "good",
      state: "PASS",
      lines: [
        ["info", "Loading frozen baseline receipt ... OK"],
        ["info", "Resolving producer contract for downstream handoff ... FOUND"],
        ["good", "Required fields are owned by the same authoritative producer."],
        ["good", "Lineage chain resolves to the expected source snapshot."],
        ["good", "Derivation rules: no unauthorized synthesis detected."],
        ["good", "Release gate satisfied. Handoff is admissible."],
        ["good", "OVERALL=PASS"]
      ]
    },
    missing: {
      outcome: "BLOCKED_BY_MISSING_AUTHORITY",
      tone: "warn",
      state: "BLOCKED",
      lines: [
        ["info", "Loading frozen baseline receipt ... OK"],
        ["info", "Resolving producer contract for downstream handoff ... PARTIAL"],
        ["warn", "Consumer requires fields with no authoritative native producer."],
        ["warn", "No contract grants a derivation path for the missing requirements."],
        ["info", "Synthetic defaulting is disabled by policy."],
        ["warn", "Release gate stopped before downstream consumption."],
        ["warn", "OVERALL=BLOCKED_BY_MISSING_AUTHORITY"]
      ]
    },
    ambiguous: {
      outcome: "FAIL_WITH_DEFECT",
      tone: "bad",
      state: "DEFECT",
      lines: [
        ["info", "Loading frozen baseline receipt ... OK"],
        ["info", "Resolving case identifier across candidate records ... MULTIPLE MATCHES"],
        ["bad", "Fields can be discovered in sibling records outside the producer-owned case scope."],
        ["bad", "Complete handoff would be possible only by crossing ownership boundaries."],
        ["info", "Selector containment rule engaged."],
        ["bad", "Named defect required before repair. Neighboring construction remains frozen."],
        ["bad", "OVERALL=FAIL_WITH_DEFECT"]
      ]
    },
    drift: {
      outcome: "QUARANTINE",
      tone: "warn",
      state: "QUARANTINE",
      lines: [
        ["info", "Loading expected lineage snapshot ... OK"],
        ["info", "Reading active source cursor ... CHANGED"],
        ["warn", "Source snapshot no longer matches the lineage receipt pinned by the handoff."],
        ["info", "Downstream release is withheld while drift is classified."],
        ["warn", "Object moved to quarantine path; frozen baseline remains untouched."],
        ["warn", "OVERALL=QUARANTINE"]
      ]
    }
  };

  const checksum = (text) => {
    let h1 = 0x811c9dc5;
    let h2 = 0x9e3779b1;
    for (let i = 0; i < text.length; i++) {
      const c = text.charCodeAt(i);
      h1 ^= c;
      h1 = Math.imul(h1, 0x01000193) >>> 0;
      h2 ^= (c + i) >>> 0;
      h2 = Math.imul(h2, 0x85ebca6b) >>> 0;
    }
    const a = h1.toString(16).padStart(8, "0");
    const b = h2.toString(16).padStart(8, "0");
    return `${a}${b}${a}${b}`.slice(0, 28);
  };

  const appendConsoleLine = (tone, text, idx) => {
    if (!consoleEl) return;
    const line = document.createElement("div");
    line.className = `console-line console-${tone}`;
    line.innerHTML = `<span>${String(idx).padStart(2, "0")}</span><p></p>`;
    qs("p", line).textContent = text;
    consoleEl.appendChild(line);
    consoleEl.scrollTop = consoleEl.scrollHeight;
  };

  const resetConsole = () => {
    if (!consoleEl) return;
    consoleEl.innerHTML = '<div class="console-line console-muted"><span>00</span><p>Ready. Select a scenario and run the integrity check.</p></div><div class="console-line console-muted"><span>01</span><p>No production systems are contacted by this demo.</p></div>';
    if (receipt) receipt.hidden = true;
    if (consoleState) consoleState.textContent = "IDLE";
    if (labRun) labRun.disabled = false;
  };

  if (labReset) labReset.addEventListener("click", resetConsole);

  if (labRun && consoleEl) {
    labRun.addEventListener("click", async () => {
      const selected = qs('input[name="scenario"]:checked');
      const key = selected?.value || "valid";
      const scenario = scenarioData[key];
      labRun.disabled = true;
      if (receipt) receipt.hidden = true;
      consoleEl.innerHTML = "";
      if (consoleState) consoleState.textContent = "RUNNING";

      appendConsoleLine("muted", `SCENARIO=${key.toUpperCase()}`, 0);
      let idx = 1;
      for (const [tone, text] of scenario.lines) {
        await sleep(reducedMotion ? 25 : 260 + (idx % 2) * 70);
        appendConsoleLine(tone, text, idx++);
      }

      const hash = checksum(`HYDRA:${key}:${scenario.outcome}:BASELINE_MUTATED=NO`);
      if (receiptOutcome) {
        receiptOutcome.textContent = scenario.outcome;
        receiptOutcome.style.color = scenario.tone === "good" ? "var(--green)" : scenario.tone === "bad" ? "var(--red)" : "var(--amber)";
      }
      if (receiptHash) receiptHash.textContent = hash;
      if (receipt) receipt.hidden = false;
      if (consoleState) consoleState.textContent = scenario.state;
      labRun.disabled = false;
    });
  }
})();
