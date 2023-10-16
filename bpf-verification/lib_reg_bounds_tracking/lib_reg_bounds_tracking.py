from z3 import *
import itertools
import sys
import re
from _collections_abc import MutableSequence
import ctypes
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes
from pprint import pprint
from itertools import chain, combinations
from packaging import version
from termcolor import colored
import time
import os
import os.path
import json
import time   



BITVEC_WIDTH_64 = 64
BITVEC_WIDTH_32 = 32
BITVEC_WIDTH_1 = 1

# limits.h
U64_MIN = 0
U64_MAX = int("1"*BITVEC_WIDTH_64, 2)
U32_MIN = 0
U32_MAX = int("1"*BITVEC_WIDTH_32, 2)
S64_MIN = int(("1" + "0"*(BITVEC_WIDTH_64 - 1)), 2)
S64_MAX = int("1"*(BITVEC_WIDTH_64 - 1), 2)
S32_MIN = int(("1" + "0"*(BITVEC_WIDTH_32 - 1)), 2)
S32_MAX = int("1"*(BITVEC_WIDTH_32 - 1), 2)

#  https://stackoverflow.com/a/3488283/3418445


class FormulaBuilder(MutableSequence):

    def __init__(self, *args):
        self.list = list()
        self.extend(list(args))

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]

    def __setitem__(self, i, v):
        self.list[i] = v

    def insert(self, i, v):
        self.list.insert(i, v)

    def __str__(self):
        return str(self.list)

    def print_spec(self):
        for v in self.list:
            print("----------")
            print(str(v))
            print("----------")


# sign
SIGNED = 1
UNSIGNED = 0


class BitVecHelper:

    uniq_id = 0
    # { bitvector: [property list] }
    bitvec_map = {}
    model = None

    # index into property list
    BITVECHELPER_BITVECTOR_IDX = 0
    BITVECHELPER_SIGN_IDX = 1
    BITVECHELPER_MODELVAL_IDX = 2
    BITVECHELPER_MODELVAL_SIGNED_IDX = 3

    class BVProperty:

        def __init__(self, bv, width, sign):
            self.bv = bv
            self.width = width
            self.sign = sign
            self.model_value = None
            self.model_value_signed = None

        def __repr__(self):
            s = "{} ({}, {})".format(str(self.bv), str(self.width),
                                     "S" if (self.sign == SIGNED) else "U")
            return s

    @staticmethod
    def new_bitvec(name, width, sign):
        bv = BitVec(name, width)
        # create property list
        BitVecHelper.bitvec_map[name] = BitVecHelper.BVProperty(
            bv, width, sign)
        return bv

    @staticmethod
    def new_uniq_bitvec(name, width, sign):
        BitVecHelper.uniq_id += 1
        bitvec_name = name+"_"+str(BitVecHelper.uniq_id)
        bv = BitVec(bitvec_name, width)
        # create property list
        BitVecHelper.bitvec_map[bitvec_name] = BitVecHelper.BVProperty(
            bv, width, sign)
        return bv

    @staticmethod
    def update_bitvec_ref(oldname, newname):
        oldbvprop = BitVecHelper.bitvec_map[oldname]
        newbv = BitVec(newname, oldbvprop.bv.sort().size())
        BitVecHelper.bitvec_map[newname] = BitVecHelper.BVProperty(
            newbv, newbv.sort().size(), oldbvprop.sign)
        BitVecHelper.bitvec_map.pop(oldname)
        return newbv

    def update_map_with_model(m):
        BitVecHelper.model = m

        # make sure model contains assignments to all bitvectors we created
        for bvname, bvprop in BitVecHelper.bitvec_map.items():
            BitVecHelper.model.evaluate(bvprop.bv, model_completion=True)

        # now update the each key in bitvec_map with its value from the model
        for modelvalue in BitVecHelper.model:
            try:
                bvprop = BitVecHelper.bitvec_map[str(modelvalue)]
                # print(modelvalue, BitVecHelper.model[modelvalue], bvprop)
            except KeyError:
                # print(modelvalue)
                continue
            bvprop.model_value = m[modelvalue].as_long()
            if bvprop.sign == SIGNED:
                if bvprop.bv.sort().size() == BITVEC_WIDTH_32:
                    int32_val = ctypes.c_int32(bvprop.model_value).value
                    bvprop.model_value_signed = int32_val
                elif bvprop.bv.sort().size() == BITVEC_WIDTH_64:
                    int64_val = ctypes.c_int64(bvprop.model_value).value
                    bvprop.model_value_signed = int64_val
            else:
                bvprop.model_value_signed = bvprop.model_value


    def get_bitvec_map_with_model_as_table():
        assert (BitVecHelper.model is not None)
        t = PrettyTable(
            ['bitvector', 'signed?', 'modelval', 'actualval'])
        t.align = "r"
        for bvname, bvprop in BitVecHelper.bitvec_map.items():
            t.add_row([
                str(bvprop.bv),
                "S" if (bvprop.sign == SIGNED) else "U",
                str(bvprop.model_value),
                str(bvprop.model_value_signed)
            ])
        return t

    def clear_map():
        BitVecHelper.bitvec_map = {}


class Tnum:

    @staticmethod
    def contains(x, tvalue, tmask):
        return tvalue == x & ~tmask

    @staticmethod
    def tnum_equals(a, b):
        return And((a.value == b.value), (a.mask == b.mask))

    @staticmethod
    def tnum_string(tvalue, tmask, width):
        assert type(tvalue) == z3.z3.BitVecNumRef
        assert type(tmask) == z3.z3.BitVecNumRef
        s = []
        for i in range(width):
            l = 1 << i
            v = tvalue & l
            m = tmask & l
            if (simplify(v == 0) and
                    simplify(m != 0)):
                s.insert(0, "x")
            elif (simplify(v == 0) and
                  simplify(m == 0)):
                s.insert(0, "0")
            elif (simplify(v != 0) and
                  simplify(m == 0)):
                s.insert(0, "1")
            else:
                raise AssertionError("not wellformed")
        return "".join(s)

    @staticmethod
    def tnum_string_2(tvalue, tmask, width):
        s = []
        # print(format(tvalue, '064b'))
        # print(format(tmask, '064b'))
        for i in range(width):
            l = 1 << i
            v = (tvalue & l) >> i
            m = (tmask & l) >> i
            if (v == 0) and (m == 1):
                s.insert(0, "x")
            elif (v == 0) and (m == 0):
                s.insert(0, "0")
            elif (v == 1) and (m == 0):
                s.insert(0, "1")
            else:
                raise AssertionError("not wellformed")
        return "".join(s)

#concrete and abstract domains in one bpf register class
class bpf_register:
    
    def __init__(self, reg_name = "none"):
        self.name = reg_name
        #self.conc_state = self.conc_reg_state(reg_name)
        #concrete value in register (32 and 64)
        self.conc64 = BitVecHelper.new_bitvec(reg_name + "_conc64", BITVEC_WIDTH_64, UNSIGNED)
        self.conc32 = BitVecHelper.new_bitvec(reg_name + "_conc32", BITVEC_WIDTH_32, UNSIGNED)
        self.var_off_value = BitVecHelper.new_uniq_bitvec(
            "var_off_value", BITVEC_WIDTH_64,  UNSIGNED)
        self.var_off_mask = BitVecHelper.new_uniq_bitvec(
            "var_off_mask", BITVEC_WIDTH_64,  UNSIGNED)
        self.smin_value = BitVecHelper.new_uniq_bitvec(
            "smin_value", BITVEC_WIDTH_64,  SIGNED)
        self.smax_value = BitVecHelper.new_uniq_bitvec(
            "smax_value", BITVEC_WIDTH_64, SIGNED)
        self.umin_value = BitVecHelper.new_uniq_bitvec(
            "umin_value", BITVEC_WIDTH_64,  UNSIGNED)
        self.umax_value = BitVecHelper.new_uniq_bitvec(
            "umax_value", BITVEC_WIDTH_64,  UNSIGNED)
        self.s32_min_value = BitVecHelper.new_uniq_bitvec(
            "s32_min_value", BITVEC_WIDTH_32,  SIGNED)
        self.s32_max_value = BitVecHelper.new_uniq_bitvec(
            "s32_max_value", BITVEC_WIDTH_32, SIGNED)
        self.u32_min_value = BitVecHelper.new_uniq_bitvec(
            "u32_min_value", BITVEC_WIDTH_32,  UNSIGNED)
        self.u32_max_value = BitVecHelper.new_uniq_bitvec(
            "u32_max_value", BITVEC_WIDTH_32,  UNSIGNED)
    
    def _get_bv_name(self):
        bvname = self.bv_name_prefix + "_" + str(self.num_start_id_counter)
        self.num_start_id_counter += 1
        return bvname


    def get_contains64_predicate_tnum(self):
        f = []
        f.append(Tnum.contains(self.conc64, self.var_off_value,
                            self.var_off_mask))
        f.append(self.var_off_value & self.var_off_mask == 0)
        return And(f)

    def get_contains64_predicate_only_unsigned(self):
        f = []
        f.append(ULE(self.umin_value, self.conc64))
        f.append(ULE(self.conc64, self.umax_value))
        return And(f)

    def get_contains64_predicate_only_signed(self):
        f = []
        f.append(self.smin_value <= self.conc64)
        f.append(self.conc64 <= self.smax_value)
        return And(f)

    def get_contains64_predicate(self):
        f = []
        f.append(self.get_contains64_predicate_only_signed())
        f.append(self.get_contains64_predicate_only_unsigned())
        f.append(Tnum.contains(self.conc64, self.var_off_value,
                            self.var_off_mask))
        f.append(self.var_off_value & self.var_off_mask == 0)
        return And(f)

    def get_contains32_predicate_only_unsigned(self):
        f = []
        f.append(ULE(self.u32_min_value, self.conc32))
        f.append(ULE(self.conc32, self.u32_max_value))
        return And(f)

    def get_contains32_predicate_only_signed(self):
        f = []
        f.append(self.s32_min_value <= self.conc32)
        f.append(self.conc32 <= self.s32_max_value)
        return And(f)

    def get_contains32_predicate(self):
        f = []
        f.append(self.get_contains32_predicate_only_unsigned())
        f.append(self.get_contains32_predicate_only_signed())
        return And(f)

    def get_equate_predicates(self, other):
        f = []
        f.append(self.conc32 == other.conc32)
        f.append(self.conc64 == other.conc64)
        f.append(self.var_off_value == other.var_off_value)
        f.append(self.var_off_mask == other.var_off_mask)
        f.append(self.smin_value == other.smin_value)
        f.append(self.smax_value == other.smax_value)
        f.append(self.umin_value == other.umin_value)
        f.append(self.umax_value == other.umax_value)
        f.append(self.s32_min_value == other.s32_min_value)
        f.append(self.s32_max_value == other.s32_max_value)
        f.append(self.u32_min_value == other.u32_min_value)
        f.append(self.u32_max_value == other.u32_max_value)
        return And(f)

    def update_bv_for_field(self, field, oldname, newname):
        if field not in self.__dict__:
            raise KeyError
        self.__dict__[field] = BitVecHelper.update_bitvec_ref(oldname, newname)

    def update_bv_mappings(self, new_mappings_list, kernver):
        #don't need 32 bit domains in kernel versions prior to 5.7rc1 - they also don't exist in json mapping
        if version.parse(kernver) < version.parse("5.7-rc1"):
            self.update_bv_for_field(
                "var_off_value", self.var_off_value.__str__(), new_mappings_list[0][0])
            self.update_bv_for_field(
                "var_off_mask", self.var_off_mask.__str__(), new_mappings_list[0][1])
            self.update_bv_for_field(
                "smin_value", self.smin_value.__str__(), new_mappings_list[1])
            self.update_bv_for_field(
                "smax_value", self.smax_value.__str__(), new_mappings_list[2])
            self.update_bv_for_field(
                "umin_value", self.umin_value.__str__(), new_mappings_list[3])
            self.update_bv_for_field(
                "umax_value", self.umax_value.__str__(), new_mappings_list[4])
        else:
            self.update_bv_for_field(
                "var_off_value", self.var_off_value.__str__(), new_mappings_list[0][0])
            self.update_bv_for_field(
                "var_off_mask", self.var_off_mask.__str__(), new_mappings_list[0][1])
            self.update_bv_for_field(
                "smin_value", self.smin_value.__str__(), new_mappings_list[1])
            self.update_bv_for_field(
                "smax_value", self.smax_value.__str__(), new_mappings_list[2])
            self.update_bv_for_field(
                "umin_value", self.umin_value.__str__(), new_mappings_list[3])
            self.update_bv_for_field(
                "umax_value", self.umax_value.__str__(), new_mappings_list[4])
            self.update_bv_for_field(
                "s32_min_value", self.s32_min_value.__str__(), new_mappings_list[5])
            self.update_bv_for_field(
                "s32_max_value", self.s32_max_value.__str__(), new_mappings_list[6])
            self.update_bv_for_field(
                "u32_min_value", self.u32_min_value.__str__(), new_mappings_list[7])
            self.update_bv_for_field(
                "u32_max_value", self.u32_max_value.__str__(), new_mappings_list[8])

    #function to set all bpf_reg state to a known value
    def singleton(self, known_val = None):
        #all abstract domain values are set to particular value except tnum mask which is set to 0
        if(known_val != None):
            return And(
            self.var_off_value 	== known_val,
            self.var_off_mask 	== 0,
            self.smin_value 	== known_val,
            self.smax_value 	== known_val,
            self.umin_value 	== known_val,
            self.umax_value		== known_val,
            self.s32_min_value	== known_val,
            self.s32_max_value 	== known_val,
            self.u32_min_value 	== known_val, 
            self.u32_max_value 	== known_val)
        else:
            return And(
            self.var_off_value 	== self.conc64,
            self.var_off_mask 	== 0,
            self.smin_value 	== self.conc64,
            self.smax_value 	== self.conc64,
            self.umin_value 	== self.conc64,
            self.umax_value		== self.conc64,
            self.s32_min_value	== self.conc32,
            self.s32_max_value 	== self.conc32,
            self.u32_min_value 	== self.conc32, 
            self.u32_max_value 	== self.conc32)

    #function to set all bpf_reg state to unknown
    def fully_unknown(self):
        #all abstract domain values are set to min/max values and tnum mask set to all ones
        return And(
            self.var_off_value 	== 0,
            self.var_off_mask 	== U64_MAX,
            self.smin_value 	== S64_MIN,
            self.smax_value 	== S64_MAX,
            self.umin_value 	== U64_MIN,
            self.umax_value		== U64_MAX,
            self.s32_min_value	== S32_MIN,
            self.s32_max_value 	== S32_MAX,
            self.u32_min_value 	== U32_MIN, 
            self.u32_max_value 	== U32_MAX)


#class to keep track of process statistics
class process_stats:
    def __init__(self):
        self.timeout_counter = 0
        self.exception_counter = 0
        self.prog = 0
        self.prog_size = 0
        self.total_progs = 0
        self.iteration = 1
        self.invalid_counter = 0
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = time.time()
        self.tmp_elapsed_time = time.time()
        self.prog_execution_time = time.time()
        self.failed_unknown_prog_list = []
        self.failed_exception_prog_list = []
        self.eval_dict = {}
        
    def set_execution_time(self):
        self.prog_execution_time = self.end_time - self.start_time
    def set_elapsed_time(self):
        self.tmp_elapsed_time = self.end_time - self.elapsed_time


    def print_verification_stats(self):
        #print("\n################# VERIFICATION STATS ########################")
        #print("Iteration " + str(self.iteration) + " out of " + self.total_progs)
        #print("\nOverall elapsed time in minutes", self.tmp_elapsed_time / 60 )
        #print("Program execution time in minutes", self.prog_execution_time / 60)
        #print("\nEvaluation Dictionary: time per prog (seconds), sat/unsat, bug types")
        #pprint(self.eval_dict)

        table = ColorTable()
        table = ColorTable(theme=Themes.OCEAN)
        table.field_names = ["Instruction", "Sound?", "u64", "s64", "tnum", "u32", "s32", "Execution time (seconds)"]
        abs_domains = ["unsigned_64", "signed_64", "Tnum", "unsigned_32", "signed_32"]
        violations = [0] * 5 
        for c in self.eval_dict.keys():
            #formatting insn name for table (the splicing is for the SRO sync,sync format)
            insn_name = c if len(c) < 15 else c[18:]
            #use sat/unsat for checkmarking soundness
            soundness = "✓" if self.eval_dict[c][1] == "unsat" else "✘"
            #checkboxes for domains violated
            for i,x in enumerate(abs_domains):
                violations[i] = "✘" if x in self.eval_dict[c][2] else "✓"
            table.add_row([insn_name, soundness, violations[0], violations[1], violations[2], violations[3], violations[4], round(self.eval_dict[c][0], 2)])
        
        print(table)
        #print("###########################################################\n")
    
    def print_verification_aggregate(self, usr_config):

        print("\n\nVerification Aggregate Statistics")
        gen_sound = "✓" if usr_config.gen_violations == 0 else "✘"
        sro_sound = "✓" if usr_config.sro_violations == 0 else "✘"
        table = PrettyTable()

        table.field_names = ["KernVer", "gen Sound?", "sro Sound?", "gen Viol.", "sro Viol.", "gen Unsound Ops", "sro Unsound Ops"]
        table.add_row([usr_config.kernel_ver, gen_sound, sro_sound, usr_config.gen_violations, usr_config.sro_violations, usr_config.gen_unsound_insn, usr_config.sro_unsound_insn])
        
        print(table)
        with open(usr_config.write_path  + "stats" + ".txt", 'w') as w:
            w.write("\n\nVerification Aggregate Statistics\n")
            w.write(str(table))
        #print("###########################################################\n")


    def print_synthesis_aggregate(self, usr_config):

        print("\n\nSynthesis Aggregate Statistics")
        all_poc_syn = "✓" if usr_config.synth_violations == usr_config.sro_violations else "✘"
        table = PrettyTable()

        table.field_names = ["KernVer", "# Tot. Viol.", "All POCs Synthesized?", "Prog Len 1", "Prog Len 2", "Prog Len 3"]
        table.add_row([usr_config.kernel_ver, usr_config.sro_violations, all_poc_syn, usr_config.synth_len1, usr_config.synth_len2, usr_config.synth_len3])
        
        print(table)
        with open(usr_config.write_path  + "stats" + ".txt", 'a') as w:
            w.write("\n\nSynthesis Aggregate Statistics\n")
            w.write(str(table))
            w.write("\n")
        #print("###########################################################\n")

    def write_dict_to_file(self, usr_config, func_name):
        try:
            os.mkdir(usr_config.write_path)
        except:
            pass
        with open(usr_config.write_path + usr_config.kernel_ver + "_" + func_name + ".txt", "w") as f:
            f.write(json.dumps(self.eval_dict))

    def print_synthesis_stats(self):
        print("\n################## SYNTHESIS STATS #########################")
        print("Program run: ", str(self.prog))
        print("Iteration " + str(self.iteration) + " out of " + self.total_progs)
        print("Overall elapsed time in minutes", self.tmp_elapsed_time / 60 )
        print("Program execution time in minutes", self.prog_execution_time / 60)
        print("\nEvaluation Dictionary: time per prog (seconds), sat/unsat, bug types")
        pprint(self.eval_dict)
        print("###########################################################\n")



#setup class for setting configurations for synthesis/verification
class config_setup:
    def __init__(self, config_file):
        self.gen_violations = 0
        self.gen_unsound_insn = 0
        self.sro_violations = 0
        self.sro_unsound_insn= 0
        self.synth_violations = 0
        self.synth_len1 = 0
        self.synth_len2= 0
        self.synth_len3= 0
        self.json_offset = config_file["json_offset"]
        self.kernel_ver = config_file["kernel_ver"]
        self.encodings_path = config_file["bpf_encodings_path"] + "/" 
        self.write_path = config_file["write_dir_path"] + "/" + config_file["kernel_ver"] + "_res/"
        self.num_iter = config_file["num_synthesis_iter"]
        self.OP_to_smt_file_map = {
            "BPF_SYNC":     self.encodings_path + "BPF_SYNC.smt2",
            "BPF_OR":       self.encodings_path + "BPF_OR.smt2",
            "BPF_AND":      self.encodings_path + "BPF_AND.smt2",
            "BPF_XOR":      self.encodings_path + "BPF_XOR.smt2",
            "BPF_LSH":      self.encodings_path + "BPF_LSH.smt2",
            "BPF_RSH":      self.encodings_path + "BPF_RSH.smt2",
            "BPF_ARSH":     self.encodings_path + "BPF_ARSH.smt2",
            "BPF_ADD":      self.encodings_path + "BPF_ADD.smt2",
            "BPF_SUB":      self.encodings_path + "BPF_SUB.smt2",
            "BPF_JLT":      self.encodings_path + "BPF_JLT.smt2",
            "BPF_JLE":      self.encodings_path + "BPF_JLE.smt2",
            "BPF_JSLT":     self.encodings_path + "BPF_JSLT.smt2",
            "BPF_JSLE":     self.encodings_path + "BPF_JSLE.smt2",
            "BPF_JEQ":      self.encodings_path + "BPF_JEQ.smt2",
            "BPF_JNE":      self.encodings_path + "BPF_JNE.smt2",
            "BPF_JGE":      self.encodings_path + "BPF_JGE.smt2",
            "BPF_JGT":      self.encodings_path + "BPF_JGT.smt2",
            "BPF_JSGE":     self.encodings_path + "BPF_JSGE.smt2",
            "BPF_JSGT":     self.encodings_path + "BPF_JSGT.smt2",
            "BPF_OR_32":       self.encodings_path + "BPF_OR_32.smt2",
            "BPF_AND_32":      self.encodings_path + "BPF_AND_32.smt2",
            "BPF_XOR_32":      self.encodings_path + "BPF_XOR_32.smt2",
            "BPF_LSH_32":      self.encodings_path + "BPF_LSH_32.smt2",
            "BPF_RSH_32":      self.encodings_path + "BPF_RSH_32.smt2",
            "BPF_ARSH_32":     self.encodings_path + "BPF_ARSH_32.smt2",
            "BPF_ADD_32":      self.encodings_path + "BPF_ADD_32.smt2",
            "BPF_SUB_32":      self.encodings_path + "BPF_SUB_32.smt2",
            "BPF_JLT_32":      self.encodings_path + "BPF_JLT_32.smt2",
            "BPF_JLE_32":      self.encodings_path + "BPF_JLE_32.smt2",
            "BPF_JSLT_32":     self.encodings_path + "BPF_JSLT_32.smt2",
            "BPF_JSLE_32":     self.encodings_path + "BPF_JSLE_32.smt2",
            "BPF_JEQ_32":      self.encodings_path + "BPF_JEQ_32.smt2",
            "BPF_JNE_32":      self.encodings_path + "BPF_JNE_32.smt2",
            "BPF_JGE_32":      self.encodings_path + "BPF_JGE_32.smt2",
            "BPF_JGT_32":      self.encodings_path + "BPF_JGT_32.smt2",
            "BPF_JSGE_32":     self.encodings_path + "BPF_JSGE_32.smt2",
            "BPF_JSGT_32":     self.encodings_path + "BPF_JSGT_32.smt2"
            }
        #synthesis insn set pool
        if isinstance(config_file["insn_set"], list):
            insn_set = set()
            for i in config_file["insn_set"]:
                insn_set.add(i)	
            self.OPS_set = insn_set
        else:
            self.set_ops(config_file["insn_set"])
        #initial insn set for verification - this will become the nth set for
        #synthesis after sound instructions are pruned away. By default should
        #be same as ops_set but can differ if some specific insns are of
        #interest.
        if isinstance(config_file["verification_set"], list):
            verification_set = set()
            for i in config_file["verification_set"]:
                verification_set.add(i)
            self.insn_set_list = [verification_set]
        else:
            self.insn_set_list = [self.OPS_set]
        
            self.insn_set_list = [self.OPS_set]
        self.bugs_dict = {}
        self.set_bug_type_dict()
        

    #setting which bpf_ops to use 32/64 or some specific
    def set_ops(self, mode):
        if mode == "ALL":
            self.OPS_set = {"BPF_AND", "BPF_OR", "BPF_LSH", "BPF_RSH", "BPF_JLT", "BPF_JLE", "BPF_JEQ", "BPF_JNE", "BPF_JGE", "BPF_JGT", "BPF_JSGE", "BPF_JSGT", "BPF_JSLT", "BPF_JSLE", "BPF_ADD", "BPF_SUB", "BPF_XOR", "BPF_ARSH",
            "BPF_OR_32", "BPF_AND_32", "BPF_LSH_32", "BPF_RSH_32", "BPF_ADD_32", "BPF_SUB_32", "BPF_XOR_32","BPF_ARSH_32", "BPF_JLT_32",  "BPF_JLE_32", "BPF_JSLT_32", "BPF_JSLE_32", "BPF_JEQ_32", "BPF_JNE_32", "BPF_JGE_32", "BPF_JGT_32", "BPF_JSGE_32", "BPF_JSGT_32"}
        elif mode == "ALL32":
            self.OPS_set = {"BPF_OR_32", "BPF_AND_32", "BPF_LSH_32", "BPF_RSH_32", "BPF_ADD_32", "BPF_SUB_32", "BPF_XOR_32","BPF_ARSH_32", "BPF_JLT_32",  "BPF_JLE_32", "BPF_JSLT_32", "BPF_JSLE_32", "BPF_JEQ_32", "BPF_JNE_32", "BPF_JGE_32", "BPF_JGT_32", "BPF_JSGE_32", "BPF_JSGT_32"}
        elif mode =="JMP32":
            self.OPS_set = {"BPF_JLT_32",  "BPF_JLE_32", "BPF_JSLT_32", "BPF_JSLE_32", "BPF_JEQ_32", "BPF_JNE_32", "BPF_JGE_32", "BPF_JGT_32", "BPF_JSGE_32", "BPF_JSGT_32"}
        elif mode =="ALU32":
            self.OPS_set = {"BPF_OR_32", "BPF_AND_32", "BPF_LSH_32", "BPF_RSH_32", "BPF_ADD_32", "BPF_SUB_32", "BPF_XOR_32","BPF_ARSH_32"}
        elif mode == "ALL64":
            self.OPS_set = {"BPF_AND", "BPF_OR", "BPF_LSH", "BPF_RSH", "BPF_JLT", "BPF_JLE", "BPF_JEQ", "BPF_JNE", "BPF_JGE", "BPF_JGT", "BPF_JSGE", "BPF_JSGT", "BPF_JSLT", "BPF_JSLE", "BPF_ADD", "BPF_SUB", "BPF_XOR", "BPF_ARSH"}
        elif mode =="JMP64":
            self.OPS_set = {"BPF_JLT", "BPF_JLE", "BPF_JEQ", "BPF_JNE", "BPF_JGE", "BPF_JGT", "BPF_JSGE", "BPF_JSGT", "BPF_JSLT", "BPF_JSLE"}
        elif mode =="ALU64":
            self.OPS_set = {"BPF_AND", "BPF_OR", "BPF_LSH", "BPF_RSH", "BPF_ADD", "BPF_SUB", "BPF_XOR", "BPF_ARSH"}

    #set bug type dictionary in case nothing was passed into function
    def set_bug_type_dict(self):
        for key in self.OP_to_smt_file_map:
            self.bugs_dict[key] = ["unsigned_64", "signed_64", "Tnum", "unsigned_32", "signed_32"]

    def print_settings(self):
        print("Printing settings for verification and synthesis:")
        print("instruction pool for synthesis: ", self.OPS_set)
        print("Executing verification/synthesis on: ", self.insn_set_list)
        print("Json offset: ", self.json_offset)
        print("Kernel version: ",self.kernel_ver)
        print("Path for encodings: ",self.encodings_path)
        print("Write dir for output: ", self.write_path)
        print("Program size to synthesize (k length): ", self.num_iter)
        if len(self.bugs_dict) < 37:
            print("Bug type dictionary per instruction: ", self.bugs_dict)
        else:
            print("Bug type dictionary per instruction: set to default (all bug types for all instructions)\n")

    

#class that includes main constructs needed for verification and synthesis
class verification_synth_module:
    def __init__(self, usr_config):
        self.solver = None
        self.input_dst_reg_list = []
        self.input_src_reg_list = []
        self.output_dst_reg_list = []
        self.output_src_reg_list = []
        self.true_dst_list = []
        self.true_src_list = []
        self.false_dst_list = []
        self.false_src_list = []
        self.inp_json_bpf_mapping_list = []
        self.out_json_bpf_mapping_list = []
        self.safety_prop_list = {}
        self.violated_prop_list = []
        self.prog = ""
        self.prog_size = 0
        self.json_offset = usr_config.json_offset
        self.kernver = usr_config.kernel_ver
        self.write_counter = 1
        self.f_gen_const = None
        self.f_pre_cond = None
        self.f_post_cond = None

    def set_spec(self, f_gen_const, f_pre_cond, f_post_cond):
        self.f_gen_const = f_gen_const
        self.f_pre_cond = f_pre_cond
        self.f_post_cond = f_post_cond

    #create array of registers with abstract states (10 domains) as well as corresponding symbolic concrete values
    def create_reg_states(self, reg_indicator):
        if reg_indicator == "dst_input":
            reg_list = self.input_dst_reg_list
            json_mappings = self.inp_json_bpf_mapping_list
        elif reg_indicator == "src_input":
            reg_list = self.input_src_reg_list
            json_mappings = self.inp_json_bpf_mapping_list
        elif reg_indicator == "dst_output":
            reg_list = self.output_dst_reg_list
            json_mappings = self.out_json_bpf_mapping_list
        elif reg_indicator == "src_output":
            reg_list = self.output_src_reg_list
            json_mappings = self.out_json_bpf_mapping_list
        elif reg_indicator == "true_dst":
            reg_list = self.true_dst_list
            json_mappings = self.out_json_bpf_mapping_list
        elif reg_indicator == "true_src":
            reg_list = self.true_src_list
            json_mappings = self.out_json_bpf_mapping_list
        elif reg_indicator == "false_dst":
            reg_list = self.false_dst_list
            json_mappings = self.out_json_bpf_mapping_list
        elif reg_indicator == "false_src":
            reg_list = self.false_src_list
            json_mappings = self.out_json_bpf_mapping_list	

        reg_list.clear()
        # #make list of register states based on number of instructions
        for i in range(self.prog_size):
            reg_list.append(bpf_register(reg_indicator + str(i)))

    #assign corresponding input and output bitvectors according to json dict at
    #bottom of bpf encodings based on the instruction
    def assign_bitvector_mapping_to_encodings(self, formula):
        #assigning these vars to reduce length of parameters
        json_out = self.out_json_bpf_mapping_list
        json_in = self.inp_json_bpf_mapping_list
        json_off = self.json_offset

        for i in range(self.prog_size):
            #input registers are always the same mapping regardless of the
            #instruction - however, src_reg isn't used in sync for example
            self.input_dst_reg_list[i].update_bv_mappings(json_in[i]["dst_reg"][json_off:], self.kernver)
            if self.prog[i] != "BPF_SYNC":
                self.input_src_reg_list[i].update_bv_mappings(json_in[i]["src_reg"][json_off:], self.kernver)

            #if the insn is alu or SYNC use "dst_reg" mapping for output
            #alu has 2 in, 1 out; sync has 1 in, 1 out
            if self.prog[i][4] != "J" or self.prog[i] == "BPF_SYNC":
                self.output_dst_reg_list[i].update_bv_mappings(json_out[i]["dst_reg"][json_off:], self.kernver)

            #these are tmp registers to be used to assign jmp outputs
            if self.prog[i][4] == "J":
                #tmp registers to model outputs of jmps
                self.create_reg_states("true_dst")
                self.create_reg_states("true_src")
                self.create_reg_states("false_dst")
                self.create_reg_states("false_src")
                self.true_dst_list[i].update_bv_mappings(json_out[i]["other_branch_dst_reg"][json_off:], self.kernver)
                self.true_src_list[i].update_bv_mappings(json_out[i]["other_branch_src_reg"][json_off:], self.kernver)
                self.false_dst_list[i].update_bv_mappings(json_out[i]["dst_reg"][json_off:], self.kernver)
                self.false_src_list[i].update_bv_mappings(json_out[i]["src_reg"][json_off:], self.kernver)

            #assert all jmp verification conditions based on 32 or 64 jmp
            if(self.prog[i] == "BPF_JLE_32"):
                formula.append(If(
                    ULE(self.input_dst_reg_list[i].conc32, self.input_src_reg_list[i].conc32),
                    self.set_true_branch(i),
                    self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JLE"):
                formula.append(If(
                    ULE(self.input_dst_reg_list[i].conc64, self.input_src_reg_list[i].conc64),
                    self.set_true_branch(i),
                    self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JLT_32"):
                formula.append(If(
                        ULT(self.input_dst_reg_list[i].conc32, self.input_src_reg_list[i].conc32),
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JLT"):
                formula.append(If(
                        ULT(self.input_dst_reg_list[i].conc64, self.input_src_reg_list[i].conc64),
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JGT_32"):
                formula.append(If(
                        UGT(self.input_dst_reg_list[i].conc32, self.input_src_reg_list[i].conc32),
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JGT"):
                formula.append(If(
                        UGT(self.input_dst_reg_list[i].conc64, self.input_src_reg_list[i].conc64),
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JGE_32"):
                formula.append(If(
                        UGE(self.input_dst_reg_list[i].conc32, self.input_src_reg_list[i].conc32),
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JGE"):
                formula.append(If(
                        UGE(self.input_dst_reg_list[i].conc64, self.input_src_reg_list[i].conc64),
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSLE_32"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc32 <= self.input_src_reg_list[i].conc32,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSLE"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc64 <= self.input_src_reg_list[i].conc64,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSLT_32"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc32 < self.input_src_reg_list[i].conc32,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSLT"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc64 < self.input_src_reg_list[i].conc64,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSGT_32"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc32 > self.input_src_reg_list[i].conc32,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSGT"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc64 > self.input_src_reg_list[i].conc64,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSGE_32"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc32 >= self.input_src_reg_list[i].conc32,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JSGE"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc64 >= self.input_src_reg_list[i].conc64,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JNE_32"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc32 != self.input_src_reg_list[i].conc32,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JNE"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc64 != self.input_src_reg_list[i].conc64,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JEQ_32"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc32 == self.input_src_reg_list[i].conc32,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))
            elif(self.prog[i] == "BPF_JEQ"):
                formula.append(If(
                        self.input_dst_reg_list[i].conc64 == self.input_src_reg_list[i].conc64,
                        self.set_true_branch(i),
                        self.set_false_branch(i)))

    def set_true_branch(self, i):
        return And(
            self.output_dst_reg_list[i].get_equate_predicates(self.true_dst_list[i]), self.output_src_reg_list[i].get_equate_predicates(self.true_src_list[i]))


    def set_false_branch(self, i):
        return And(
            self.output_dst_reg_list[i].get_equate_predicates(self.false_dst_list[i]), self.output_src_reg_list[i].get_equate_predicates(self.false_src_list[i]))

    #function to set concrete to remain unchanged between inputs and output for jmps and SYNC
    def set_unchanged_concrete_jmps(self, formula):
        for i in range(self.prog_size):
            if self.prog[i][4] == "J" or self.prog[i] == "BPF_SYNC":
                formula.append(And(
                    self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32, 
                    self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64))
                formula.append(And(
                    self.output_src_reg_list[i].conc32 == self.input_src_reg_list[i].conc32, 
                    self.output_src_reg_list[i].conc64 == self.input_src_reg_list[i].conc64))

    #extract concrete 32 bit value from concrete 64 bit value
    def extract_from_64_bit(self, reg_indicator, formula):
        if reg_indicator == "dst_input":
            reg_list = self.input_dst_reg_list
        elif reg_indicator == "src_input":
            reg_list = self.input_src_reg_list
        elif reg_indicator == "dst_output":
            reg_list = self.output_dst_reg_list
        elif reg_indicator == "src_output":
            reg_list = self.output_src_reg_list
        elif reg_indicator == "true_dst":
            reg_list = self.true_dst_list
        elif reg_indicator == "true_src":
            reg_list = self.true_src_list
        elif reg_indicator == "false_dst":
            reg_list = self.false_dst_list
        elif reg_indicator == "false_src":
            reg_list = self.false_src_list
        tmp_list = []
        for i in range(self.prog_size):
            tmp_list.append(
                reg_list[i].conc32 == Extract(31, 0, reg_list[i].conc64))
        formula.append(And(tmp_list))		
    #assert 32 bit concrete value is contained in 32 bit bounds and 64 conc in
    #64
    def conc_is_contained_in_bounds(self, reg_indicator, formula):
        if reg_indicator == "dst_input":
            reg_list = self.input_dst_reg_list
        elif reg_indicator == "src_input":
            reg_list = self.input_src_reg_list
        elif reg_indicator == "dst_output":
            reg_list = self.output_dst_reg_list
        elif reg_indicator == "src_output":
            reg_list = self.output_src_reg_list

        #if the kernel version is prior to 5.7rc1 we don't use 32 bit
        #containment
        if version.parse(self.kernver) < version.parse("5.7-rc1"):
            for i in range(self.prog_size):
                #assert conc64 is contained within 64 bit bounds
                formula.append(reg_list[i].get_contains64_predicate())
        else:
            for i in range(self.prog_size):
                #assert conc32 is contained within 32 bit bounds
                formula.append(reg_list[i].get_contains32_predicate())
                #assert conc64 is contained within 64 bit bounds
                formula.append(reg_list[i].get_contains64_predicate())
        

    #set outputs of of prior instructions (i.e., prior to last insn) to be wellformed
    def set_wellformed_outputs(self, formula):
        #only consider 64 bit domains in prior versions to 5.7rc1
        if version.parse(self.kernver) < version.parse("5.7-rc1"):
            for i in range(self.prog_size-1):
                formula.append(self.output_dst_reg_list[i].get_contains64_predicate())
        else:
            for i in range(self.prog_size-1):
                formula.append(And(
                    self.output_dst_reg_list[i].get_contains32_predicate(),
                    self.output_dst_reg_list[i].get_contains64_predicate()))


    #define corresponding concrete outputs based on bpf operation - false branches
    def set_concrete_operation(self, formula):
        
        for i in range(self.prog_size):
            #if alu op ends with _32 then do 32 op and zero extend concrete 32
            #into 64 output. For 32jmps conc inputs (32/64) must remained unchanged before and after jmp.
            if self.prog[i][-1] == "2":
                if(self.prog[i] == "BPF_OR_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 | self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_AND_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 & self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_XOR_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 ^ self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_ADD_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 + self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_SUB_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 - self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_LSH_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 << self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_RSH_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == LShR(self.input_dst_reg_list[i].conc32, self.input_src_reg_list[i].conc32))
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
                elif(self.prog[i] == "BPF_ARSH_32"):
                    formula.append(
                        self.output_dst_reg_list[i].conc32 == self.input_dst_reg_list[i].conc32 >> self.input_src_reg_list[i].conc32)
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == ZeroExt(32, self.output_dst_reg_list[i].conc32))
            #set 64 bit op
            else:
                if(self.prog[i] == "BPF_OR"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 | self.input_src_reg_list[i].conc64)
                elif(self.prog[i] == "BPF_AND"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 & self.input_src_reg_list[i].conc64)
                elif(self.prog[i] == "BPF_XOR"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 ^ self.input_src_reg_list[i].conc64)
                elif(self.prog[i] == "BPF_ADD"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 + self.input_src_reg_list[i].conc64)
                elif(self.prog[i] == "BPF_SUB"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 - self.input_src_reg_list[i].conc64)
                elif(self.prog[i] == "BPF_LSH"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 << self.input_src_reg_list[i].conc64)
                elif(self.prog[i] == "BPF_RSH"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == LShR(self.input_dst_reg_list[i].conc64, self.input_src_reg_list[i].conc64))
                elif(self.prog[i] == "BPF_ARSH"):
                    formula.append(
                        self.output_dst_reg_list[i].conc64 == self.input_dst_reg_list[i].conc64 >> self.input_src_reg_list[i].conc64)
                


    #verification condition - one for jmps, the other for ALU
    def set_verification_condition(self):
        self.safety_prop_list.clear()
        if self.prog[-1][4] == "J":
            if version.parse(self.kernver) < version.parse("5.7-rc1"):
                self.safety_prop_list = {
                "unsigned_64": Not(And(
                    self.output_dst_reg_list[-1].get_contains64_predicate_only_unsigned(),
                    self.output_src_reg_list[-1].get_contains64_predicate_only_unsigned()
                    )), 
                "signed_64": Not(And(
                    self.output_dst_reg_list[-1].get_contains64_predicate_only_signed(),
                    self.output_src_reg_list[-1].get_contains64_predicate_only_signed())),
                "Tnum": Not(And(
                    self.output_dst_reg_list[-1].get_contains64_predicate_tnum(),
                    self.output_src_reg_list[-1].get_contains64_predicate_tnum()))}
            else:
                self.safety_prop_list = {
                    "unsigned_64": Not(And(
                        self.output_dst_reg_list[-1].get_contains64_predicate_only_unsigned(),
                        self.output_src_reg_list[-1].get_contains64_predicate_only_unsigned()
                        )), 
                    "signed_64": Not(And(
                        self.output_dst_reg_list[-1].get_contains64_predicate_only_signed(),
                        self.output_src_reg_list[-1].get_contains64_predicate_only_signed())),
                    "Tnum": Not(And(
                        self.output_dst_reg_list[-1].get_contains64_predicate_tnum(),
                        self.output_src_reg_list[-1].get_contains64_predicate_tnum())),
                    "unsigned_32": Not(And(
                        self.output_dst_reg_list[-1].get_contains32_predicate_only_unsigned(),
                        self.output_src_reg_list[-1].get_contains32_predicate_only_unsigned()
                        )),
                    "signed_32": Not(And(
                        self.output_dst_reg_list[-1].get_contains32_predicate_only_signed(),
                        self.output_src_reg_list[-1].get_contains32_predicate_only_signed()))}
        else:
            if version.parse(self.kernver) < version.parse("5.7-rc1"):
                self.safety_prop_list = {
                "unsigned_64": Not(
                    self.output_dst_reg_list[-1].get_contains64_predicate_only_unsigned()), 
                "signed_64": Not(
                    self.output_dst_reg_list[-1].get_contains64_predicate_only_signed()),
                "Tnum": Not(
                    self.output_dst_reg_list[-1].get_contains64_predicate_tnum())}
            else:
                self.safety_prop_list = {
                    "unsigned_64": Not(
                        self.output_dst_reg_list[-1].get_contains64_predicate_only_unsigned()), 
                    "signed_64": Not(
                        self.output_dst_reg_list[-1].get_contains64_predicate_only_signed()),
                    "Tnum": Not(
                        self.output_dst_reg_list[-1].get_contains64_predicate_tnum()),
                    "unsigned_32": Not(
                        self.output_dst_reg_list[-1].get_contains32_predicate_only_unsigned()),
                    "signed_32": Not(
                        self.output_dst_reg_list[-1].get_contains32_predicate_only_signed())}


    #propagate two sync instructions
    def seq_discover(self, formula):
        f_dst = []
        f_src = []
        #num of adjacent prior insn to take inputs from. 
        num_prior_insn = 2

        #minimum program size = 3 in sync check since we're using two instances
        #of sync.
        if(self.prog_size > 2):
            for i in reversed(range(self.prog_size-1)):
                f_dst.clear()
                f_src.clear()
                #last k insn will pull num of immediate prior instructions as
                #defined above in num_prior_insn
                if i < 1:
                    break
                
                for count, j in enumerate(reversed(range(i+1))):
                    #we only want an insn to pull from prior x insn where x is
                    #defined by num_prior_insn var above
                    if count == num_prior_insn:
                        break
                    #dst operand will pull from first output
                    if(count == 1):
                        f_dst.append(
                            self.input_dst_reg_list[i+1].get_equate_predicates(self.output_dst_reg_list[j]))

                    # #src operand will take directly prior insn (this is so that we won't get that the nth insn just skips over one of the priors)
                    if(count == 0):
                        f_src.append(
                            self.input_src_reg_list[i+1].get_equate_predicates(self.output_dst_reg_list[j]))


                formula.append(And(f_dst))
                formula.append(And(f_src))

    #propagate multiple instructions for multiprogram synthesis
    def propagate_instructions(self, formula):
        f_dst = []
        f_src = []

        if(self.prog_size > 1):
            #dst operand can be any of the prior outputs, fully known reg, or
            #fully unknown reg src operand can be any of the prior outputs,
            #fully known reg, or fully unknown reg
            for i in reversed(range(self.prog_size-1)):
                f_dst.clear()
                f_src.clear()
                
                for j in range(i+1):
                    #adding propagation of both outputs in jmps is costly in terms of synthesis - consider this later.
                    #dst operand can be any of the prior outputs
                    f_dst.append(
                        self.input_dst_reg_list[i+1].get_equate_predicates(self.output_dst_reg_list[j]))
                    #src operand can be any of the prior outputs
                    f_src.append(
                        self.input_src_reg_list[i+1].get_equate_predicates(self.output_dst_reg_list[j]))
                # dst operand can be singleton reg, or fully unknown reg
                f_dst.append(self.input_dst_reg_list[i+1].fully_unknown())
                f_dst.append(self.input_dst_reg_list[i+1].singleton())	
                #src operand can be singleton reg, or fully unknown reg
                f_src.append(self.input_src_reg_list[i+1].fully_unknown())
                f_src.append(self.input_src_reg_list[i+1].singleton())

                formula.append(Or(f_dst))
                formula.append(Or(f_src))

    #function to check every bug type given some program (one bug type per
    #one bounds violated (u64, s64,...))
    def check_bug_violations(self):
        self.violated_prop_list.clear()

        for p in self.safety_prop_list:
            #backtracking state for solver before we add safety conditions
            self.solver.push()
            self.solver.add(self.safety_prop_list[p])
            check_output = str(self.solver.check())
            #for debugging###
            # self.f_post_cond.append(self.safety_prop_list[p])
            # self.print_register_mappings()
            # self.print_specification()
            # self.print_synthesis_model()
            # self.print_synthesized_program()
            # self.f_post_cond.remove(self.safety_prop_list[p])
            # print("Bound violated: ", p)
            ####
            #if there is a sat model we add the violated bound
            if check_output == "sat": 
                self.violated_prop_list.append(p)

            #remove safety condition we put in for new one to replace it
            self.solver.pop()

    #synthesize bugs based on possible bug types
    def synthesize_bug_type(self, usr_config):
        self.violated_prop_list.clear()
        #look at bug list for the last instruction in sequence
        for p in usr_config.bugs_dict[self.prog[-1]]:
            #backtracking state for solver before we add safety conditions
            self.solver.push()
            self.solver.add(self.safety_prop_list[p])
            check_output = str(self.solver.check())
            if check_output == "sat": 
                #update smt model map to be able to write it to file
                BitVecHelper.update_map_with_model(self.solver.model())
                self.violated_prop_list.append(p)
                # self.print_register_mappings()
                # self.print_specification()
                # self.print_synthesis_model()
                self.print_synthesized_program(p)
                self.write_synthesis_bug_model(usr_config, p)
                self.generate_json_model(usr_config, p)

                self.write_counter += 1
                

            self.solver.pop()
        #remove safety condition we put in for new one to replace it
        for p in self.violated_prop_list:
            usr_config.bugs_dict[self.prog[-1]].remove(p)

    #write model to file
    def write_synthesis_bug_model(self, usr_config, bug_type):
        directory = usr_config.write_path +"/bug_log_" + usr_config.kernel_ver + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        s = ""
        with open(directory + str(self.write_counter) + ".txt", "w") as f:
            if(self.prog_size > 1):
                for i in range(self.prog_size):
                    s += str(self.prog[i]) + "\n"
            else:
                s += str(self.prog) + "\n"
            s += ";\n"
            s += "out_dst_64conc: " +  fmv_dec(self.output_dst_reg_list[-1].conc64) + "\n"
            s += "out_dst_32conc: " +  fmv_dec(self.output_dst_reg_list[-1].conc32) + "\n"
            s += ";\n"
            s += "Bound violated: " + bug_type +"\n"
            s += ";\n"
            s += usr_config.kernel_ver + "\n" #kernel version
            s += ";\n"
            for i in range(self.prog_size):
                s += getcstr_to_write(self.input_dst_reg_list[i])
                s += getcstr_to_write(self.input_src_reg_list[i])
                s += getcstr_to_write(self.output_dst_reg_list[i])

            f.write(s)

            if version.parse(self.kernver) < version.parse("5.7-rc1"):
                for i in range(self.prog_size):
                    f.write("\n")
                    f.write(getcstr_no_32_bounds("dst_reg_input_" + str(i), self.input_dst_reg_list[i]))
                    f.write(getcstr_no_32_bounds("src_reg_input_" + str(i), self.input_src_reg_list[i]))
                    f.write(getcstr_no_32_bounds("dst_reg_output_" + str(i), self.output_dst_reg_list[i]))
                    if self.prog[i][4] == "J":
                        f.write(getcstr_no_32_bounds("src_reg_output_" + str(i), self.output_src_reg_list[i]))
            else: 
                for i in range(self.prog_size):
                    f.write("\n")
                    f.write(getcstr("dst_reg_input_" + str(i), self.input_dst_reg_list[i]))
                    f.write(getcstr("src_reg_input_" + str(i), self.input_src_reg_list[i]))
                    f.write(getcstr("dst_reg_output_" + str(i), self.output_dst_reg_list[i]))
                    if self.prog[i][4] == "J":
                        f.write(getcstr("src_reg_output_" + str(i), self.output_src_reg_list[i]))
        
            f.write("\nOutput program:\n")
            m = self.solver.model()
            for i in range(self.prog_size):
                #print model for 32 bit if it's a 32 bit op
                if(self.prog[i][-1] == "2"):
                    f.write(str(self.prog[i]) + "({}, {})\n".format(m[self.input_dst_reg_list[i].conc32], m[self.input_src_reg_list[i].conc32],  m[self.output_dst_reg_list[i].conc32]))
                #else pring model for 64 bit
                else:
                    f.write(str(self.prog[i]) + "({}, {})\n".format(m[self.input_dst_reg_list[i].conc64], m[self.input_src_reg_list[i].conc64],  m[self.output_dst_reg_list[i].conc64]))
            
            

    #print synthesis model
    def print_synthesized_program(self, bug_type):
        
        print("\nSynthesized program for", self.prog[-1], "({}).".format(bug_type), "Instruction sequence: ", end="")
        m = self.solver.model()
        for i in range(self.prog_size):
            if(self.prog[i][-1] == "2"):
                print(colored(str(self.prog[i]), "green"), end=" ")
            #else pring model for 64 bit
            else:
                print(colored(str(self.prog[i]), "green"), end=" ")
            
            #print model for 32 bit if it's a 32 bit op
            # if(self.prog[i][-1] == "2"):
            # 	print(colored(str(self.prog[i]) + "({}, {})".format(m[self.input_dst_reg_list[i].conc32], m[self.input_src_reg_list[i].conc32],  m[self.output_dst_reg_list[i].conc32]), "green"))
            # #else pring model for 64 bit
            # else:
            # 	print(colored(str(self.prog[i]) + "({}, {})".format(m[self.input_dst_reg_list[i].conc64], m[self.input_src_reg_list[i].conc64],  m[self.output_dst_reg_list[i].conc64]), "green"))


    def generate_json_model(self, usr_config, bug_type):
        m = self.solver.model()
        reg_headers = ["conc64", "conc32", "var_off_value", "var_off_mask", "smin_value", "smax_value", "umin_value", "umax_value",  "s32_min_value", "s32_max_value", "u32_min_value", "u32_max_value"]
        signed64_doms = ["smin_value", "smax_value"]
        signed32_doms = ["s32_min_value", "s32_max_value"]
        prog_names = []
        json_dict = {}
        
        #create sub dictionaries
        for i, ele in enumerate(self.prog):
            #make a list of program names which are entries in dict
            prog_names.append(i)
            json_dict[i] = {"insn": ele, "dst_inp": {}, "src_inp": {}, "dst_out": {}, "src_out": {}}

        for i in range(len(self.prog)):
            inp_dst_dict = vars(self.input_dst_reg_list[i])
            inp_src_dict = vars(self.input_src_reg_list[i])
            out_dst_dict = vars(self.output_dst_reg_list[i])
            out_src_dict = vars(self.output_src_reg_list[i])

            json_dict[prog_names[i]]["inst_num"] = i
            for j in reg_headers:
                
                if j in signed64_doms:
                    json_dict[prog_names[i]]["dst_inp"][j] = ctypes.c_int64(m[inp_dst_dict[j]].as_long()).value
                    json_dict[prog_names[i]]["dst_out"][j] = ctypes.c_int64(m[out_dst_dict[j]].as_long()).value
                    json_dict[prog_names[i]]["src_inp"][j] = ctypes.c_int64(m[inp_src_dict[j]].as_long()).value
                    json_dict[prog_names[i]]["src_out"][j] = ctypes.c_int64(m[out_src_dict[j]].as_long()).value

                elif j in signed32_doms:
                    json_dict[prog_names[i]]["dst_inp"][j] = ctypes.c_int32(m[inp_dst_dict[j]].as_long()).value
                    json_dict[prog_names[i]]["dst_out"][j] = ctypes.c_int32(m[out_dst_dict[j]].as_long()).value
                    json_dict[prog_names[i]]["src_inp"][j] = ctypes.c_int32(m[inp_src_dict[j]].as_long()).value
                    json_dict[prog_names[i]]["src_out"][j] = ctypes.c_int32(m[out_src_dict[j]].as_long()).value
                
                else:
                    json_dict[prog_names[i]]["dst_inp"][j] = m[inp_dst_dict[j]].as_long()
                    json_dict[prog_names[i]]["dst_out"][j] = m[out_dst_dict[j]].as_long()
                    json_dict[prog_names[i]]["src_inp"][j] = m[inp_src_dict[j]].as_long()
                    json_dict[prog_names[i]]["src_out"][j] = m[out_src_dict[j]].as_long()

        directory = usr_config.write_path +"/bug_log_" + usr_config.kernel_ver + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filename = directory + str(usr_config.kernel_ver) + "_" + str(self.prog[-1]) + "_" + str(bug_type) + ".json"
        filename = filename = filename.replace("unsigned_64", "u64")
        filename = filename = filename.replace("Tnum", "tnum")
        filename = filename = filename.replace("unsigned_32", "u32")
        filename = filename = filename.replace("signed_64", "s64")
        filename = filename = filename.replace("signed_32", "s32")
        filename = filename.replace("BPF_", "")
        filename = filename.replace("_32", "32")
        filename = filename.lower()

        with open(filename, "w") as f:
            json.dump(json_dict, f)



    # def generate_bpf_bytcode(self):

        # reg_count = 1
        # #print model for bpf bytecode
        # for i in range(self.prog_size):
        # 	if m[self.input_dst_reg_list[i].var_off_mask] == 0:
        # 		print("\n// REG_{} known".format(reg_count))
        # 		print("BPF_LD_IMM64(BPF_REG_{}, {})".format(reg_count, str(m[self.input_dst_reg_list[i].conc64])))
        # 		reg_count += 1
        # 	else:
        # 		print("\n// REG_{} unknown".format(reg_count))
        # 		print("BPF_LD_IMM64(BPF_REG_{}, {})".format(reg_count, str(m[self.input_dst_reg_list[i].conc64])))
        # 		print("BPF_ALU64_IMM(BPF_NEG, BPF_REG_{}, 0)".format(reg_count))
        # 		print("BPF_ALU64_IMM(BPF_NEG, BPF_REG_{}, 0)".format(reg_count))
        # 		reg_count += 1
        # 	if m[self.input_src_reg_list[i].var_off_mask] == 0:
        # 		print("\n// REG_{} known".format(reg_count))
        # 		print("BPF_LD_IMM64(BPF_REG_{}, {})".format(reg_count, str(m[self.input_src_reg_list[i].conc64])))
        # 		reg_count += 1
        # 	else:
        # 		print("\n// REG_{} unknown".format(reg_count))
        # 		print("BPF_LD_IMM64(BPF_REG_{}, {})".format(reg_count, str(m[self.input_src_reg_list[i].conc64])))
        # 		print("BPF_ALU64_IMM(BPF_NEG, BPF_REG_{}, 0)".format(reg_count))
        # 		print("BPF_ALU64_IMM(BPF_NEG, BPF_REG_{}, 0)".format(reg_count))
        # 		reg_count += 1

        # reg_count = 1
        # #print instructions
        # print("\n//instruction sequence begins")
        # for i in range(self.prog_size):
        # 	#print model for bpf bytecode
        # 	if m[self.input_dst_reg_list[i].var_off_mask] == 0:
        # 		dst = str(m[self.input_dst_reg_list[i].conc64])
        # 		reg_count += 1
        # 	else:
        # 		dst = "REG_" + str(reg_count)
        # 		reg_count += 1
        # 	if m[self.input_src_reg_list[i].var_off_mask] == 0:
        # 		src = str(m[self.input_src_reg_list[i].conc64])
        # 		reg_count += 1
        # 	else:
        # 		src = "REG_" + str(reg_count)
        # 		reg_count += 1
        # 	if self.prog[i][4] == "J":
        # 		print("BPF_{}_REG({}, {}, {}, X)".format("JMP?", self.prog[i], dst, src))
        # 	else:
        # 		print("BPF_{}_REG({}, {}, {}, X)".format("ALU?", self.prog[i], dst, src))
            # BPF_MOV64_IMM(BPF_REG_0, 1),

            # BPF_JMP32_REG(BPF_JLT, BPF_REG_1, BPF_REG_3, 3),


            

    #print specification for verification/synthesis
    def print_specification(self):
        print("\n--------------------")
        print("Specification")
        self.f_gen_const.print_spec()
        self.f_pre_cond.print_spec()
        self.f_post_cond.print_spec()

    #print corresponding input/output mappings
    def print_register_mappings(self):
        
        print("\n-------------")
        print("Register Mappings")
        print("-------------")
        print("dst input mappings")
        pprint([self.input_dst_reg_list[i].__dict__ for i in range(self.prog_size)])
        print("--------------------------------")
        print("src input mappings")
        pprint([self.input_src_reg_list[i].__dict__ for i in range(self.prog_size)])
        print("--------------------------------")
        print("dst output mappings")
        pprint([self.output_dst_reg_list[i].__dict__ for i in range(self.prog_size)])
        print("--------------------------------")

    #print synthesis model
    def print_synthesis_model(self):
        print("\n-------------")
        print("Synthesis Model")
        print("-------------")
        print(self.prog)
        m = self.solver.model()
        BitVecHelper.update_map_with_model(m)
        t = BitVecHelper.get_bitvec_map_with_model_as_table()
        print(t)
        if version.parse(self.kernver) < version.parse("5.7-rc1"):
            for i in range(self.prog_size):
                print(getcstr_no_32_bounds("dst_reg_input_" + str(i), self.input_dst_reg_list[i]))
                print(getcstr_no_32_bounds("src_reg_input_" + str(i), self.input_src_reg_list[i]))
                print(getcstr_no_32_bounds("dst_reg_output_" + str(i), self.output_dst_reg_list[i]))
                if self.prog[i][4] == "J":
                    print(getcstr_no_32_bounds("src_reg_output_" + str(i), self.output_src_reg_list[i]))
        else: 
            for i in range(self.prog_size):
                print(getcstr("dst_reg_input_" + str(i), self.input_dst_reg_list[i]))
                print(getcstr("src_reg_input_" + str(i), self.input_src_reg_list[i]))
                print(getcstr("dst_reg_output_" + str(i), self.output_dst_reg_list[i]))
                if self.prog[i][4] == "J":
                    print(getcstr("src_reg_output_" + str(i), self.output_src_reg_list[i]))



#### UTILITY Functions for synthesis


# format_model_value - print in hex
def fmv(modelvalue):
    bvprop = BitVecHelper.bitvec_map[str(modelvalue)]
    #st = ""
    st = 0
    if bvprop.sign == SIGNED:
        #st += str(bvprop.model_value_signed)
        st = hex(bvprop.model_value_signed)
    elif bvprop.sign == UNSIGNED:
        #st += str(bvprop.model_value)
        st = hex(bvprop.model_value)
        #if (bvprop.model_value > 0x7fffffffffffffff):
        #    st += "ULL"
    return st

# format_model_value - print in dec
def fmv_dec(modelvalue):
    bvprop = BitVecHelper.bitvec_map[str(modelvalue)]
    st = ""
    if bvprop.sign == SIGNED:
        st += str(bvprop.model_value_signed)
        #st = bvprop.model_value_signed
    elif bvprop.sign == UNSIGNED:
        st += str(bvprop.model_value)
        #st = bvprop.model_value
        #if (bvprop.model_value > 0x7fffffffffffffff):
        #    st += "ULL"
    return st


def getcstr(name, reg_st):
    cstr = "{}.var_off.value = {};\n".format(name, 	fmv_dec(reg_st.var_off_value))
    cstr += "{}.var_off.mask = {};\n".format(name, 	fmv_dec(reg_st.var_off_mask))
    cstr += "{}.smin_value = {};\n".format(name, 	fmv_dec(reg_st.smin_value))
    cstr += "{}.smax_value = {};\n".format(name, 	fmv_dec(reg_st.smax_value))
    cstr += "{}.umin_value = {};\n".format(name, 	fmv_dec(reg_st.umin_value))
    cstr += "{}.umax_value = {};\n".format(name, 	fmv_dec(reg_st.umax_value))
    cstr += "{}.s32_min_value = {};\n".format(name, fmv_dec(reg_st.s32_min_value))
    cstr += "{}.s32_max_value = {};\n".format(name, fmv_dec(reg_st.s32_max_value))
    cstr += "{}.u32_min_value = {};\n".format(name, fmv_dec(reg_st.u32_min_value))
    cstr += "{}.u32_max_value = {};\n".format(name, fmv_dec(reg_st.u32_max_value))
    return cstr

def getcstr_no_32_bounds(name, reg_st):
    cstr = "{}.var_off.value = {};\n".format(name, 	fmv_dec(reg_st.var_off_value))
    cstr += "{}.var_off.mask = {};\n".format(name, 	fmv_dec(reg_st.var_off_mask))
    cstr += "{}.smin_value = {};\n".format(name, 	fmv_dec(reg_st.smin_value))
    cstr += "{}.smax_value = {};\n".format(name, 	fmv_dec(reg_st.smax_value))
    cstr += "{}.umin_value = {};\n".format(name, 	fmv_dec(reg_st.umin_value))
    cstr += "{}.umax_value = {};\n".format(name, 	fmv_dec(reg_st.umax_value))
    return cstr

def print_dunder(d):
    for i in d:
        print(i, ":", d[i], d[i].sort())

#define powerset with replacement (powerset+cartesian product)
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,1) (2,2) (3,3) ...(1,3) (2,3) (1,2,3)..."
    s = list(iterable)
    return chain.from_iterable(itertools.product(s, repeat = r) for r in range(1,len(s)+1))



def getcstr_to_write(reg_st):
    cstr = "{}\n".format(fmv_dec(reg_st.var_off_value))
    cstr += "{}\n".format(fmv_dec(reg_st.var_off_mask))
    cstr += "{}\n".format(fmv_dec(reg_st.smin_value))
    cstr += "{}\n".format(fmv_dec(reg_st.smax_value))
    cstr += "{}\n".format(fmv_dec(reg_st.umin_value))
    cstr += "{}\n".format(fmv_dec(reg_st.umax_value))
    cstr += "{}\n".format(fmv_dec(reg_st.s32_min_value))
    cstr += "{}\n".format(fmv_dec(reg_st.s32_max_value))
    cstr += "{}\n".format(fmv_dec(reg_st.u32_min_value))
    cstr += "{}\n".format(fmv_dec(reg_st.u32_max_value))
    return cstr



# update ast for synthesizing multiples of the same instruction (bpf_or, bpf_or...) creates tmp new smt_lib files
def ast_sub_for_bpf_encoding(smt_file, suffix):
    bitvec_name_list = []
    text_file = open("/tmp/tmp_" + str(suffix) + ".smt2", "w")
    with open(smt_file, "r") as file_1:
        filedata = file_1.readlines()
        for line in filedata:
            #separate line by space delimiter 
            x = line.split()
            #if empty line, skip it
            if(not x):
                continue
            #if its a bitvector declare take note of name
            elif(x[0] == '(declare-fun'):
                bitvec_name_list.append(x[1])
            
    #print(bitvec_name_list)
    with open(smt_file, "r") as file_1:
        newdata = file_1.read()
        for i in bitvec_name_list:
            #add suffix to each bitvector name to change it from previous encoding
            newdata = newdata.replace(i, i + "_" + str(suffix))
        #print(newdata)
    #write updated encoding to new tmp file
    text_file.write(newdata)
    text_file.close()

    return text_file.name


#check if there are multiple uses of the same bpf encoding smt_lib file and do an ast sub on the repeating inst if there are - return updated list of files
def check_for_repeat_instructions_and_update(smt_files):
    updated_smtfile_list = []
    #counter for updating the suffix of bitvector names in the AST
    suffix = time.time_ns()
    for i in smt_files:
        #if file already exists it's a repeat - update AST
        if i in updated_smtfile_list:
            updated_smtfile_list.append(ast_sub_for_bpf_encoding(i, suffix))
            suffix += 1
        #else add to the list
        else:
            updated_smtfile_list.append(i)

    #print(updated_smtfile_list)
    return updated_smtfile_list


 #create instance of smt solver, add bpf encodings to it, and make list of
 #input/output mappings - each mapping refers to a single json at the end of an
 #smt lib file (bpf instruction encoding). json_offset refers to reg struct
 #numbering (i.e. where do abstract domain start in the struct)
def parse_and_map(prog, OP_to_smt_file_map):
    #make list of smt file paths
    smt_files = []
    for i in range(len(prog)):
        smt_files.append(OP_to_smt_file_map[prog[i]])

    #if there are multiples of the same instruction - perform ast sub
    smt_files = check_for_repeat_instructions_and_update(smt_files)

    #make list of input/output mappings - each mapping refers to a single json at the end of an smt lib file
    in_json_bpf_enc_mappings = []
    out_json_bpf_enc_mappings = []
    for i in range(len(smt_files)):
        with open(smt_files[i], "r") as file_1:
            #read in file
            file_1_lines = file_1.readlines()
            #parse second to last line in file (contains inputs)
            in_json_bpf_enc_mappings.append(file_1_lines[-2].strip())
            #remove first ; character
            in_json_bpf_enc_mappings[i] = in_json_bpf_enc_mappings[i][1:]
            #load json string into python dict
            in_json_bpf_enc_mappings[i] = json.loads(in_json_bpf_enc_mappings[i])

            ##parse last line in file (contains outputs)
            out_json_bpf_enc_mappings.append(file_1_lines[-1].strip())
            #remove first ; character
            out_json_bpf_enc_mappings[i] = out_json_bpf_enc_mappings[i][1:]
            #load json string into python dict
            out_json_bpf_enc_mappings[i] = json.loads(out_json_bpf_enc_mappings[i])

    #create solver instance
    solver = Optimize()
    
    #add smt encodings to solver by parsing smt files
    for x in smt_files:
            solver.add(parse_smt2_file(x)) 
    
    return solver, in_json_bpf_enc_mappings, out_json_bpf_enc_mappings





