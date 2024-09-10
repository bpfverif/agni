; ModuleID = 'kernel/bpf/tnum.c'
source_filename = "kernel/bpf/tnum.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

module asm "\09.section \22__ksymtab_strings\22,\22aMS\22,%progbits,1\09"
module asm "__kstrtab_tnum_strn:\09\09\09\09\09"
module asm "\09.asciz \09\22tnum_strn\22\09\09\09\09\09"
module asm "__kstrtabns_tnum_strn:\09\09\09\09\09"
module asm "\09.asciz \09\22\22\09\09\09\09\09"
module asm "\09.previous\09\09\09\09\09\09"
module asm "\09.section \22___ksymtab_gpl+tnum_strn\22, \22a\22\09"
module asm "\09.balign\094\09\09\09\09\09"
module asm "__ksymtab_tnum_strn:\09\09\09\09"
module asm "\09.long\09tnum_strn- .\09\09\09\09"
module asm "\09.long\09__kstrtab_tnum_strn- .\09\09\09"
module asm "\09.long\09__kstrtabns_tnum_strn- .\09\09\09"
module asm "\09.previous\09\09\09\09\09"

%struct.tnum = type { i64, i64 }

@tnum_unknown = dso_local constant %struct.tnum { i64 0, i64 -1 }, align 8
@.str = private unnamed_addr constant [15 x i8] c"(%#llx; %#llx)\00", align 1
@__UNIQUE_ID___addressable_tnum_strn3 = internal global i8* bitcast (i32 (i8*, i64, i64, i64)* @tnum_strn to i8*), section ".discard.addressable", align 8
@llvm.compiler.used = appending global [1 x i8*] [i8* bitcast (i8** @__UNIQUE_ID___addressable_tnum_strn3 to i8*)], section "llvm.metadata"

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_const(i64 noundef %value) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %value.addr = alloca i64, align 8
  store i64 %value, i64* %value.addr, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %0 = load i64, i64* %value.addr, align 8
  store i64 %0, i64* %value1, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  store i64 0, i64* %mask, align 8
  %1 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %2 = load { i64, i64 }, { i64, i64 }* %1, align 8
  ret { i64, i64 } %2
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_range(i64 noundef %min, i64 noundef %max) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %min.addr = alloca i64, align 8
  %max.addr = alloca i64, align 8
  %chi = alloca i64, align 8
  %delta = alloca i64, align 8
  %bits = alloca i8, align 1
  store i64 %min, i64* %min.addr, align 8
  store i64 %max, i64* %max.addr, align 8
  %0 = load i64, i64* %min.addr, align 8
  %1 = load i64, i64* %max.addr, align 8
  %xor = xor i64 %0, %1
  store i64 %xor, i64* %chi, align 8
  %2 = load i64, i64* %chi, align 8
  %call = call i32 @fls64___(i64 noundef %2) #4
  %conv = trunc i32 %call to i8
  store i8 %conv, i8* %bits, align 1
  %3 = load i8, i8* %bits, align 1
  %conv1 = zext i8 %3 to i32
  %cmp = icmp sgt i32 %conv1, 63
  br i1 %cmp, label %if.then, label %if.end

if.then:                                          ; preds = %entry
  %4 = bitcast %struct.tnum* %retval to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %4, i8* align 8 bitcast (%struct.tnum* @tnum_unknown to i8*), i64 16, i1 false)
  br label %return

if.end:                                           ; preds = %entry
  %5 = load i8, i8* %bits, align 1
  %conv3 = zext i8 %5 to i32
  %sh_prom = zext i32 %conv3 to i64
  %shl = shl i64 1, %sh_prom
  %sub = sub i64 %shl, 1
  store i64 %sub, i64* %delta, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %6 = load i64, i64* %min.addr, align 8
  %7 = load i64, i64* %delta, align 8
  %neg = xor i64 %7, -1
  %and = and i64 %6, %neg
  store i64 %and, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %8 = load i64, i64* %delta, align 8
  store i64 %8, i64* %mask, align 8
  br label %return

return:                                           ; preds = %if.end, %if.then
  %9 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %10 = load { i64, i64 }, { i64, i64 }* %9, align 8
  ret { i64, i64 } %10
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define internal i32 @fls64___(i64 noundef %x) #0 {
entry:
  %retval = alloca i32, align 4
  %x.addr = alloca i64, align 8
  store i64 %x, i64* %x.addr, align 8
  %0 = load i64, i64* %x.addr, align 8
  %cmp = icmp eq i64 %0, 0
  br i1 %cmp, label %if.then, label %if.end

if.then:                                          ; preds = %entry
  store i32 0, i32* %retval, align 4
  br label %return

if.end:                                           ; preds = %entry
  %1 = load i64, i64* %x.addr, align 8
  %call = call i32 @generic___fls___(i64 noundef %1) #4
  %add = add i32 %call, 1
  store i32 %add, i32* %retval, align 4
  br label %return

return:                                           ; preds = %if.end, %if.then
  %2 = load i32, i32* %retval, align 4
  ret i32 %2
}

; Function Attrs: argmemonly nofree nounwind willreturn
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* noalias nocapture writeonly, i8* noalias nocapture readonly, i64, i1 immarg) #1

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_lshift(i64 %a.coerce0, i64 %a.coerce1, i8 noundef zeroext %shift) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %shift.addr = alloca i8, align 1
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i8 %shift, i8* %shift.addr, align 1
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %3 = load i64, i64* %value1, align 8
  %4 = load i8, i8* %shift.addr, align 1
  %conv = zext i8 %4 to i32
  %sh_prom = zext i32 %conv to i64
  %shl = shl i64 %3, %sh_prom
  store i64 %shl, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %5 = load i64, i64* %mask2, align 8
  %6 = load i8, i8* %shift.addr, align 1
  %conv3 = zext i8 %6 to i32
  %sh_prom4 = zext i32 %conv3 to i64
  %shl5 = shl i64 %5, %sh_prom4
  store i64 %shl5, i64* %mask, align 8
  %7 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %8 = load { i64, i64 }, { i64, i64 }* %7, align 8
  ret { i64, i64 } %8
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_rshift(i64 %a.coerce0, i64 %a.coerce1, i8 noundef zeroext %shift) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %shift.addr = alloca i8, align 1
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i8 %shift, i8* %shift.addr, align 1
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %3 = load i64, i64* %value1, align 8
  %4 = load i8, i8* %shift.addr, align 1
  %conv = zext i8 %4 to i32
  %sh_prom = zext i32 %conv to i64
  %shr = lshr i64 %3, %sh_prom
  store i64 %shr, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %5 = load i64, i64* %mask2, align 8
  %6 = load i8, i8* %shift.addr, align 1
  %conv3 = zext i8 %6 to i32
  %sh_prom4 = zext i32 %conv3 to i64
  %shr5 = lshr i64 %5, %sh_prom4
  store i64 %shr5, i64* %mask, align 8
  %7 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %8 = load { i64, i64 }, { i64, i64 }* %7, align 8
  ret { i64, i64 } %8
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_arshift(i64 %a.coerce0, i64 %a.coerce1, i8 noundef zeroext %min_shift, i8 noundef zeroext %insn_bitness) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %min_shift.addr = alloca i8, align 1
  %insn_bitness.addr = alloca i8, align 1
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i8 %min_shift, i8* %min_shift.addr, align 1
  store i8 %insn_bitness, i8* %insn_bitness.addr, align 1
  %3 = load i8, i8* %insn_bitness.addr, align 1
  %conv = zext i8 %3 to i32
  %cmp = icmp eq i32 %conv, 32
  br i1 %cmp, label %if.then, label %if.else

if.then:                                          ; preds = %entry
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %value2 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %4 = load i64, i64* %value2, align 8
  %conv3 = trunc i64 %4 to i32
  %5 = load i8, i8* %min_shift.addr, align 1
  %conv4 = zext i8 %5 to i32
  %shr = ashr i32 %conv3, %conv4
  %conv5 = zext i32 %shr to i64
  store i64 %conv5, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %mask6 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %6 = load i64, i64* %mask6, align 8
  %conv7 = trunc i64 %6 to i32
  %7 = load i8, i8* %min_shift.addr, align 1
  %conv8 = zext i8 %7 to i32
  %shr9 = ashr i32 %conv7, %conv8
  %conv10 = zext i32 %shr9 to i64
  store i64 %conv10, i64* %mask, align 8
  br label %return

if.else:                                          ; preds = %entry
  %value11 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %value12 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %8 = load i64, i64* %value12, align 8
  %9 = load i8, i8* %min_shift.addr, align 1
  %conv13 = zext i8 %9 to i32
  %sh_prom = zext i32 %conv13 to i64
  %shr14 = ashr i64 %8, %sh_prom
  store i64 %shr14, i64* %value11, align 8
  %mask15 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %mask16 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %10 = load i64, i64* %mask16, align 8
  %11 = load i8, i8* %min_shift.addr, align 1
  %conv17 = zext i8 %11 to i32
  %sh_prom18 = zext i32 %conv17 to i64
  %shr19 = ashr i64 %10, %sh_prom18
  store i64 %shr19, i64* %mask15, align 8
  br label %return

return:                                           ; preds = %if.else, %if.then
  %12 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %13 = load { i64, i64 }, { i64, i64 }* %12, align 8
  ret { i64, i64 } %13
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_add(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %sm = alloca i64, align 8
  %sv = alloca i64, align 8
  %sigma = alloca i64, align 8
  %chi = alloca i64, align 8
  %mu = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %6 = load i64, i64* %mask, align 8
  %mask1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %7 = load i64, i64* %mask1, align 8
  %add = add i64 %6, %7
  store i64 %add, i64* %sm, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %8 = load i64, i64* %value, align 8
  %value2 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %9 = load i64, i64* %value2, align 8
  %add3 = add i64 %8, %9
  store i64 %add3, i64* %sv, align 8
  %10 = load i64, i64* %sm, align 8
  %11 = load i64, i64* %sv, align 8
  %add4 = add i64 %10, %11
  store i64 %add4, i64* %sigma, align 8
  %12 = load i64, i64* %sigma, align 8
  %13 = load i64, i64* %sv, align 8
  %xor = xor i64 %12, %13
  store i64 %xor, i64* %chi, align 8
  %14 = load i64, i64* %chi, align 8
  %mask5 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %15 = load i64, i64* %mask5, align 8
  %or = or i64 %14, %15
  %mask6 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %16 = load i64, i64* %mask6, align 8
  %or7 = or i64 %or, %16
  store i64 %or7, i64* %mu, align 8
  %value8 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %17 = load i64, i64* %sv, align 8
  %18 = load i64, i64* %mu, align 8
  %neg = xor i64 %18, -1
  %and = and i64 %17, %neg
  store i64 %and, i64* %value8, align 8
  %mask9 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %19 = load i64, i64* %mu, align 8
  store i64 %19, i64* %mask9, align 8
  %20 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %21 = load { i64, i64 }, { i64, i64 }* %20, align 8
  ret { i64, i64 } %21
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_sub(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %dv = alloca i64, align 8
  %alpha = alloca i64, align 8
  %beta = alloca i64, align 8
  %chi = alloca i64, align 8
  %mu = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %6 = load i64, i64* %value, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %7 = load i64, i64* %value1, align 8
  %sub = sub i64 %6, %7
  store i64 %sub, i64* %dv, align 8
  %8 = load i64, i64* %dv, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %9 = load i64, i64* %mask, align 8
  %add = add i64 %8, %9
  store i64 %add, i64* %alpha, align 8
  %10 = load i64, i64* %dv, align 8
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %11 = load i64, i64* %mask2, align 8
  %sub3 = sub i64 %10, %11
  store i64 %sub3, i64* %beta, align 8
  %12 = load i64, i64* %alpha, align 8
  %13 = load i64, i64* %beta, align 8
  %xor = xor i64 %12, %13
  store i64 %xor, i64* %chi, align 8
  %14 = load i64, i64* %chi, align 8
  %mask4 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %15 = load i64, i64* %mask4, align 8
  %or = or i64 %14, %15
  %mask5 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %16 = load i64, i64* %mask5, align 8
  %or6 = or i64 %or, %16
  store i64 %or6, i64* %mu, align 8
  %value7 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %17 = load i64, i64* %dv, align 8
  %18 = load i64, i64* %mu, align 8
  %neg = xor i64 %18, -1
  %and = and i64 %17, %neg
  store i64 %and, i64* %value7, align 8
  %mask8 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %19 = load i64, i64* %mu, align 8
  store i64 %19, i64* %mask8, align 8
  %20 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %21 = load { i64, i64 }, { i64, i64 }* %20, align 8
  ret { i64, i64 } %21
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_and(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %alpha = alloca i64, align 8
  %beta = alloca i64, align 8
  %v = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %6 = load i64, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %7 = load i64, i64* %mask, align 8
  %or = or i64 %6, %7
  store i64 %or, i64* %alpha, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %8 = load i64, i64* %value1, align 8
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %9 = load i64, i64* %mask2, align 8
  %or3 = or i64 %8, %9
  store i64 %or3, i64* %beta, align 8
  %value4 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %10 = load i64, i64* %value4, align 8
  %value5 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %11 = load i64, i64* %value5, align 8
  %and = and i64 %10, %11
  store i64 %and, i64* %v, align 8
  %value6 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %12 = load i64, i64* %v, align 8
  store i64 %12, i64* %value6, align 8
  %mask7 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %13 = load i64, i64* %alpha, align 8
  %14 = load i64, i64* %beta, align 8
  %and8 = and i64 %13, %14
  %15 = load i64, i64* %v, align 8
  %neg = xor i64 %15, -1
  %and9 = and i64 %and8, %neg
  store i64 %and9, i64* %mask7, align 8
  %16 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %17 = load { i64, i64 }, { i64, i64 }* %16, align 8
  ret { i64, i64 } %17
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_or(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %v = alloca i64, align 8
  %mu = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %6 = load i64, i64* %value, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %7 = load i64, i64* %value1, align 8
  %or = or i64 %6, %7
  store i64 %or, i64* %v, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %8 = load i64, i64* %mask, align 8
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %9 = load i64, i64* %mask2, align 8
  %or3 = or i64 %8, %9
  store i64 %or3, i64* %mu, align 8
  %value4 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %10 = load i64, i64* %v, align 8
  store i64 %10, i64* %value4, align 8
  %mask5 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %11 = load i64, i64* %mu, align 8
  %12 = load i64, i64* %v, align 8
  %neg = xor i64 %12, -1
  %and = and i64 %11, %neg
  store i64 %and, i64* %mask5, align 8
  %13 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %14 = load { i64, i64 }, { i64, i64 }* %13, align 8
  ret { i64, i64 } %14
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_xor(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %v = alloca i64, align 8
  %mu = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %6 = load i64, i64* %value, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %7 = load i64, i64* %value1, align 8
  %xor = xor i64 %6, %7
  store i64 %xor, i64* %v, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %8 = load i64, i64* %mask, align 8
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %9 = load i64, i64* %mask2, align 8
  %or = or i64 %8, %9
  store i64 %or, i64* %mu, align 8
  %value3 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %10 = load i64, i64* %v, align 8
  %11 = load i64, i64* %mu, align 8
  %neg = xor i64 %11, -1
  %and = and i64 %10, %neg
  store i64 %and, i64* %value3, align 8
  %mask4 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %12 = load i64, i64* %mu, align 8
  store i64 %12, i64* %mask4, align 8
  %13 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %14 = load { i64, i64 }, { i64, i64 }* %13, align 8
  ret { i64, i64 } %14
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_mul(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %acc_v = alloca i64, align 8
  %acc_m = alloca %struct.tnum, align 8
  %tmp = alloca %struct.tnum, align 8
  %.compoundliteral = alloca %struct.tnum, align 8
  %tmp13 = alloca %struct.tnum, align 8
  %.compoundliteral14 = alloca %struct.tnum, align 8
  %tmp21 = alloca %struct.tnum, align 8
  %tmp23 = alloca %struct.tnum, align 8
  %.compoundliteral25 = alloca %struct.tnum, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %6 = load i64, i64* %value, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %7 = load i64, i64* %value1, align 8
  %mul = mul i64 %6, %7
  store i64 %mul, i64* %acc_v, align 8
  %8 = bitcast %struct.tnum* %acc_m to i8*
  call void @llvm.memset.p0i8.i64(i8* align 8 %8, i8 0, i64 16, i1 false)
  br label %while.cond

while.cond:                                       ; preds = %if.end20, %entry
  %value2 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %9 = load i64, i64* %value2, align 8
  %tobool = icmp ne i64 %9, 0
  br i1 %tobool, label %lor.end, label %lor.rhs

lor.rhs:                                          ; preds = %while.cond
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %10 = load i64, i64* %mask, align 8
  %tobool3 = icmp ne i64 %10, 0
  br label %lor.end

lor.end:                                          ; preds = %lor.rhs, %while.cond
  %11 = phi i1 [ true, %while.cond ], [ %tobool3, %lor.rhs ]
  br i1 %11, label %while.body, label %while.end

while.body:                                       ; preds = %lor.end
  %value4 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %12 = load i64, i64* %value4, align 8
  %and = and i64 %12, 1
  %tobool5 = icmp ne i64 %and, 0
  br i1 %tobool5, label %if.then, label %if.else

if.then:                                          ; preds = %while.body
  %value6 = getelementptr inbounds %struct.tnum, %struct.tnum* %.compoundliteral, i32 0, i32 0
  store i64 0, i64* %value6, align 8
  %mask7 = getelementptr inbounds %struct.tnum, %struct.tnum* %.compoundliteral, i32 0, i32 1
  %mask8 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %13 = load i64, i64* %mask8, align 8
  store i64 %13, i64* %mask7, align 8
  %14 = bitcast %struct.tnum* %acc_m to { i64, i64 }*
  %15 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %14, i32 0, i32 0
  %16 = load i64, i64* %15, align 8
  %17 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %14, i32 0, i32 1
  %18 = load i64, i64* %17, align 8
  %19 = bitcast %struct.tnum* %.compoundliteral to { i64, i64 }*
  %20 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %19, i32 0, i32 0
  %21 = load i64, i64* %20, align 8
  %22 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %19, i32 0, i32 1
  %23 = load i64, i64* %22, align 8
  %call = call { i64, i64 } @tnum_add(i64 %16, i64 %18, i64 %21, i64 %23) #4
  %24 = bitcast %struct.tnum* %tmp to { i64, i64 }*
  %25 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %24, i32 0, i32 0
  %26 = extractvalue { i64, i64 } %call, 0
  store i64 %26, i64* %25, align 8
  %27 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %24, i32 0, i32 1
  %28 = extractvalue { i64, i64 } %call, 1
  store i64 %28, i64* %27, align 8
  %29 = bitcast %struct.tnum* %acc_m to i8*
  %30 = bitcast %struct.tnum* %tmp to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %29, i8* align 8 %30, i64 16, i1 false)
  br label %if.end20

if.else:                                          ; preds = %while.body
  %mask9 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %31 = load i64, i64* %mask9, align 8
  %and10 = and i64 %31, 1
  %tobool11 = icmp ne i64 %and10, 0
  br i1 %tobool11, label %if.then12, label %if.end

if.then12:                                        ; preds = %if.else
  %value15 = getelementptr inbounds %struct.tnum, %struct.tnum* %.compoundliteral14, i32 0, i32 0
  store i64 0, i64* %value15, align 8
  %mask16 = getelementptr inbounds %struct.tnum, %struct.tnum* %.compoundliteral14, i32 0, i32 1
  %value17 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %32 = load i64, i64* %value17, align 8
  %mask18 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %33 = load i64, i64* %mask18, align 8
  %or = or i64 %32, %33
  store i64 %or, i64* %mask16, align 8
  %34 = bitcast %struct.tnum* %acc_m to { i64, i64 }*
  %35 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %34, i32 0, i32 0
  %36 = load i64, i64* %35, align 8
  %37 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %34, i32 0, i32 1
  %38 = load i64, i64* %37, align 8
  %39 = bitcast %struct.tnum* %.compoundliteral14 to { i64, i64 }*
  %40 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %39, i32 0, i32 0
  %41 = load i64, i64* %40, align 8
  %42 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %39, i32 0, i32 1
  %43 = load i64, i64* %42, align 8
  %call19 = call { i64, i64 } @tnum_add(i64 %36, i64 %38, i64 %41, i64 %43) #4
  %44 = bitcast %struct.tnum* %tmp13 to { i64, i64 }*
  %45 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %44, i32 0, i32 0
  %46 = extractvalue { i64, i64 } %call19, 0
  store i64 %46, i64* %45, align 8
  %47 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %44, i32 0, i32 1
  %48 = extractvalue { i64, i64 } %call19, 1
  store i64 %48, i64* %47, align 8
  %49 = bitcast %struct.tnum* %acc_m to i8*
  %50 = bitcast %struct.tnum* %tmp13 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %49, i8* align 8 %50, i64 16, i1 false)
  br label %if.end

if.end:                                           ; preds = %if.then12, %if.else
  br label %if.end20

if.end20:                                         ; preds = %if.end, %if.then
  %51 = bitcast %struct.tnum* %a to { i64, i64 }*
  %52 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %51, i32 0, i32 0
  %53 = load i64, i64* %52, align 8
  %54 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %51, i32 0, i32 1
  %55 = load i64, i64* %54, align 8
  %call22 = call { i64, i64 } @tnum_rshift(i64 %53, i64 %55, i8 noundef zeroext 1) #4
  %56 = bitcast %struct.tnum* %tmp21 to { i64, i64 }*
  %57 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %56, i32 0, i32 0
  %58 = extractvalue { i64, i64 } %call22, 0
  store i64 %58, i64* %57, align 8
  %59 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %56, i32 0, i32 1
  %60 = extractvalue { i64, i64 } %call22, 1
  store i64 %60, i64* %59, align 8
  %61 = bitcast %struct.tnum* %a to i8*
  %62 = bitcast %struct.tnum* %tmp21 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %61, i8* align 8 %62, i64 16, i1 false)
  %63 = bitcast %struct.tnum* %b to { i64, i64 }*
  %64 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %63, i32 0, i32 0
  %65 = load i64, i64* %64, align 8
  %66 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %63, i32 0, i32 1
  %67 = load i64, i64* %66, align 8
  %call24 = call { i64, i64 } @tnum_lshift(i64 %65, i64 %67, i8 noundef zeroext 1) #4
  %68 = bitcast %struct.tnum* %tmp23 to { i64, i64 }*
  %69 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %68, i32 0, i32 0
  %70 = extractvalue { i64, i64 } %call24, 0
  store i64 %70, i64* %69, align 8
  %71 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %68, i32 0, i32 1
  %72 = extractvalue { i64, i64 } %call24, 1
  store i64 %72, i64* %71, align 8
  %73 = bitcast %struct.tnum* %b to i8*
  %74 = bitcast %struct.tnum* %tmp23 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %73, i8* align 8 %74, i64 16, i1 false)
  br label %while.cond, !llvm.loop !5

while.end:                                        ; preds = %lor.end
  %value26 = getelementptr inbounds %struct.tnum, %struct.tnum* %.compoundliteral25, i32 0, i32 0
  %75 = load i64, i64* %acc_v, align 8
  store i64 %75, i64* %value26, align 8
  %mask27 = getelementptr inbounds %struct.tnum, %struct.tnum* %.compoundliteral25, i32 0, i32 1
  store i64 0, i64* %mask27, align 8
  %76 = bitcast %struct.tnum* %.compoundliteral25 to { i64, i64 }*
  %77 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %76, i32 0, i32 0
  %78 = load i64, i64* %77, align 8
  %79 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %76, i32 0, i32 1
  %80 = load i64, i64* %79, align 8
  %81 = bitcast %struct.tnum* %acc_m to { i64, i64 }*
  %82 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %81, i32 0, i32 0
  %83 = load i64, i64* %82, align 8
  %84 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %81, i32 0, i32 1
  %85 = load i64, i64* %84, align 8
  %call28 = call { i64, i64 } @tnum_add(i64 %78, i64 %80, i64 %83, i64 %85) #4
  %86 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %87 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %86, i32 0, i32 0
  %88 = extractvalue { i64, i64 } %call28, 0
  store i64 %88, i64* %87, align 8
  %89 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %86, i32 0, i32 1
  %90 = extractvalue { i64, i64 } %call28, 1
  store i64 %90, i64* %89, align 8
  %91 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %92 = load { i64, i64 }, { i64, i64 }* %91, align 8
  ret { i64, i64 } %92
}

; Function Attrs: argmemonly nofree nounwind willreturn writeonly
declare void @llvm.memset.p0i8.i64(i8* nocapture writeonly, i8, i64, i1 immarg) #2

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_intersect(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %v = alloca i64, align 8
  %mu = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %6 = load i64, i64* %value, align 8
  %value1 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %7 = load i64, i64* %value1, align 8
  %or = or i64 %6, %7
  store i64 %or, i64* %v, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %8 = load i64, i64* %mask, align 8
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %9 = load i64, i64* %mask2, align 8
  %and = and i64 %8, %9
  store i64 %and, i64* %mu, align 8
  %value3 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 0
  %10 = load i64, i64* %v, align 8
  %11 = load i64, i64* %mu, align 8
  %neg = xor i64 %11, -1
  %and4 = and i64 %10, %neg
  store i64 %and4, i64* %value3, align 8
  %mask5 = getelementptr inbounds %struct.tnum, %struct.tnum* %retval, i32 0, i32 1
  %12 = load i64, i64* %mu, align 8
  store i64 %12, i64* %mask5, align 8
  %13 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %14 = load { i64, i64 }, { i64, i64 }* %13, align 8
  ret { i64, i64 } %14
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_cast(i64 %a.coerce0, i64 %a.coerce1, i8 noundef zeroext %size) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %size.addr = alloca i8, align 1
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i8 %size, i8* %size.addr, align 1
  %3 = load i8, i8* %size.addr, align 1
  %conv = zext i8 %3 to i32
  %mul = mul i32 %conv, 8
  %sh_prom = zext i32 %mul to i64
  %shl = shl i64 1, %sh_prom
  %sub = sub i64 %shl, 1
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %4 = load i64, i64* %value, align 8
  %and = and i64 %4, %sub
  store i64 %and, i64* %value, align 8
  %5 = load i8, i8* %size.addr, align 1
  %conv1 = zext i8 %5 to i32
  %mul2 = mul i32 %conv1, 8
  %sh_prom3 = zext i32 %mul2 to i64
  %shl4 = shl i64 1, %sh_prom3
  %sub5 = sub i64 %shl4, 1
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %6 = load i64, i64* %mask, align 8
  %and6 = and i64 %6, %sub5
  store i64 %and6, i64* %mask, align 8
  %7 = bitcast %struct.tnum* %retval to i8*
  %8 = bitcast %struct.tnum* %a to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %7, i8* align 8 %8, i64 16, i1 false)
  %9 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %10 = load { i64, i64 }, { i64, i64 }* %9, align 8
  ret { i64, i64 } %10
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local zeroext i1 @tnum_is_aligned(i64 %a.coerce0, i64 %a.coerce1, i64 noundef %size) #0 {
entry:
  %retval = alloca i1, align 1
  %a = alloca %struct.tnum, align 8
  %size.addr = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i64 %size, i64* %size.addr, align 8
  %3 = load i64, i64* %size.addr, align 8
  %tobool = icmp ne i64 %3, 0
  br i1 %tobool, label %if.end, label %if.then

if.then:                                          ; preds = %entry
  store i1 true, i1* %retval, align 1
  br label %return

if.end:                                           ; preds = %entry
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %4 = load i64, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %5 = load i64, i64* %mask, align 8
  %or = or i64 %4, %5
  %6 = load i64, i64* %size.addr, align 8
  %sub = sub i64 %6, 1
  %and = and i64 %or, %sub
  %tobool1 = icmp ne i64 %and, 0
  %lnot = xor i1 %tobool1, true
  store i1 %lnot, i1* %retval, align 1
  br label %return

return:                                           ; preds = %if.end, %if.then
  %7 = load i1, i1* %retval, align 1
  ret i1 %7
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local zeroext i1 @tnum_in(i64 %a.coerce0, i64 %a.coerce1, i64 %b.coerce0, i64 %b.coerce1) #0 {
entry:
  %retval = alloca i1, align 1
  %a = alloca %struct.tnum, align 8
  %b = alloca %struct.tnum, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %b to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  store i64 %b.coerce0, i64* %4, align 8
  %5 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  store i64 %b.coerce1, i64* %5, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 1
  %6 = load i64, i64* %mask, align 8
  %mask1 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %7 = load i64, i64* %mask1, align 8
  %neg = xor i64 %7, -1
  %and = and i64 %6, %neg
  %tobool = icmp ne i64 %and, 0
  br i1 %tobool, label %if.then, label %if.end

if.then:                                          ; preds = %entry
  store i1 false, i1* %retval, align 1
  br label %return

if.end:                                           ; preds = %entry
  %mask2 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %8 = load i64, i64* %mask2, align 8
  %neg3 = xor i64 %8, -1
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %9 = load i64, i64* %value, align 8
  %and4 = and i64 %9, %neg3
  store i64 %and4, i64* %value, align 8
  %value5 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %10 = load i64, i64* %value5, align 8
  %value6 = getelementptr inbounds %struct.tnum, %struct.tnum* %b, i32 0, i32 0
  %11 = load i64, i64* %value6, align 8
  %cmp = icmp eq i64 %10, %11
  store i1 %cmp, i1* %retval, align 1
  br label %return

return:                                           ; preds = %if.end, %if.then
  %12 = load i1, i1* %retval, align 1
  ret i1 %12
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local i32 @tnum_strn(i8* noundef %str, i64 noundef %size, i64 %a.coerce0, i64 %a.coerce1) #0 {
entry:
  %a = alloca %struct.tnum, align 8
  %str.addr = alloca i8*, align 8
  %size.addr = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i8* %str, i8** %str.addr, align 8
  store i64 %size, i64* %size.addr, align 8
  %3 = load i8*, i8** %str.addr, align 8
  %4 = load i64, i64* %size.addr, align 8
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %5 = load i64, i64* %value, align 8
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %6 = load i64, i64* %mask, align 8
  %call = call i32 (i8*, i64, i8*, ...) @snprintf(i8* noundef %3, i64 noundef %4, i8* noundef getelementptr inbounds ([15 x i8], [15 x i8]* @.str, i64 0, i64 0), i64 noundef %5, i64 noundef %6) #4
  ret i32 %call
}

; Function Attrs: noredzone null_pointer_is_valid
declare dso_local i32 @snprintf(i8* noundef, i64 noundef, i8* noundef, ...) #3

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local i32 @tnum_sbin(i8* noundef %str, i64 noundef %size, i64 %a.coerce0, i64 %a.coerce1) #0 {
entry:
  %a = alloca %struct.tnum, align 8
  %str.addr = alloca i8*, align 8
  %size.addr = alloca i64, align 8
  %n = alloca i64, align 8
  %__UNIQUE_ID___x4 = alloca i64, align 8
  %__UNIQUE_ID___y5 = alloca i64, align 8
  %tmp = alloca i64, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i8* %str, i8** %str.addr, align 8
  store i64 %size, i64* %size.addr, align 8
  store i64 64, i64* %n, align 8
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %3 = load i64, i64* %n, align 8
  %tobool = icmp ne i64 %3, 0
  br i1 %tobool, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %4 = load i64, i64* %n, align 8
  %5 = load i64, i64* %size.addr, align 8
  %cmp = icmp ult i64 %4, %5
  br i1 %cmp, label %if.then, label %if.end12

if.then:                                          ; preds = %for.body
  %mask = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %6 = load i64, i64* %mask, align 8
  %and = and i64 %6, 1
  %tobool1 = icmp ne i64 %and, 0
  br i1 %tobool1, label %if.then2, label %if.else

if.then2:                                         ; preds = %if.then
  %7 = load i8*, i8** %str.addr, align 8
  %8 = load i64, i64* %n, align 8
  %sub = sub i64 %8, 1
  %arrayidx = getelementptr i8, i8* %7, i64 %sub
  store i8 120, i8* %arrayidx, align 1
  br label %if.end11

if.else:                                          ; preds = %if.then
  %value = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %9 = load i64, i64* %value, align 8
  %and3 = and i64 %9, 1
  %tobool4 = icmp ne i64 %and3, 0
  br i1 %tobool4, label %if.then5, label %if.else8

if.then5:                                         ; preds = %if.else
  %10 = load i8*, i8** %str.addr, align 8
  %11 = load i64, i64* %n, align 8
  %sub6 = sub i64 %11, 1
  %arrayidx7 = getelementptr i8, i8* %10, i64 %sub6
  store i8 49, i8* %arrayidx7, align 1
  br label %if.end

if.else8:                                         ; preds = %if.else
  %12 = load i8*, i8** %str.addr, align 8
  %13 = load i64, i64* %n, align 8
  %sub9 = sub i64 %13, 1
  %arrayidx10 = getelementptr i8, i8* %12, i64 %sub9
  store i8 48, i8* %arrayidx10, align 1
  br label %if.end

if.end:                                           ; preds = %if.else8, %if.then5
  br label %if.end11

if.end11:                                         ; preds = %if.end, %if.then2
  br label %if.end12

if.end12:                                         ; preds = %if.end11, %for.body
  %mask13 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 1
  %14 = load i64, i64* %mask13, align 8
  %shr = lshr i64 %14, 1
  store i64 %shr, i64* %mask13, align 8
  %value14 = getelementptr inbounds %struct.tnum, %struct.tnum* %a, i32 0, i32 0
  %15 = load i64, i64* %value14, align 8
  %shr15 = lshr i64 %15, 1
  store i64 %shr15, i64* %value14, align 8
  br label %for.inc

for.inc:                                          ; preds = %if.end12
  %16 = load i64, i64* %n, align 8
  %dec = add i64 %16, -1
  store i64 %dec, i64* %n, align 8
  br label %for.cond, !llvm.loop !7

for.end:                                          ; preds = %for.cond
  %17 = load i8*, i8** %str.addr, align 8
  %18 = load i64, i64* %size.addr, align 8
  %sub16 = sub i64 %18, 1
  store i64 %sub16, i64* %__UNIQUE_ID___x4, align 8
  store i64 64, i64* %__UNIQUE_ID___y5, align 8
  %19 = load i64, i64* %__UNIQUE_ID___x4, align 8
  %20 = load i64, i64* %__UNIQUE_ID___y5, align 8
  %cmp17 = icmp ult i64 %19, %20
  br i1 %cmp17, label %cond.true, label %cond.false

cond.true:                                        ; preds = %for.end
  %21 = load i64, i64* %__UNIQUE_ID___x4, align 8
  br label %cond.end

cond.false:                                       ; preds = %for.end
  %22 = load i64, i64* %__UNIQUE_ID___y5, align 8
  br label %cond.end

cond.end:                                         ; preds = %cond.false, %cond.true
  %cond = phi i64 [ %21, %cond.true ], [ %22, %cond.false ]
  store i64 %cond, i64* %tmp, align 8
  %23 = load i64, i64* %tmp, align 8
  %arrayidx18 = getelementptr i8, i8* %17, i64 %23
  store i8 0, i8* %arrayidx18, align 1
  ret i32 64
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_subreg(i64 %a.coerce0, i64 %a.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %a to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  %5 = load i64, i64* %4, align 8
  %6 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  %7 = load i64, i64* %6, align 8
  %call = call { i64, i64 } @tnum_cast(i64 %5, i64 %7, i8 noundef zeroext 4) #4
  %8 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %9 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %8, i32 0, i32 0
  %10 = extractvalue { i64, i64 } %call, 0
  store i64 %10, i64* %9, align 8
  %11 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %8, i32 0, i32 1
  %12 = extractvalue { i64, i64 } %call, 1
  store i64 %12, i64* %11, align 8
  %13 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %14 = load { i64, i64 }, { i64, i64 }* %13, align 8
  ret { i64, i64 } %14
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_clear_subreg(i64 %a.coerce0, i64 %a.coerce1) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %agg.tmp = alloca %struct.tnum, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  %3 = bitcast %struct.tnum* %a to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  %5 = load i64, i64* %4, align 8
  %6 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  %7 = load i64, i64* %6, align 8
  %call = call { i64, i64 } @tnum_rshift(i64 %5, i64 %7, i8 noundef zeroext 32) #4
  %8 = bitcast %struct.tnum* %agg.tmp to { i64, i64 }*
  %9 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %8, i32 0, i32 0
  %10 = extractvalue { i64, i64 } %call, 0
  store i64 %10, i64* %9, align 8
  %11 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %8, i32 0, i32 1
  %12 = extractvalue { i64, i64 } %call, 1
  store i64 %12, i64* %11, align 8
  %13 = bitcast %struct.tnum* %agg.tmp to { i64, i64 }*
  %14 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %13, i32 0, i32 0
  %15 = load i64, i64* %14, align 8
  %16 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %13, i32 0, i32 1
  %17 = load i64, i64* %16, align 8
  %call1 = call { i64, i64 } @tnum_lshift(i64 %15, i64 %17, i8 noundef zeroext 32) #4
  %18 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %19 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %18, i32 0, i32 0
  %20 = extractvalue { i64, i64 } %call1, 0
  store i64 %20, i64* %19, align 8
  %21 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %18, i32 0, i32 1
  %22 = extractvalue { i64, i64 } %call1, 1
  store i64 %22, i64* %21, align 8
  %23 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %24 = load { i64, i64 }, { i64, i64 }* %23, align 8
  ret { i64, i64 } %24
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define dso_local { i64, i64 } @tnum_const_subreg(i64 %a.coerce0, i64 %a.coerce1, i32 noundef %value) #0 {
entry:
  %retval = alloca %struct.tnum, align 8
  %a = alloca %struct.tnum, align 8
  %value.addr = alloca i32, align 4
  %agg.tmp = alloca %struct.tnum, align 8
  %agg.tmp1 = alloca %struct.tnum, align 8
  %0 = bitcast %struct.tnum* %a to { i64, i64 }*
  %1 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  store i64 %a.coerce0, i64* %1, align 8
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  store i64 %a.coerce1, i64* %2, align 8
  store i32 %value, i32* %value.addr, align 4
  %3 = bitcast %struct.tnum* %a to { i64, i64 }*
  %4 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 0
  %5 = load i64, i64* %4, align 8
  %6 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %3, i32 0, i32 1
  %7 = load i64, i64* %6, align 8
  %call = call { i64, i64 } @tnum_clear_subreg(i64 %5, i64 %7) #4
  %8 = bitcast %struct.tnum* %agg.tmp to { i64, i64 }*
  %9 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %8, i32 0, i32 0
  %10 = extractvalue { i64, i64 } %call, 0
  store i64 %10, i64* %9, align 8
  %11 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %8, i32 0, i32 1
  %12 = extractvalue { i64, i64 } %call, 1
  store i64 %12, i64* %11, align 8
  %13 = load i32, i32* %value.addr, align 4
  %conv = zext i32 %13 to i64
  %call2 = call { i64, i64 } @tnum_const(i64 noundef %conv) #4
  %14 = bitcast %struct.tnum* %agg.tmp1 to { i64, i64 }*
  %15 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %14, i32 0, i32 0
  %16 = extractvalue { i64, i64 } %call2, 0
  store i64 %16, i64* %15, align 8
  %17 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %14, i32 0, i32 1
  %18 = extractvalue { i64, i64 } %call2, 1
  store i64 %18, i64* %17, align 8
  %19 = bitcast %struct.tnum* %agg.tmp to { i64, i64 }*
  %20 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %19, i32 0, i32 0
  %21 = load i64, i64* %20, align 8
  %22 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %19, i32 0, i32 1
  %23 = load i64, i64* %22, align 8
  %24 = bitcast %struct.tnum* %agg.tmp1 to { i64, i64 }*
  %25 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %24, i32 0, i32 0
  %26 = load i64, i64* %25, align 8
  %27 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %24, i32 0, i32 1
  %28 = load i64, i64* %27, align 8
  %call3 = call { i64, i64 } @tnum_or(i64 %21, i64 %23, i64 %26, i64 %28) #4
  %29 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %30 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %29, i32 0, i32 0
  %31 = extractvalue { i64, i64 } %call3, 0
  store i64 %31, i64* %30, align 8
  %32 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %29, i32 0, i32 1
  %33 = extractvalue { i64, i64 } %call3, 1
  store i64 %33, i64* %32, align 8
  %34 = bitcast %struct.tnum* %retval to { i64, i64 }*
  %35 = load { i64, i64 }, { i64, i64 }* %34, align 8
  ret { i64, i64 } %35
}

; Function Attrs: noinline noredzone nounwind null_pointer_is_valid sspstrong
define internal i32 @generic___fls___(i64 noundef %word) #0 {
entry:
  %word.addr = alloca i64, align 8
  %num = alloca i32, align 4
  store i64 %word, i64* %word.addr, align 8
  store i32 63, i32* %num, align 4
  %0 = load i64, i64* %word.addr, align 8
  %and = and i64 %0, -4294967296
  %tobool = icmp ne i64 %and, 0
  br i1 %tobool, label %if.end, label %if.then

if.then:                                          ; preds = %entry
  %1 = load i32, i32* %num, align 4
  %sub = sub i32 %1, 32
  store i32 %sub, i32* %num, align 4
  %2 = load i64, i64* %word.addr, align 8
  %shl = shl i64 %2, 32
  store i64 %shl, i64* %word.addr, align 8
  br label %if.end

if.end:                                           ; preds = %if.then, %entry
  %3 = load i64, i64* %word.addr, align 8
  %and1 = and i64 %3, -281474976710656
  %tobool2 = icmp ne i64 %and1, 0
  br i1 %tobool2, label %if.end6, label %if.then3

if.then3:                                         ; preds = %if.end
  %4 = load i32, i32* %num, align 4
  %sub4 = sub i32 %4, 16
  store i32 %sub4, i32* %num, align 4
  %5 = load i64, i64* %word.addr, align 8
  %shl5 = shl i64 %5, 16
  store i64 %shl5, i64* %word.addr, align 8
  br label %if.end6

if.end6:                                          ; preds = %if.then3, %if.end
  %6 = load i64, i64* %word.addr, align 8
  %and7 = and i64 %6, -72057594037927936
  %tobool8 = icmp ne i64 %and7, 0
  br i1 %tobool8, label %if.end12, label %if.then9

if.then9:                                         ; preds = %if.end6
  %7 = load i32, i32* %num, align 4
  %sub10 = sub i32 %7, 8
  store i32 %sub10, i32* %num, align 4
  %8 = load i64, i64* %word.addr, align 8
  %shl11 = shl i64 %8, 8
  store i64 %shl11, i64* %word.addr, align 8
  br label %if.end12

if.end12:                                         ; preds = %if.then9, %if.end6
  %9 = load i64, i64* %word.addr, align 8
  %and13 = and i64 %9, -1152921504606846976
  %tobool14 = icmp ne i64 %and13, 0
  br i1 %tobool14, label %if.end18, label %if.then15

if.then15:                                        ; preds = %if.end12
  %10 = load i32, i32* %num, align 4
  %sub16 = sub i32 %10, 4
  store i32 %sub16, i32* %num, align 4
  %11 = load i64, i64* %word.addr, align 8
  %shl17 = shl i64 %11, 4
  store i64 %shl17, i64* %word.addr, align 8
  br label %if.end18

if.end18:                                         ; preds = %if.then15, %if.end12
  %12 = load i64, i64* %word.addr, align 8
  %and19 = and i64 %12, -4611686018427387904
  %tobool20 = icmp ne i64 %and19, 0
  br i1 %tobool20, label %if.end24, label %if.then21

if.then21:                                        ; preds = %if.end18
  %13 = load i32, i32* %num, align 4
  %sub22 = sub i32 %13, 2
  store i32 %sub22, i32* %num, align 4
  %14 = load i64, i64* %word.addr, align 8
  %shl23 = shl i64 %14, 2
  store i64 %shl23, i64* %word.addr, align 8
  br label %if.end24

if.end24:                                         ; preds = %if.then21, %if.end18
  %15 = load i64, i64* %word.addr, align 8
  %and25 = and i64 %15, -9223372036854775808
  %tobool26 = icmp ne i64 %and25, 0
  br i1 %tobool26, label %if.end29, label %if.then27

if.then27:                                        ; preds = %if.end24
  %16 = load i32, i32* %num, align 4
  %sub28 = sub i32 %16, 1
  store i32 %sub28, i32* %num, align 4
  br label %if.end29

if.end29:                                         ; preds = %if.then27, %if.end24
  %17 = load i32, i32* %num, align 4
  ret i32 %17
}

attributes #0 = { noinline noredzone nounwind null_pointer_is_valid sspstrong "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+retpoline-external-thunk,+retpoline-indirect-branches,+retpoline-indirect-calls,-3dnow,-3dnowa,-aes,-avx,-avx2,-avx512bf16,-avx512bitalg,-avx512bw,-avx512cd,-avx512dq,-avx512er,-avx512f,-avx512fp16,-avx512ifma,-avx512pf,-avx512vbmi,-avx512vbmi2,-avx512vl,-avx512vnni,-avx512vp2intersect,-avx512vpopcntdq,-avxvnni,-f16c,-fma,-fma4,-gfni,-kl,-mmx,-pclmul,-sha,-sse,-sse2,-sse3,-sse4.1,-sse4.2,-sse4a,-ssse3,-vaes,-vpclmulqdq,-widekl,-x87,-xop" "tune-cpu"="generic" "warn-stack-size"="2048" }
attributes #1 = { argmemonly nofree nounwind willreturn }
attributes #2 = { argmemonly nofree nounwind willreturn writeonly }
attributes #3 = { noredzone null_pointer_is_valid "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+retpoline-external-thunk,+retpoline-indirect-branches,+retpoline-indirect-calls,-3dnow,-3dnowa,-aes,-avx,-avx2,-avx512bf16,-avx512bitalg,-avx512bw,-avx512cd,-avx512dq,-avx512er,-avx512f,-avx512fp16,-avx512ifma,-avx512pf,-avx512vbmi,-avx512vbmi2,-avx512vl,-avx512vnni,-avx512vp2intersect,-avx512vpopcntdq,-avxvnni,-f16c,-fma,-fma4,-gfni,-kl,-mmx,-pclmul,-sha,-sse,-sse2,-sse3,-sse4.1,-sse4.2,-sse4a,-ssse3,-vaes,-vpclmulqdq,-widekl,-x87,-xop" "tune-cpu"="generic" }
attributes #4 = { noredzone }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 2}
!1 = !{i32 1, !"Code Model", i32 2}
!2 = !{i32 1, !"override-stack-alignment", i32 8}
!3 = !{i32 4, !"SkipRaxSetup", i32 1}
!4 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
!5 = distinct !{!5, !6}
!6 = !{!"llvm.loop.mustprogress"}
!7 = distinct !{!7, !6}
