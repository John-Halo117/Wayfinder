# Sanctuary Anti-Pattern & Failure-Mode Canon

Status: canonical negative specification for Sanctuary physical design.

Purpose: reject locally clever, efficient, modular, secure, multifunctional, or space-saving ideas when their displaced burden makes the whole habitat more expensive, fragile, annoying, illegible, unsafe, inaccessible, or permanently complex.

## Governing rejection laws

> A local optimization is invalid when its displaced burden exceeds its recovered value.

> Capability that is technically present but too annoying, fragile, inaccessible, unsafe, illegible, or confusing to use is not real capability.

The positive spatial-capability compiler and this inverse compiler are both required. Passing one does not waive the other.

## Universal inverse compiler

For every candidate feature or mechanism ask, in order:

1. What state are we actually trying to create?
2. Is this a requirement or merely a cool implementation?
3. What existing capability already satisfies it?
4. What permanent obligation does this add?
5. What failure modes does it introduce?
6. Where does displaced burden move?
7. What deploy/reset/maintenance/cleaning burden appears?
8. What happens if power, network, motor, controller, cloud, or vendor fails?
9. Can it be inspected, cleaned, repaired, isolated, and replaced?
10. Does it damage calm, accessibility, security, water control, fire protection, acoustics, serviceability, or privacy?
11. Is there a simpler static/manual solution?
12. Is there a boring mature standard solution?
13. Does the claimed saving survive whole-system recompilation?
14. Would the design still be chosen after novelty wears off?

Disposition:

- **BUILD** — survives requirements, whole-system recompilation, and failure review.
- **DEFER** — useful candidate, not yet justified.
- **RESERVE / PROBE** — uncertainty remains and cheap reversible preservation/probing has option value.
- **PRUNE** — fails the negative specification or is dominated by a simpler adequate alternative.

## 1. Spatial

Reject by default:

- **Room-first design** — named activity automatically becomes a dedicated room. Descend through slot -> pocket -> niche -> cubby -> passage -> nook -> alcove -> zone -> room, subject to the active GH/MH profile.
- **Maximum-utilization syndrome** — every cubic foot is filled. Negative space, circulation slack, staging capacity, accessibility, visual calm, and future option value are legitimate uses.
- **Transformer-house syndrome** — ordinary living requires repeated folding, rotating, sliding, retracting, or converting. Transformation is for intermittent capability, not basic existence.
- **Conversion tax** — multifunctionality claims ignore deploy time, reset time, object moves, search, and decisions.
- **Spatial double booking** — two functions claim one volume despite material simultaneous demand.
- **Geometry worship** — a favorite grid/curve/module/shape dictates loads, rooms, furniture, or structure without requirement support.

## 2. Intelligent hollowing

Reject by default:

- **Hollow everything** — material removal becomes an objective instead of removing only useless solid.
- **Empty = available** — drainage, fire, acoustic, thermal, equipment, service, or clearance voids are harvested despite already doing work.
- **Swiss-cheese structure** — repeated local penetrations accumulate into weakening, leakage, reinforcement, and documentation burden.
- **Expensive void in cheap material** — fabrication/engineering complexity exceeds material and propagated savings.
- **Inaccessible hollow** — cavity-mounted equipment lacks inspection/removal/service access; that is a tomb, not a service cavity.
- **Pest hotel** — hollows lack exclusion, inspection, drainage, and cleaning topology.

## 3. Productive boundaries

Reject by default:

- **Wall as junk drawer** — storage, utilities, controls, pet routes, ducts, lighting, and mechanisms congest one boundary without independent serviceability.
- **Sacred-waterproofing penetration** — optional capability penetrates a critical water-control boundary without necessity and qualified detailing.
- **Boundary overloading** — secondary functions compromise the primary boundary duty or replacement path.
- **Hidden everything** — visual calm becomes concealment fetishism. Frequently used, emergency, control, and service functions remain legible at the appropriate disclosure level.

## 4. Vertical volume

Reject by default:

- **Stool architecture** — frequently used objects require a stool or awkward reach.
- **Ceiling warehouse** — overhead storage becomes default and creates retrieval, risk, visual, or mechanism burden.
- **Mechanized Christmas decorations** — expensive access machinery serves very-low-frequency storage.
- **Heavy-high storage** — high mass + high elevation + frequent manipulation without a genuine handling system.

## 5. Interfaces

Reject by default:

- **Universal-interface delusion** — one interface is forced to serve every payload and becomes oversized/mediocre.
- **Proprietary house** — permanent architecture depends unnecessarily on one vendor ecosystem. Prefer applicable standard -> open/mature interoperable interface -> commodity interface -> justified custom residual.
- **Interface without payload** — expensive speculative hardware is installed merely because future use is imaginable. Cheap geometry/routes/reserve may be preserved instead.
- **Payload dictates skeleton** — short-lived replaceable equipment determines permanent building geometry without a durable requirement.
- **False compatibility** — physical fit is treated as proof of load, electrical/fluid/data, authority, or safe-use compatibility.

## 6. Deployables

Reject by default:

- **No park state** — deployable equipment has nowhere practical to live.
- **Reset debt** — recurring use leaves cleanup/cables/hardware/components that accumulate into permanent disorder.
- **Deployment cascade** — using A requires moving B which requires moving C.
- **Powered because cool** — motors/software substitute for adequate passive/manual mechanisms without material benefit.
- **Motorized necessity** — a consequential capability loses availability during power/control failure when a practical manual/local fallback could exist.

## 7. Foundation

Reject by default:

- **Concrete-minimization theater** — lower concrete volume is celebrated while installed/lifecycle cost rises.
- **Wafflemat religion** — one foundation technology becomes the requirement instead of remaining a challenger against boring adequate systems for the actual site.
- **Bad-land technology subsidy** — advanced foundations rationalize a parcel whose geotechnical burden was cheaper to avoid during land selection.
- **Uniform three-foot bathtub** — nominal earth coupling becomes uniform unnecessary excavation/retaining despite topography.
- **Foundation-as-basement creep** — shallow earth-contact construction accumulates basement-level complexity without basement capability.
- **Retaining-wall proliferation** — architectural landscaping creates avoidable additional retaining systems instead of first using siting/grading.
- **Slab tomb** — short-lived/serviceable systems are buried in permanent concrete without lifecycle justification.

## 8. Earthwork

Reject by default:

- **Dirt ping-pong** — useful excavated material leaves, then equivalent material is repurchased and returned.
- **Zero-export dogma** — unsuitable material is retained/reused merely to satisfy a no-export slogan.
- **Sculpt-the-world syndrome** — heavy earthmoving forces terrain to accommodate a predetermined building when relocation could remove the burden.
- **Equipment-mobilization amnesia** — compatible earthwork is split across repeated avoidable mobilizations.

## 9. Water

Reject by default:

- **Membrane heroism** — exceptional waterproofing compensates for poor bulk-water routing. Preferred order: intercept -> shed -> route -> drain -> waterproof.
- **Sump dependency by design** — permanent pumping replaces feasible gravity drainage.
- **Landscape-hydrology collision** — swales, ponds, irrigation, rain gardens, etc. compromise structural drainage. Maintain the dry structural island.
- **Roof-to-foundation pipeline** — roof drainage discharges beside earth-contact structure.
- **Drain without destination** — drainage is installed without a proven receiving path/outfall/infiltration strategy.

## 10. Utilities

Reject by default:

- **Penetration confetti** — each trade independently penetrates the envelope instead of using qualified service portals/zones where appropriate.
- **Utility spaghetti** — individually shortest runs create an illegible aggregate topology.
- **Manifold burial** — serviceable components disappear behind finish.
- **Spare-conduit mania** — speculative conduit count substitutes for cheap route/access reserve.
- **Smart plumbing** — simple infrastructure gains networked sensing/actuation without consequential benefit.

## 11. Floors

Reject by default:

- **Floor lasagna** — independently chosen layers create redundant structure/leveling/underlayment/finish/rug burden.
- **Polished-concrete cost trap** — deleting finish flooring mutates into a premium polishing package with higher cost/burden.
- **Access-panel checkerboard** — serviceability becomes panels everywhere instead of concentrated access topology.
- **Floor-grid dictatorship** — structural coordinates unnecessarily constrain furniture/room life.

## 12. Walls

Reject by default:

- **Double wall for no reason** — structure + service + decorative layers survive despite combinable functions.
- **Stud-finder dependency** — every future attachment requires rediscovering hidden structure where strategic qualified mounting zones would materially help.
- **Industrial-rail everywhere** — solving stud-finder dependency turns every occupied wall into exposed industrial infrastructure.
- **Permanent built-in everything** — furniture clutter is merely exchanged for architectural rigidity.
- **Acoustic hollowing failure** — harvested cavities meet structure but destroy acoustic performance.

## 13. Ceilings

Reject by default:

- **Ceiling gadget forest** — capability density becomes visual/perceptual density.
- **Hex-light everywhere** — workshop aesthetics leak into restorative spaces without purpose.
- **Inaccessible service plenum** — infrastructure is concealed but not actually reachable.
- **Falling-payload architecture** — overhead convenience outranks qualified load/dynamic/human-use requirements.

## 14. Pet architecture

Reject by default:

- **Catification everywhere** — every wall becomes animal equipment; animal capability does not require visual saturation.
- **Cat highway through human headspace** — independent circulation creates human conflicts.
- **Uncleanable pet void** — animal routes cannot be inspected/cleaned.
- **Animal escape graph** — pet circulation unintentionally traverses controlled exterior/service/security boundaries.

## 15. Robots / machines

Reject by default:

- **Robot tax** — human geometry becomes worse solely for one current robot when accommodation is not nearly free.
- **Proprietary robot architecture** — permanent building features depend on today's robot dimensions/protocols.
- **Autonomous-authority creep** — reachability or navigation ability is mistaken for authority to operate.

## 16. Progressive disclosure

Reject by default:

- **Puzzle house** — residents forget capabilities because discovery overwhelms retrieval.
- **Secret-door theme park** — concealment becomes the aesthetic objective.
- **Cleverness tax** — guests need tutorials for ordinary faucets, toilets, lights, doors, or equivalent L0/L1 functions.
- **Invisible emergency function** — emergency equipment/controls are too hidden to find under stress.

## 17. Zero-trust / security

Reject by default:

- **Security through obscurity** — hidden existence substitutes for actual authority/control.
- **Fortification theater** — visible security harms ordinary resident life without commensurate risk reduction.
- **Authentication everywhere** — low-consequence ordinary actions require needless identity checks.
- **Smart-lock dependency cascade** — network/cloud/controller failure blocks ordinary physical access without robust local/manual path.
- **Contractor superuser** — service personnel receive broad authority because scoped service access was not designed.

## 18. Modularity

Reject by default:

- **LEGO-house syndrome** — everything becomes modular merely because modularity sounds future-proof.
- **Module proliferation** — many slightly different interface standards defeat standardization.
- **Premature standardization** — unresolved dimensions are frozen before requirements stabilize.
- **Lowest-common-denominator module** — specialization is destroyed merely to achieve nominal interchangeability.

## 19. Resilience

Reject by default:

- **Backup everything** — redundancy is installed independent of failure consequence, probability, and recovery time.
- **Off-grid cosplay** — expensive independence duplicates reliable infrastructure without enough resilience value.
- **Automation masquerading as resilience** — more controllers/batteries/software are assumed inherently more resilient than simple passive/manual fallback.
- **Backup without exercise** — redundancy exists on paper but has not been tested/rehearsed.

## 20. Accessibility

Reject by default:

- **Accessibility as add-on** — accessible routes/reach/control are patched after geometry is fixed.
- **Mechanism replaces reachability** — frequently needed items are inherently inaccessible and become usable only while a mechanism works.
- **Universal design = institutional design** — accessibility is allowed to dictate an unnecessarily institutional aesthetic.

## 21. Maintenance

Reject by default:

- **Maintenance-free claim** — lifecycle burden is assumed absent.
- **Finish before service** — finish quality blocks access to consequential infrastructure.
- **Specialized-tool dependency** — routine service requires proprietary/specialty tooling without strong justification.
- **Documentation cemetery** — as-built/service documentation exists but cannot be found at the point of need.

## 22. Cost

Reject by default:

- **Feature-level ROI** — every component claims to pay for itself while aggregate house complexity/capital exceeds the objective.
- **Material-cost myopia** — low material price creates high labor/installation/lifecycle cost.
- **DIY fantasy pricing** — user labor, tools, mistakes, mobilization, schedule, and rework are priced at zero.
- **Savings migration** — one subsystem claims savings while costs reappear in another; propagate claimed savings through the dependency DAG.
- **Percentage seduction** — percentage reduction in concrete/material/energy/etc. is presented without final-dollar/whole-system consequence.

## 23. Future proofing

Reject by default:

- **Future-proof everything** — speculative current hardware is installed as a guess at future technology. Prefer cheap space + route + access + power + applicable standard interface.
- **Infinite reserve** — large unused service volume is justified as optionality without pricing it.
- **Frozen future** — assemblies are optimized so tightly that ordinary adaptation requires demolition even when cheap reserve geometry was available.

## 24. Meta anti-patterns

These generate many of the others and receive priority review:

- **Cleverness seeking** — “can we?” silently replaces “should we?”.
- **Mechanism promotion** — a candidate implementation becomes the requirement.
- **Local optimization** — one subsystem improves while the parent/house gets worse. Recompile parents.
- **Metric substitution** — concrete volume, ft² efficiency, storage density, R-value, automation count, material utilization, or capability count replaces the actual lived objective.
- **Complexity ratchet** — additions receive a lower burden of proof than deletions.
- **Novelty ratchet** — new technology remains in competition while boring baselines quietly disappear. Keep the boring baseline.
- **Optimization without stop condition** — optimization continues after marginal value is below money/cognition/fragility/option burden.
- **Architecture for the diagram** — a design is elegant in Polaris but unpleasant in reality. Reality has veto authority.

## Whole-system burden dimensions

No universal score is required. Preserve independent material dimensions where they can change the decision:

- capital / installed cost
- labor and mobilization
- permanent spatial obligation
- visual/perceptual burden
- deployment/reset/search burden
- maintenance/cleaning/service burden
- failure consequence and recovery time
- accessibility/reachability
- water/fire/acoustic/structural consequences
- vendor/software/power/network dependence
- privacy/security/authority consequences
- lifecycle replacement burden
- option value and reversibility
- evidence/confidence

A candidate survives only if its claimed benefit remains material after displaced burdens are propagated through affected parents.

## Complementary Sanctuary law

The house is allowed to become *less* in order to become more capable:

less unnecessary concrete, wall, buried infrastructure, dedicated space, proprietary hardware, maintenance, choreography, and visual noise.

More capability is admitted only when that capability survives the inverse compiler.
