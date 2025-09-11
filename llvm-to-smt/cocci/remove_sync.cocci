/// Remove calls to reg_bounds_sync(). This is required in modular mode during
/// which this function is verified separately. The calls inside
/// reg_bounds_sync___() must be preserved to be able to verify BPF_SYNC.
// Confidence: Medium
// Comments:
// Options:

@rule@
identifier fn != reg_bounds_sync___;
type T;
@@

T fn(...) {
<...
- reg_bounds_sync(...);
...>
}
