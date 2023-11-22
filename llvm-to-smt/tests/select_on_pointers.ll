; ModuleID = 'verifier.ll'
source_filename = "verifier.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct.bpf_reg_state = type { i32, i32, i32, %struct.tnum, i64, i64, i64, i64, i32, i32, i32, i32, i32, i32, %struct.bpf_reg_state*, i32, i32, i32, i8 }
%struct.tnum = type { i64, i64 }

; Function Attrs: noinline nounwind uwtable
define dso_local void @check_cond_jmp_op_wrapper_BPF_JEQ(%struct.bpf_reg_state* %dst_reg, %struct.bpf_reg_state* %src_reg, %struct.bpf_reg_state* %other_branch_dst_reg, %struct.bpf_reg_state* %other_branch_src_reg) local_unnamed_addr #0 align 16 {
  %tnum = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 3
  ; %tnum_value = getelementptr inbounds %struct.tnum, %struct.tnum* %tnum, i64 0, i32 0
  %tnum_mask = getelementptr inbounds %struct.tnum, %struct.tnum* %tnum, i64 0, i32 1
  ; %tnum_value_load = load i64, i64* %tnum_value, align 8
  ; store i64 %tnum_value_load, i64* %tnum_mask, align 8
  %tnum_mask_load = load i64, i64* %tnum_mask, align 8
  %tnum_is_known = icmp eq i64 %tnum_mask_load, 0
  ; ite(tnum_mask_load_bv == 0, tnum_is_known_bv == 1, tnum_is_known_bv == 0)
  %select_false_reg = select i1 %tnum_is_known, %struct.bpf_reg_state* %src_reg, %struct.bpf_reg_state* %dst_reg
  ; SelectMap: select_false_reg, tnum_is_known, src_reg, dst_reg
  %tnum_value_false_reg = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %select_false_reg, i64 0, i32 3, i32 0
  ; GEPMap: tnum_value_false_reg, select_false_reg, 3, 0
  %tnum_value_false_reg_load = load i64, i64* %tnum_value_false_reg, align 8
  ; ite(tnum_is_known_bv == 1, tnum_value_false_reg_load == src_reg_3_0, tnum_value_false_reg_load == dst_reg_3_0)
  %tnum_mask_is_unknown = icmp eq i64 %tnum_mask_load, 18446744073709551615
  ; ite(tnum_mask_load_bv == 18446744073709551615, tnum_mask_is_unknown_bv == 1, tnum_mask_is_unknown_bv == 0)
  %select_true_reg = select i1 %tnum_mask_is_unknown, %struct.bpf_reg_state* %other_branch_dst_reg, %struct.bpf_reg_state* %other_branch_src_reg
  ; SelectMap: select_true_reg, tnum_mask_is_unknown, other_branch_dst_reg, other_branch_src_reg
  %tnum_value_true_reg = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %select_true_reg, i64 0, i32 3, i32 0
  ; GEPMap: tnum_value_true_reg, select_true_reg, 3, 0
  store i64 %tnum_value_false_reg_load, i64* %tnum_value_true_reg, align 8
  ; other_branch_dst_reg: [other_dst_bv_0, other_dst_bv_1, other_dst_bv_2, [select_store_bv_0, other_dst_bv_4], other_dst_bv_5, ...]
  ; other_branch_src_reg: [other_src_bv_0, other_src_bv_1, other_src_bv_2, [select_store_bv_1, other_src_bv_4], other_src_bv_5, ...]
  ; assert in bbassetionsMap:
  ; ite(tnum_mask_is_unknown == 1, select_store_bv_0 == tnum_value_false_reg_load_bv, select_store_bv_0 == other_dst_bv_3)
  ; ite(tnum_mask_is_unknown == 0, select_store_bv_1 == tnum_value_false_reg_load_bv, select_store_bv_1 == other_src_bv_3)

  ret void
}

attributes #0 = { alwaysinline norecurse nounwind readnone uwtable willreturn "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { alwaysinline nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { argmemonly nofree nosync nounwind willreturn }
attributes #4 = { noinline nounwind uwtable "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nounwind }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 12.0.1 (https://github.com/llvm/llvm-project.git fed41342a82f5a3a9201819a82bf7a48313e296b)"}
