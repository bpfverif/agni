
wrapper_tnum_fls = r"""
// https://elixir.bootlin.com/linux/latest/source/include/asm-generic/bitops/__fls.h#L13
static unsigned long fls___(unsigned long word)
{
	int num = BITS_PER_LONG - 1;

#if BITS_PER_LONG == 64
	if (!(word & (~0ul << 32))) {
		num -= 32;
		word <<= 32;
	}
#endif
	if (!(word & (~0ul << (BITS_PER_LONG - 16)))) {
		num -= 16;
		word <<= 16;
	}
	if (!(word & (~0ul << (BITS_PER_LONG - 8)))) {
		num -= 8;
		word <<= 8;
	}
	if (!(word & (~0ul << (BITS_PER_LONG - 4)))) {
		num -= 4;
		word <<= 4;
	}
	if (!(word & (~0ul << (BITS_PER_LONG - 2)))) {
		num -= 2;
		word <<= 2;
	}
	if (!(word & (~0ul << (BITS_PER_LONG - 1))))
		num -= 1;
	return num;
}

// https://elixir.bootlin.com/linux/latest/source/include/asm-generic/bitops/fls64.h#L19
static int fls64___(__u64 x)
{
	if (x == 0)
		return 0;
	return fls___(x) + 1;
}

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

wrapper_alu = """

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

wrapper_alu32 = wrapper_alu.replace(
    "adjust_scalar_min_max_vals_wrapper", "adjust_scalar_min_max_vals_wrapper_32")
wrapper_alu32 = wrapper_alu32.replace("BPF_ALU64_REG", "BPF_ALU32_REG")

# 4.14.214 to 4.16-rc1
wrapper_jmp_0 = '''

void check_cond_jmp_op_wrapper_{}(struct bpf_reg_state *dst_reg,
			       struct bpf_reg_state *src_reg,
			       struct bpf_reg_state *other_branch_dst_reg,
			       struct bpf_reg_state *other_branch_src_reg)
{{
    struct bpf_insn insn;
	u8 opcode;

	/* Set BPF insn */
	insn = BPF_JMP_REG({}, BPF_REG_1, BPF_REG_2, 0);
	opcode = BPF_OP(insn.code);
	dst_reg->type = SCALAR_VALUE;
	src_reg->type = SCALAR_VALUE;

	/* Perform custom push_stack to make sure we have don't have garbage values 
	for other_branch_regs */
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

	/* Kernel copy-pasted code begins */
	if (BPF_SRC(insn.code) == BPF_K &&
	    (opcode == BPF_JEQ || opcode == BPF_JNE) &&
	    dst_reg->type == SCALAR_VALUE &&
	    tnum_equals_const(dst_reg->var_off, insn.imm)) {{
		if (opcode == BPF_JEQ) {{
			return;
		}} else {{
			return;
		}}
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		if (dst_reg->type == SCALAR_VALUE &&
		    src_reg->type == SCALAR_VALUE) {{
			if (tnum_is_const(src_reg->var_off))
				reg_set_min_max(other_branch_dst_reg,
						dst_reg, src_reg->var_off.value,
						opcode);
			else if (tnum_is_const(dst_reg->var_off))
				reg_set_min_max_inv(other_branch_src_reg,
						    src_reg,
						    dst_reg->var_off.value, opcode);
			else if (opcode == BPF_JEQ || opcode == BPF_JNE)
				reg_combine_min_max(other_branch_src_reg,
						    other_branch_dst_reg,
						    src_reg,
						    dst_reg, opcode);
		}}
	}} else if (dst_reg->type == SCALAR_VALUE) {{
		reg_set_min_max(other_branch_dst_reg,
					dst_reg, insn.imm, opcode);
	}}

    return;
}}

'''

# 4.16-rc1 to 4.20-rc6
wrapper_jmp_1 = '''

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
	if (BPF_SRC(insn.code) == BPF_K &&
	    (opcode == BPF_JEQ || opcode == BPF_JNE) &&
	    dst_reg->type == SCALAR_VALUE &&
	    tnum_is_const(dst_reg->var_off)) {{
		if ((opcode == BPF_JEQ && dst_reg->var_off.value == insn.imm) ||
		    (opcode == BPF_JNE && dst_reg->var_off.value != insn.imm)) {{
			return;
		}} else {{
			return;
		}}
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		if (dst_reg->type == SCALAR_VALUE &&
		    src_reg->type == SCALAR_VALUE) {{
			if (tnum_is_const(src_reg->var_off))
				reg_set_min_max(other_branch_dst_reg,
						dst_reg, src_reg->var_off.value,
						opcode);
			else if (tnum_is_const(dst_reg->var_off))
				reg_set_min_max_inv(other_branch_src_reg,
						    src_reg,
						    dst_reg->var_off.value, opcode);
			else if (opcode == BPF_JEQ || opcode == BPF_JNE)
				reg_combine_min_max(other_branch_src_reg,
						    other_branch_dst_reg,
						    src_reg,
						    dst_reg, opcode);
		}}
	}} else if (dst_reg->type == SCALAR_VALUE) {{
		reg_set_min_max(other_branch_dst_reg,
					dst_reg, insn.imm, opcode);
	}}

	return;
}}

'''

# 4.20-rc6 to 5.3-rc1
wrapper_jmp_2 = '''

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
	if (BPF_SRC(insn.code) == BPF_K) {{
		int pred = is_branch_taken(dst_reg, insn.imm, opcode);
		if (pred == 1) {{
			return;
		}} else if (pred == 0) {{
			return;
		}}
	}}

	if (BPF_SRC(insn.code) == BPF_X) {{
		if (dst_reg->type == SCALAR_VALUE &&
		    src_reg->type == SCALAR_VALUE) {{
			if (tnum_is_const(src_reg->var_off))
				reg_set_min_max(other_branch_dst_reg,
						dst_reg, src_reg->var_off.value,
						opcode);
			else if (tnum_is_const(dst_reg->var_off))
				reg_set_min_max_inv(other_branch_src_reg,
						    src_reg,
						    dst_reg->var_off.value, opcode);
			else if (opcode == BPF_JEQ || opcode == BPF_JNE)
				reg_combine_min_max(other_branch_src_reg,
						    other_branch_dst_reg,
						    src_reg,
						    dst_reg, opcode);
		}}
	}} else if (dst_reg->type == SCALAR_VALUE) {{
		reg_set_min_max(other_branch_dst_reg,
					dst_reg, insn.imm, opcode);
	}}

}}

'''

# 5.1-rc1 to 5.3-rc1
wrapper_jmp_3 = '''

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
	 * for other_branch_regs in case pred != -1
	 */
	push_stack___(other_branch_dst_reg, dst_reg);
	push_stack___(other_branch_src_reg, src_reg);

	/* Kernel copy-pasted code begins */
	is_jmp32 = BPF_CLASS(insn.code) == BPF_JMP32;

	if (BPF_SRC(insn.code) == BPF_K) {{
		pred = is_branch_taken(dst_reg, insn.imm,
				       opcode, is_jmp32);
		if (pred == 1) {{
			return;
		}} else if (pred == 0) {{
			return;
		}}
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

wrapper32_jmp_3 = wrapper_jmp_3.replace(
    "check_cond_jmp_op_wrapper", "check_cond_jmp_op_wrapper_32")
wrapper32_jmp_3 = wrapper32_jmp_3.replace("BPF_JMP_REG", "BPF_JMP32_REG")

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

wrapper32_jmp_4 = wrapper_jmp_4.replace(
    "check_cond_jmp_op_wrapper", "check_cond_jmp_op_wrapper_32")
wrapper32_jmp_4 = wrapper32_jmp_4.replace("BPF_JMP_REG", "BPF_JMP32_REG")

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

wrapper32_jmp_5 = wrapper_jmp_5.replace(
    "check_cond_jmp_op_wrapper", "check_cond_jmp_op_wrapper_32")
wrapper32_jmp_5 = wrapper32_jmp_5.replace("BPF_JMP_REG", "BPF_JMP32_REG")

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

wrapper32_jmp_6 = wrapper_jmp_6.replace(
    "check_cond_jmp_op_wrapper", "check_cond_jmp_op_wrapper_32")
wrapper32_jmp_6 = wrapper32_jmp_6.replace("BPF_JMP_REG", "BPF_JMP32_REG")

wrapper_sync_1 = r'''

void sync___(struct bpf_reg_state *dst_reg)
{
	__reg_deduce_bounds(dst_reg);
	__reg_bound_offset(dst_reg);
}

'''

wrapper_sync_2 = r'''

void sync___(struct bpf_reg_state *dst_reg)
{
	__update_reg_bounds(dst_reg);
	__reg_deduce_bounds(dst_reg);
	__reg_bound_offset(dst_reg);
}

'''

wrapper_sync_3 = r'''

void sync___(struct bpf_reg_state *dst_reg)
{
    // reg_bounds_sync()
	__update_reg_bounds(dst_reg);
	__reg_deduce_bounds(dst_reg);
	__reg_bound_offset(dst_reg);
	__update_reg_bounds(dst_reg);
}

'''