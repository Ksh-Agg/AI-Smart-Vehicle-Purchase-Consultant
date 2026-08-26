import type { Vehicle, UserPreferenceProfile, LangGraphNode } from '../types/agent';

export const INITIAL_VEHICLES: Vehicle[] = [
  {
    id: 'veh-1',
    make: 'Tesla',
    model: 'Model Y Long Range AWD',
    year: 2025,
    trim: 'Dual Motor AWD',
    price: 47990,
    powertrain: 'EV',
    epaMpgOrRange: '310 mi range (122 MPGe)',
    zeroToSixty: '4.8s',
    cargoVolumeCuFt: 76.2,
    safetyRatingStars: 5,
    nhtsaOverallScore: '5-Star Safety Award',
    matchScore: 96,
    imageUrl: 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1200&q=80',
    fuzzyMatchBreakdown: {
      budgetScore: 92,
      efficiencyScore: 98,
      spaceScore: 95,
      performanceScore: 97,
      safetyScore: 98,
    },
    pros: [
      'Top-tier Supercharger network access',
      'Massive 76.2 cu ft cargo capacity with sub-trunk',
      '5-Star crash protection & Autopilot safety suite',
      'Zero local emissions & low charging costs'
    ],
    cons: [
      'Minimalist cabin with screen-only controls',
      'Firmer suspension tuning over rough pavement'
    ],
    keyFeatures: ['Heat Pump 2.0', 'Autopilot Hardware 4', 'Glass Roof', 'AWD Dual Motor'],
    estimated5YearOwnershipCost: 49200,
  },
  {
    id: 'veh-2',
    make: 'Hyundai',
    model: 'Ioniq 5',
    year: 2025,
    trim: 'Limited AWD',
    price: 49850,
    powertrain: 'EV',
    epaMpgOrRange: '260 mi range (110 MPGe)',
    zeroToSixty: '4.5s',
    cargoVolumeCuFt: 59.3,
    safetyRatingStars: 5,
    nhtsaOverallScore: 'IIHS Top Safety Pick+',
    matchScore: 92,
    imageUrl: 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80',
    fuzzyMatchBreakdown: {
      budgetScore: 89,
      efficiencyScore: 94,
      spaceScore: 88,
      performanceScore: 96,
      safetyScore: 96,
    },
    pros: [
      'Ultra-fast 800V DC charging (10% to 80% in 18 mins)',
      'Retro-futuristic styling and ultra-quiet ride',
      'Vehicle-to-Load (V2L) 120V household outlets',
      'Spacious flat-floor interior lounge design'
    ],
    cons: [
      'Slightly lower cargo space behind 2nd row vs Model Y',
      'Rear wiper only standard on latest refreshes'
    ],
    keyFeatures: ['800V Architecture', 'Highway Driving Assist 2', 'V2L Power Outlets', 'Head-Up Display'],
    estimated5YearOwnershipCost: 51400,
  },
  {
    id: 'veh-3',
    make: 'Toyota',
    model: 'RAV4 Hybrid',
    year: 2025,
    trim: 'XSE Hybrid AWD',
    price: 38785,
    powertrain: 'Hybrid',
    epaMpgOrRange: '40 MPG Combined (580 mi range)',
    zeroToSixty: '7.1s',
    cargoVolumeCuFt: 69.8,
    safetyRatingStars: 5,
    nhtsaOverallScore: '5-Star Safety Rating',
    matchScore: 89,
    imageUrl: 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=1200&q=80',
    fuzzyMatchBreakdown: {
      budgetScore: 98,
      efficiencyScore: 90,
      spaceScore: 91,
      performanceScore: 78,
      safetyScore: 94,
    },
    pros: [
      'Exceptional proven reliability and resale value',
      '580-mile total road trip range without charging stops',
      'Low entry price well under budget ceiling',
      'Toyota Safety Sense 2.5 suite included standard'
    ],
    cons: [
      'Engine drone under heavy highway acceleration',
      'Infotainment UI is utilitarian compared to EVs'
    ],
    keyFeatures: ['Electronic On-Demand AWD', 'Toyota Safety Sense 2.5', 'Dual-Zone Climate', 'JBL Audio'],
    estimated5YearOwnershipCost: 44100,
  },
  {
    id: 'veh-4',
    make: 'Honda',
    model: 'CR-V Hybrid',
    year: 2025,
    trim: 'Sport Touring AWD',
    price: 41550,
    powertrain: 'Hybrid',
    epaMpgOrRange: '37 MPG Combined (518 mi range)',
    zeroToSixty: '7.4s',
    cargoVolumeCuFt: 76.5,
    safetyRatingStars: 5,
    nhtsaOverallScore: 'IIHS Top Safety Pick+',
    matchScore: 87,
    imageUrl: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80',
    fuzzyMatchBreakdown: {
      budgetScore: 95,
      efficiencyScore: 86,
      spaceScore: 96,
      performanceScore: 75,
      safetyScore: 95,
    },
    pros: [
      'Segment-leading cargo volume and wide tailgate opening',
      'Supple ride quality and upscale tactile switchgear',
      'Smooth transition between electric motor and gas engine'
    ],
    cons: [
      'No spare tire on hybrid trims',
      'Slightly lower fuel economy than RAV4 Hybrid'
    ],
    keyFeatures: ['Honda Sensing Suite', 'Bose Premium Audio', 'Hands-Free Power Tailgate', 'Wireless CarPlay'],
    estimated5YearOwnershipCost: 46800,
  },
  {
    id: 'veh-5',
    make: 'BMW',
    model: 'i4 eDrive40',
    year: 2025,
    trim: 'Gran Coupe M Sport',
    price: 57900,
    powertrain: 'EV',
    epaMpgOrRange: '301 mi range (109 MPGe)',
    zeroToSixty: '4.7s',
    cargoVolumeCuFt: 45.6,
    safetyRatingStars: 5,
    nhtsaOverallScore: 'Euro NCAP 5-Star',
    matchScore: 82,
    imageUrl: 'https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=80',
    fuzzyMatchBreakdown: {
      budgetScore: 71,
      efficiencyScore: 92,
      spaceScore: 74,
      performanceScore: 98,
      safetyScore: 93,
    },
    pros: [
      'Exceptional steering feel and authentic BMW dynamics',
      'Curved display with iDrive 8.5 system',
      'Practical liftback hatchback rear cargo door'
    ],
    cons: [
      'Higher base MSRP and expensive option packages',
      'Rear seat footroom constrained by transmission tunnel platform'
    ],
    keyFeatures: ['BMW Curved Display', 'Adaptive M Suspension', 'Driving Assistant Pro', 'Harman Kardon'],
    estimated5YearOwnershipCost: 61500,
  }
];

export const INITIAL_PREFERENCE_PROFILE: UserPreferenceProfile = {
  budgetMin: 35000,
  budgetMax: 50000,
  preferredPowertrains: ['EV', 'Hybrid'],
  seatingCapacity: 5,
  primaryUse: 'Family Roadtrips',
  priorities: {
    safety: 'High',
    fuelEconomy: 'High',
    cargoSpace: 'High',
    techFeatures: 'Medium',
    performance: 'Medium',
  },
};

export const INITIAL_LANGGRAPH_NODES: LangGraphNode[] = [
  {
    id: 'node-intake',
    name: 'questionnaire_intake',
    label: '1. Intake & Profile Parse',
    state: 'completed',
    description: 'Pydantic validation of budget constraints, fuel preferences, and cargo needs.',
    durationMs: 38,
    outputSummary: 'Parsed: Budget $35k-$50k, Powertrain=[EV, Hybrid], Priority=Safety+Cargo',
  },
  {
    id: 'node-catalogue',
    name: 'catalogue_query',
    label: '2. Catalogue Ingestion & SQL Query',
    state: 'completed',
    description: 'Filter PostgreSQL master vehicle catalogue with normalized specs.',
    durationMs: 84,
    outputSummary: 'Matched 14 vehicle trim variants within preliminary criteria.',
  },
  {
    id: 'node-fuzzy',
    name: 'fuzzy_logic_scoring',
    label: '3. Fuzzy Multi-Attribute Engine',
    state: 'completed',
    description: 'Min-max normalization, trapezoidal membership scoring for price & utility.',
    durationMs: 112,
    outputSummary: 'Scored 14 candidates across 5 weighted dimensions.',
  },
  {
    id: 'node-ranking',
    name: 'ranker_aggregator',
    label: '4. Dynamic Weight Ranker',
    state: 'completed',
    description: 'Multi-attribute matrix aggregation and top-k selection.',
    durationMs: 42,
    outputSummary: 'Top 5 ranked vehicles identified (Score 96% -> 82%).',
  },
  {
    id: 'node-explainer',
    name: 'llm_explanation_layer',
    label: '5. LLM Synthesis & Explanation',
    state: 'completed',
    description: 'Synthesizes tradeoff rationales, pros/cons, and customized purchase summary.',
    durationMs: 320,
    outputSummary: 'Generated purchase advisory narrative and HITL approval suggestion.',
  },
];

// ponytail: simulated stream generator for LangGraph SSE events until FastAPI endpoint is attached.
// Upgrade path: replace generator with EventSource / fetchEventSource in live integration.
export async function* simulateLangGraphConsultationStream(prompt: string) {
  // 1. Initial thinking start
  yield {
    type: 'on_chain_start',
    nodeId: 'node-intake',
    thought: `Analyzing consultation query: "${prompt}". Validating preference bounds against user profile...`
  };

  await new Promise(r => setTimeout(r, 450));

  yield {
    type: 'on_thinking_step',
    thought: 'Identified key requirements: Budget ceiling $50,000, 5-passenger seating, preference for electrified powertrains (EV & Hybrid) with high safety rating.'
  };

  await new Promise(r => setTimeout(r, 400));

  // 2. Tool call: Catalogue Query
  yield {
    type: 'on_tool_start',
    tool: {
      id: `tool-${Date.now()}-1`,
      toolName: 'query_vehicle_catalogue',
      label: 'Query Master Vehicle Catalogue (PostgreSQL)',
      status: 'running' as const,
      inputParams: {
        budget_range: [35000, 50000],
        powertrain_filter: ['EV', 'Hybrid'],
        min_safety_stars: 5,
      }
    }
  };

  await new Promise(r => setTimeout(r, 600));

  yield {
    type: 'on_tool_end',
    toolId: `tool-${Date.now()}-1`,
    outputResult: {
      records_scanned: 48,
      candidates_matched: 5,
      applied_filters: 'budget <= 50000 AND safety_stars >= 5',
    },
    executionTimeMs: 142,
  };

  // 3. Tool call: Fuzzy Engine
  yield {
    type: 'on_tool_start',
    tool: {
      id: `tool-${Date.now()}-2`,
      toolName: 'calculate_fuzzy_preference_scores',
      label: 'Fuzzy Logic & Multi-Attribute Weight Engine',
      status: 'running' as const,
      inputParams: {
        weight_safety: 0.35,
        weight_cargo: 0.25,
        weight_efficiency: 0.20,
        weight_budget: 0.20,
      }
    }
  };

  await new Promise(r => setTimeout(r, 550));

  yield {
    type: 'on_tool_end',
    toolId: `tool-${Date.now()}-2`,
    outputResult: {
      ranked_candidate_ids: ['veh-1', 'veh-2', 'veh-3', 'veh-4', 'veh-5'],
      top_score: 96,
      top_candidate: 'Tesla Model Y Long Range AWD',
    },
    executionTimeMs: 98,
  };

  // 4. HITL Approval Request
  yield {
    type: 'on_interrupt',
    approval: {
      id: `approval-${Date.now()}`,
      title: 'Suggested Criteria Optimization: EV Tax Credit & Budget Ceiling',
      description: 'The Tesla Model Y Long Range ($47,990) qualifies for the $7,500 Federal EV Tax Credit at point-of-sale, effectively lowering net vehicle cost to $40,490. Would you like me to factor federal & state incentives into the total ownership calculation?',
      type: 'budget_increase' as const,
      payload: {
        suggestedBudgetDelta: -7500,
        relaxedConstraint: 'Include point-of-sale Federal Clean Vehicle Credit',
        tradeoffSummary: 'Lowers effective purchase price below RAV4 Hybrid while unlocking superior EV acceleration and cargo volume.',
      },
      status: 'pending' as const,
    }
  };

  await new Promise(r => setTimeout(r, 350));

  // 5. Streaming chat response tokens
  const fullText = `Based on your criteria for high safety, family road trip capability, and electrified efficiency, here is your customized vehicle recommendation overview:

1. **Tesla Model Y Long Range AWD (96% Match)** — **Top Pick**. Offers class-leading 76.2 cu ft cargo capacity, standard 5-star crash safety, and seamless Supercharger road trip routing. At $47,990, it fits within your $50k ceiling.
2. **Hyundai Ioniq 5 Limited (92% Match)** — Outstanding 800V DC fast-charging (10-80% in 18 mins), whisper-quiet ride, and V2L household power output for camping gear.
3. **Toyota RAV4 Hybrid XSE (89% Match)** — The road trip endurance champion with 580 miles of gas-hybrid range and bulletproof resale value.

I have loaded the comparative specification cards and 5-year cost breakdown into your **Inspector Canvas** on the right. Would you like me to deep dive into battery degradation warranties or compare insurance tiers for these models?`;

  const chunks = fullText.split(' ');
  for (let i = 0; i < chunks.length; i += 3) {
    const token = chunks.slice(i, i + 3).join(' ') + ' ';
    yield {
      type: 'on_chat_model_stream',
      token,
      vehicles: INITIAL_VEHICLES,
    };
    await new Promise(r => setTimeout(r, 45));
  }

  yield {
    type: 'on_chain_end',
    completedNodeId: 'node-explainer',
  };
}
