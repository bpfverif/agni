@remove_same_reg_branch@
identifier fn = is_scalar_branch_taken;
@@

fn(...) {
<...
-	if (reg1 == reg2) { ... }
...>
}

@remove_same_reg_skip_refine@
identifier fn = reg_set_min_max;
@@

fn(...) {
<...
-	if (false_reg1 == false_reg2)
-		return 0;
...>
}