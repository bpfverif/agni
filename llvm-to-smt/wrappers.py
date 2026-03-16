
wrapper_fls = r"""

// https://elixir.bootlin.com/linux/v6.10/source/include/asm-generic/bitops/fls.h#L43
static int generic_fls___(unsigned int x)
{
	int r = 32;

	if (!x)
		return 0;
	if (!(x & 0xffff0000u)) {
		x <<= 16;
		r -= 16;
	}
	if (!(x & 0xff000000u)) {
		x <<= 8;
		r -= 8;
	}
	if (!(x & 0xf0000000u)) {
		x <<= 4;
		r -= 4;
	}
	if (!(x & 0xc0000000u)) {
		x <<= 2;
		r -= 2;
	}
	if (!(x & 0x80000000u)) {
		x <<= 1;
		r -= 1;
	}
	return r;
}

#define fls___(x) generic_fls___(x)

// https://elixir.bootlin.com/linux/v6.10/source/include/asm-generic/bitops/__fls.h#L45
static unsigned int generic___fls___(unsigned long word)
{
	unsigned int num = BITS_PER_LONG - 1;

#if BITS_PER_LONG == 64
	if (!(word & (~0ul << 32))) {
		num -= 32;
		word <<= 32;
	}
#endif
	if (!(word & (~0ul << (BITS_PER_LONG-16)))) {
		num -= 16;
		word <<= 16;
	}
	if (!(word & (~0ul << (BITS_PER_LONG-8)))) {
		num -= 8;
		word <<= 8;
	}
	if (!(word & (~0ul << (BITS_PER_LONG-4)))) {
		num -= 4;
		word <<= 4;
	}
	if (!(word & (~0ul << (BITS_PER_LONG-2)))) {
		num -= 2;
		word <<= 2;
	}
	if (!(word & (~0ul << (BITS_PER_LONG-1))))
		num -= 1;
	return num;
}

#define __fls___(word) generic___fls___(word)

// https://elixir.bootlin.com/linux/v6.10/source/include/asm-generic/bitops/fls64.h#L19
#if BITS_PER_LONG == 32
static int fls64___(__u64 x)
{
	__u32 h = x >> 32;
	if (h)
		return fls___(h) + 32;
	return fls___(x);
}
#elif BITS_PER_LONG == 64
static int fls64___(__u64 x)
{
	if (x == 0)
		return 0;
	return __fls___(x) + 1;
}
#endif

"""

wrapper_unknown = r'''

static void mark_reg_unknown___(struct bpf_reg_state *reg)
{
	reg->type = SCALAR_VALUE;
	reg->var_off = tnum_unknown;
	__mark_reg_unbounded(reg);
}

'''

wrapper_push_stack_no32 = r'''

static void push_stack___(struct bpf_reg_state* to, struct bpf_reg_state* from){
    to->type = from->type;
	to->var_off.value = from->var_off.value;
	to->var_off.mask = from->var_off.mask;
	to->smin_value = from->smin_value;
	to->smax_value = from->smax_value;
	to->umin_value = from->umin_value;
	to->umax_value = from->umax_value;
}

'''

wrapper_push_stack_w32 = r'''

static void push_stack___(struct bpf_reg_state* to, struct bpf_reg_state* from){
    to->type = from->type;
	to->var_off.value = from->var_off.value;
	to->var_off.mask = from->var_off.mask;
	to->smin_value = from->smin_value;
	to->smax_value = from->smax_value;
	to->umin_value = from->umin_value;
	to->umax_value = from->umax_value;
	to->s32_min_value = from->s32_min_value;
	to->s32_max_value = from->s32_max_value;
	to->u32_min_value = from->u32_min_value;
	to->u32_max_value = from->u32_max_value;
}

'''

wrapper_alu_1 = """

void adjust_scalar_min_max_vals_wrapper_{}(struct bpf_reg_state *dst_reg,
					struct bpf_reg_state *src_reg)
{{
	struct bpf_verifier_env env;
	struct bpf_insn insn = BPF_ALU64_REG({}, BPF_REG_1, BPF_REG_2);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	adjust_scalar_min_max_vals(&env, &insn, dst_reg, *src_reg);

}}
"""

wrapper_alu32_1 = wrapper_alu_1.replace("BPF_ALU64_REG", "BPF_ALU32_REG")


# 5.3-rc1 to 5.7-rc1
wrapper_jmp_4 = '''

void check_cond_jmp_op_wrapper_{}(struct bpf_reg_state *dst_reg,
			       struct bpf_reg_state *src_reg,
			       struct bpf_reg_state *other_branch_dst_reg,
			       struct bpf_reg_state *other_branch_src_reg)
{{
	struct bpf_insn insn;
	u8 opcode;
	bool is_jmp32;
	int pred = -1;

	/* Set BPF insn */
	insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	opcode = BPF_OP(insn.code);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	/* Perform custom push_stack to make sure we have don't have garbage values 
	for other_branch_regs in case pred != -1 */
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

	/* Kernel copy-pasted code begins */
	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;

	if (BPF_SRC(insn.code) == BPF_K)
		pred = is_branch_taken(dst_reg, insn.imm,
				       opcode, is_jmp32);
	else if (src_reg->type == SCALAR_VALUE &&
		 tnum_is_const(src_reg->var_off))
		pred = is_branch_taken(dst_reg, src_reg->var_off.value,
				       opcode, is_jmp32);

	if (pred == 1) {{
		return;
	}} else if (pred == 0) {{
		return;
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		struct bpf_reg_state lo_reg0 = *dst_reg;
		struct bpf_reg_state lo_reg1 = *src_reg;
		struct bpf_reg_state *src_lo, *dst_lo;

		dst_lo = &lo_reg0;
		src_lo = &lo_reg1;
		coerce_reg_to_size(dst_lo, 4);
		coerce_reg_to_size(src_lo, 4);

		if (dst_reg->type == SCALAR_VALUE &&
		    src_reg->type == SCALAR_VALUE) {{
			if (tnum_is_const(src_reg->var_off) ||
			    (is_jmp32 && tnum_is_const(src_lo->var_off)))
				reg_set_min_max(other_branch_dst_reg,
						dst_reg,
						is_jmp32
						? src_lo->var_off.value
						: src_reg->var_off.value,
						opcode, is_jmp32);
			else if (tnum_is_const(dst_reg->var_off) ||
				 (is_jmp32 && tnum_is_const(dst_lo->var_off)))
				reg_set_min_max_inv(other_branch_src_reg,
						    src_reg,
						    is_jmp32
						    ? dst_lo->var_off.value
						    : dst_reg->var_off.value,
						    opcode, is_jmp32);
			else if (!is_jmp32 &&
				 (opcode == BPF_JEQ || opcode == BPF_JNE))
				reg_combine_min_max(other_branch_src_reg,
						    other_branch_dst_reg,
						    src_reg, dst_reg, opcode);
		}}
	}} else if (dst_reg->type == SCALAR_VALUE) {{
		reg_set_min_max(other_branch_dst_reg,
					dst_reg, insn.imm, opcode, is_jmp32);
	}}

}}

'''

wrapper_jmp32_4 = wrapper_jmp_4.replace("BPF_JMP_REG", "BPF_JMP32_REG")

# 5.7-rc1+
wrapper_jmp_5 = '''

void check_cond_jmp_op_wrapper_{}(struct bpf_reg_state *dst_reg,
			       struct bpf_reg_state *src_reg,
			       struct bpf_reg_state *other_branch_dst_reg,
			       struct bpf_reg_state *other_branch_src_reg)
{{
	/* Setup */
	struct bpf_insn insn;
	u8 opcode;
	bool is_jmp32;
	int pred = -1;

	insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	opcode = BPF_OP(insn.code);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	/* Perform custom push_stack to make sure we have don't have garbage values 
	for other_branch_regs in case pred != -1 */
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

	/* Kernel copy-pasted code begins */
	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;

	if (BPF_SRC(insn.code) == BPF_K) {{
		pred = is_branch_taken(dst_reg, insn.imm, opcode, is_jmp32);
	}} else if (src_reg->type == SCALAR_VALUE &&
		   is_jmp32 && tnum_is_const(tnum_subreg(src_reg->var_off))) {{
		pred = is_branch_taken(dst_reg,
				       tnum_subreg(src_reg->var_off).value,
				       opcode,
				       is_jmp32);
	}} else if (src_reg->type == SCALAR_VALUE &&
		   !is_jmp32 && tnum_is_const(src_reg->var_off)) {{
		pred = is_branch_taken(dst_reg,
				       src_reg->var_off.value,
				       opcode,
				       is_jmp32);
	}}

	if (pred == 1) {{
		return;
	}} else if (pred == 0) {{
		return;
	}}


	if (BPF_SRC(insn.code) == BPF_X) {{
		if (dst_reg->type == SCALAR_VALUE &&
		    src_reg->type == SCALAR_VALUE) {{
			if (tnum_is_const(src_reg->var_off) ||
			    (is_jmp32 &&
			     tnum_is_const(tnum_subreg(src_reg->var_off))))
				reg_set_min_max(
					other_branch_dst_reg, dst_reg,
					src_reg->var_off.value,
					tnum_subreg(src_reg->var_off).value,
					opcode, is_jmp32);
			else if (tnum_is_const(dst_reg->var_off) ||
				 (is_jmp32 &&
				  tnum_is_const(tnum_subreg(dst_reg->var_off))))
				reg_set_min_max_inv(
					other_branch_src_reg, src_reg,
					dst_reg->var_off.value,
					tnum_subreg(dst_reg->var_off).value,
					opcode, is_jmp32);
			else if (!is_jmp32 &&
				 (opcode == BPF_JEQ || opcode == BPF_JNE))
				/* Comparing for equality, we can combine knowledge */
				reg_combine_min_max(other_branch_src_reg,
						    other_branch_dst_reg,
						    src_reg, dst_reg, opcode);
		}}
	}} else if (dst_reg->type == SCALAR_VALUE) {{
		reg_set_min_max(other_branch_dst_reg, dst_reg, insn.imm,
				(u32)insn.imm, opcode, is_jmp32);
	}}
}}

'''

wrapper_jmp32_5 = wrapper_jmp_5.replace("BPF_JMP_REG", "BPF_JMP32_REG")

# 6.4-rc1+
wrapper_jmp_6 = '''

void check_cond_jmp_op_wrapper_{}(struct bpf_reg_state *dst_reg,
			       struct bpf_reg_state *src_reg,
			       struct bpf_reg_state *other_branch_dst_reg,
			       struct bpf_reg_state *other_branch_src_reg)
{{
	/* Setup */
	struct bpf_insn insn;
	u8 opcode;
	bool is_jmp32;
	int pred = -1;

	insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	opcode = BPF_OP(insn.code);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	/* Perform custom push_stack to make sure we have don't have garbage values
	 * for other_branch_regs in case pred != -1
	 */
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

	/* Kernel copy-pasted code begins */
	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;

	if (BPF_SRC(insn.code) == BPF_K) {{
		pred = is_branch_taken(dst_reg, insn.imm, opcode, is_jmp32);
	}} else if (src_reg->type == SCALAR_VALUE &&
		   is_jmp32 && tnum_is_const(tnum_subreg(src_reg->var_off))) {{
		pred = is_branch_taken(dst_reg,
				       tnum_subreg(src_reg->var_off).value,
				       opcode,
				       is_jmp32);
	}} else if (src_reg->type == SCALAR_VALUE &&
		   !is_jmp32 && tnum_is_const(src_reg->var_off)) {{
		pred = is_branch_taken(dst_reg,
				       src_reg->var_off.value,
				       opcode,
				       is_jmp32);
	}} else if (dst_reg->type == SCALAR_VALUE &&
		   is_jmp32 && tnum_is_const(tnum_subreg(dst_reg->var_off))) {{
		pred = is_branch_taken(src_reg,
				       tnum_subreg(dst_reg->var_off).value,
				       flip_opcode(opcode),
				       is_jmp32);
	}} else if (dst_reg->type == SCALAR_VALUE &&
		   !is_jmp32 && tnum_is_const(dst_reg->var_off)) {{
		pred = is_branch_taken(src_reg,
				       dst_reg->var_off.value,
				       flip_opcode(opcode),
				       is_jmp32);
	}}

	if (pred == 1) {{
		return;
	}} else if (pred == 0) {{
		return;
	}}


	if (BPF_SRC(insn.code) == BPF_X) {{
		if (dst_reg->type == SCALAR_VALUE &&
		    src_reg->type == SCALAR_VALUE) {{
			if (tnum_is_const(src_reg->var_off) ||
			    (is_jmp32 &&
			     tnum_is_const(tnum_subreg(src_reg->var_off))))
				reg_set_min_max(
					other_branch_dst_reg, dst_reg,
					src_reg->var_off.value,
					tnum_subreg(src_reg->var_off).value,
					opcode, is_jmp32);
			else if (tnum_is_const(dst_reg->var_off) ||
				 (is_jmp32 &&
				  tnum_is_const(tnum_subreg(dst_reg->var_off))))
				reg_set_min_max_inv(
					other_branch_src_reg, src_reg,
					dst_reg->var_off.value,
					tnum_subreg(dst_reg->var_off).value,
					opcode, is_jmp32);
			else if (!is_jmp32 &&
				 (opcode == BPF_JEQ || opcode == BPF_JNE))
				/* Comparing for equality, we can combine knowledge */
				reg_combine_min_max(other_branch_src_reg,
						    other_branch_dst_reg,
						    src_reg, dst_reg, opcode);
		}}
	}} else if (dst_reg->type == SCALAR_VALUE) {{
		reg_set_min_max(other_branch_dst_reg, dst_reg, insn.imm,
				(u32)insn.imm, opcode, is_jmp32);
	}}
}}

'''

wrapper_jmp32_6 = wrapper_jmp_6.replace("BPF_JMP_REG", "BPF_JMP32_REG")

# Andrii's patchset cd9c127069c0
wrapper_jmp_cd9c127069c0 = '''

void check_cond_jmp_op_wrapper_{}(struct bpf_reg_state *dst_reg,
			       struct bpf_reg_state *src_reg,
			       struct bpf_reg_state *other_branch_dst_reg,
			       struct bpf_reg_state *other_branch_src_reg)
{{
	/* Setup */
	struct bpf_insn insn;
	u8 opcode;
	bool is_jmp32;
	int pred = -1;

	insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	opcode = BPF_OP(insn.code);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	/* Perform custom push_stack to make sure we have don't have garbage values
	 * for other_branch_regs in case pred != -1
	 */
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

	/* Kernel copy-pasted code begins */
	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;
	pred = is_branch_taken(dst_reg, src_reg, opcode, is_jmp32);

	if (pred == 1) {{
		return;
	}} else if (pred == 0) {{
		return;
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		reg_set_min_max(other_branch_dst_reg,
				other_branch_src_reg,
				dst_reg, src_reg, opcode, is_jmp32);

		if (!is_jmp32 && (opcode == BPF_JEQ || opcode == BPF_JNE)) {{
			/* Comparing for equality, we can combine knowledge */
			reg_combine_min_max(other_branch_dst_reg,
				other_branch_dst_reg,
				src_reg, dst_reg, opcode);
		}}
	}} else /* BPF_SRC(insn.code) == BPF_K */ {{
		reg_combine_min_max(other_branch_src_reg,
			other_branch_dst_reg,
			src_reg, dst_reg, opcode);
	}}

}}
'''

wrapper_jmp32_cd9c127069c0 = wrapper_jmp_cd9c127069c0.replace(
    "BPF_JMP_REG", "BPF_JMP32_REG")

# v6.8-rc1+
wrapper_jmp_7 = '''
void check_cond_jmp_op_wrapper_{}(
	struct bpf_reg_state *dst_reg, struct bpf_reg_state *src_reg,
	struct bpf_reg_state *other_branch_dst_reg,
	struct bpf_reg_state *other_branch_src_reg)
{{
	struct bpf_verifier_env env;
	struct bpf_insn insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;
    
    // Perform custom push_stack to make sure other_branch_*_regs
    // are equal to dst/src_reg. This needs to be done here rather
    // than later (as it appears in kernel code), otherwise
    // other_branch_dst/src_reg will be free to take on any value
    // in the SMT formula when pred == 1 or pred == 0 below, which
    // will then lead to a false positive counterexample.
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

    // ---------------------------------------------------------------
    //  Kernel copy-pasted code begins
    // ---------------------------------------------------------------
	struct bpf_reg_state fake_reg = {{}};
	u8 opcode = BPF_OP(insn.code);
	bool is_jmp32;
	int pred = -1;
	int err;

	if (BPF_SRC(insn.code) == BPF_X) {{
		if (insn.imm != 0) {{
			return;
		}}

	}} else {{
		if (insn.src_reg != BPF_REG_0) {{
			return;
		}}
		src_reg = &fake_reg;
		src_reg->type = SCALAR_VALUE;
		__mark_reg_known(src_reg, insn.imm);
	}}

	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;
	pred = is_branch_taken(dst_reg, src_reg, opcode, is_jmp32);
	if (pred >= 0) {{
		/* If we get here with a dst_reg pointer type it is because
		 * above is_branch_taken() special cased the 0 comparison.
		 */
	}}

	if (pred == 1) {{
		/* Only follow the goto, ignore fall-through. If needed, push
		 * the fall-through branch for simulation under speculative
		 * execution.
		 */
		return;
	}} else if (pred == 0) {{
		/* Only follow the fall-through branch, since that's where the
		 * program will go. If needed, push the goto branch for
		 * simulation under speculative execution.
		 */
		return;
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		err = reg_set_min_max(&env,
				      other_branch_dst_reg,
				      other_branch_src_reg,
				      dst_reg, src_reg, opcode, is_jmp32);
	}} else /* BPF_SRC(insn.code) == BPF_K */ {{
		err = reg_set_min_max(&env,
				      other_branch_dst_reg,
				      src_reg /* fake one */,
				      dst_reg, src_reg /* same fake one */,
				      opcode, is_jmp32);
	}}
	if (err)
		return;

	return;
}}
'''

wrapper_jmp32_7 = wrapper_jmp_7.replace("BPF_JMP_REG", "BPF_JMP32_REG")

wrapper_jmp_8 = '''
void check_cond_jmp_op_wrapper_{}(
	struct bpf_reg_state *restrict dst_reg,
	struct bpf_reg_state *restrict src_reg,
	struct bpf_reg_state *restrict other_branch_dst_reg,
	struct bpf_reg_state *restrict other_branch_src_reg)
{{
	struct bpf_verifier_env env;
	struct bpf_insn insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	__builtin_assume(dst_reg != src_reg);
	__builtin_assume(dst_reg != other_branch_dst_reg);
	__builtin_assume(dst_reg != other_branch_src_reg);
	__builtin_assume(src_reg != other_branch_dst_reg);
	__builtin_assume(src_reg != other_branch_src_reg);
	__builtin_assume(other_branch_dst_reg != other_branch_src_reg);

    // Perform custom push_stack to make sure other_branch_*_regs
    // are equal to dst/src_reg. This needs to be done here rather
    // than later (as it appears in kernel code), otherwise
    // other_branch_dst/src_reg will be free to take on any value
    // in the SMT formula when pred == 1 or pred == 0 below, which
    // will then lead to a false positive counterexample.
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

    // ---------------------------------------------------------------
    //  Kernel copy-pasted code begins
    // ---------------------------------------------------------------
	struct bpf_reg_state fake_reg[2];
	u8 opcode = BPF_OP(insn.code);
	bool is_jmp32;
	int pred = -1;
	int err;

	if (BPF_SRC(insn.code) == BPF_X) {{
		if (insn.imm != 0) {{
			return;
		}}

	}} else {{
		if (insn.src_reg != BPF_REG_0) {{
			return;
		}}
		src_reg = &fake_reg[0];
		src_reg->type = SCALAR_VALUE;
		__mark_reg_known(src_reg, insn.imm);
	}}

	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;
	pred = is_branch_taken(dst_reg, src_reg, opcode, is_jmp32);
	if (pred >= 0) {{
		/* If we get here with a dst_reg pointer type it is because
		 * above is_branch_taken() special cased the 0 comparison.
		 */
	}}

	if (pred == 1) {{
		/* Only follow the goto, ignore fall-through. If needed, push
		 * the fall-through branch for simulation under speculative
		 * execution.
		 */
		return;
	}} else if (pred == 0) {{
		/* Only follow the fall-through branch, since that's where the
		 * program will go. If needed, push the goto branch for
		 * simulation under speculative execution.
		 */
		return;
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		err = reg_set_min_max(&env,
				      other_branch_dst_reg,
				      other_branch_src_reg,
				      dst_reg, src_reg, opcode, is_jmp32);
	}} else /* BPF_SRC(insn.code) == BPF_K */ {{
	    push_stack___(&fake_reg[1], &fake_reg[0]);
		err = reg_set_min_max(&env,
				      other_branch_dst_reg,
				      &fake_reg[0],
				      dst_reg, &fake_reg[1],
				      opcode, is_jmp32);
	}}
	if (err)
		return;

	return;
}}
'''

wrapper_jmp32_8 = wrapper_jmp_8.replace("BPF_JMP_REG", "BPF_JMP32_REG")

wrapper_sync_2 = r'''

void reg_bounds_sync___(struct bpf_reg_state *dst_reg)
{
	__update_reg_bounds(dst_reg);
	__reg_deduce_bounds(dst_reg);
	__reg_bound_offset(dst_reg);
}
'''

# Note: jumps pre 5.19 (__reg_combine_64_into_32, __reg_combine_32_into_64)
# had the following (different) order:
# -	__reg_deduce_bounds(reg);
# -	__reg_bound_offset(reg);
# -	__update_reg_bounds(reg);

wrapper_sync_3 = r'''

void reg_bounds_sync___(struct bpf_reg_state *dst_reg)
{
	reg_bounds_sync(dst_reg);
}

'''

wrapper_sync_4 = r'''

void reg_bounds_sync___(struct bpf_reg_state *dst_reg)
{
	struct bpf_verifier_env env;
	reg_bounds_sync(dst_reg);
}

'''