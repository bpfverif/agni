/// Remove calls to reg_bounds_sync() and subfunctions. This is required in
/// modular mode during which these functions are verified separately. The
/// calls inside reg_bounds_sync() and reg_bounds_sync___() must be preserved
/// to be able to verify BPF_SYNC*.
// Confidence: Medium
// Comments:
// Options:

@rule1@
identifier fn != reg_bounds_sync___;
type T;
@@

T fn(...) {
<...
- reg_bounds_sync(...);
...>
}

@rule2@
identifier fn = adjust_scalar_min_max_vals;
type T;
@@

T fn(...) {
<...
(
- __update_reg_bounds(...);
|
- __reg_deduce_bounds(...);
|
- __reg_bound_offset(...);
)
...>
}
