# Sketchpad
A constraint-based geometry sketching tool.

Sketchpad allows drawing by specifying nothing but _constraints_. "These two segments are end-to-end and perpendicular; this segment is tangent to this arc," and so on. Sketchpad uses the powerful [Z3 Theorem Prover](https://github.com/Z3Prover/z3) to solve the analytic geometry problem presented by the constraints you specify. The output drawing is an exact algebraic solution to your set of constraints. Don't like where some element ended up? It's because your sketch was underspecified :D 

Sketchpad can find every degree-of-freedom in your sketch---even ones Newtonian method solvers would miss!
