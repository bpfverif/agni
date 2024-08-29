; ModuleID = '/home/pchaigno/agni/bpf-encodings/5.4/BPF_JSLE/BPF_JSLE.O1.ffee.O1.rfc.O1.ivf.O1.pmc.O0.lfsh.ivf.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.bpf_reg_state = type { i32, %union.anon.147, i32, i32, i32, %struct.tnum, i64, i64, i64, i64, %struct.bpf_reg_state*, i32, i32, i32, i8 }
%union.anon.147 = type { %struct.bpf_map* }
%struct.bpf_map = type { %struct.bpf_map_ops*, %struct.bpf_map*, i8*, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, %struct.btf*, %struct.bpf_map_memory, i8, i8, [38 x i8], %struct.atomic_t, %struct.atomic_t, %struct.work_struct, [16 x i8], [8 x i8] }
%struct.bpf_map_ops = type { i32 (%union.bpf_attr*)*, %struct.bpf_map* (%union.bpf_attr*)*, void (%struct.bpf_map*, %struct.file*)*, void (%struct.bpf_map*)*, i32 (%struct.bpf_map*, i8*, i8*)*, void (%struct.bpf_map*)*, i8* (%struct.bpf_map*, i8*)*, i8* (%struct.bpf_map*, i8*)*, i32 (%struct.bpf_map*, i8*, i8*, i64)*, i32 (%struct.bpf_map*, i8*)*, i32 (%struct.bpf_map*, i8*, i64)*, i32 (%struct.bpf_map*, i8*)*, i32 (%struct.bpf_map*, i8*)*, i8* (%struct.bpf_map*, %struct.file*, i32)*, void (i8*)*, i32 (%struct.bpf_map*, %struct.bpf_insn*)*, i32 (i8*)*, void (%struct.bpf_map*, i8*, %struct.seq_file*)*, i32 (%struct.bpf_map*, %struct.btf*, %struct.btf_type*, %struct.btf_type*)*, i32 (%struct.bpf_map*, i64*, i32)*, i32 (%struct.bpf_map*, i64, i32*)* }
%union.bpf_attr = type { %struct.anon.1 }
%struct.anon.1 = type { i32, i32, i64, i64, i32, i32, i64, i32, i32, [16 x i8], i32, i32, i32, i32, i64, i32, i32, i64, i32 }
%struct.file = type { %union.anon.12, %struct.path, %struct.inode*, %struct.file_operations*, %struct.spinlock, i32, %union.anon.13, i32, i32, %struct.mutex, i64, %struct.fown_struct, %struct.cred*, %struct.file_ra_state, i64, i8*, i8*, %struct.list_head, %struct.list_head, %struct.address_space*, i32 }
%union.anon.12 = type { %struct.callback_head }
%struct.callback_head = type { %struct.callback_head*, void (%struct.callback_head*)* }
%struct.path = type { %struct.vfsmount*, %struct.dentry* }
%struct.vfsmount = type opaque
%struct.dentry = type { i32, %struct.atomic_t, %struct.hlist_bl_node, %struct.dentry*, %struct.qstr, %struct.inode*, [32 x i8], %struct.local_t, %struct.dentry_operations*, %struct.super_block*, i64, i8*, %struct.sysv_shm, %struct.list_head, %struct.list_head, %union.anon.75 }
%struct.hlist_bl_node = type { %struct.hlist_bl_node*, %struct.hlist_bl_node** }
%struct.qstr = type { %union.anon.13, i8* }
%struct.local_t = type { %union.anon.13 }
%struct.dentry_operations = type { i32 (%struct.dentry*, i32)*, i32 (%struct.dentry*, i32)*, i32 (%struct.dentry*, %struct.qstr*)*, i32 (%struct.dentry*, i32, i8*, %struct.qstr*)*, i32 (%struct.dentry*)*, i32 (%struct.dentry*)*, void (%struct.dentry*)*, void (%struct.dentry*)*, void (%struct.dentry*, %struct.inode*)*, i8* (%struct.dentry*, i8*, i32)*, %struct.vfsmount* (%struct.path*)*, i32 (%struct.path*, i1)*, %struct.dentry* (%struct.dentry*, %struct.inode*)*, [24 x i8] }
%struct.super_block = type { %struct.list_head, i32, i8, i64, i64, %struct.file_system_type*, %struct.super_operations*, %struct.dquot_operations*, %struct.quotactl_ops*, %struct.export_operations*, i64, i64, i64, %struct.dentry*, %struct.rw_semaphore, i32, %struct.atomic_t, i8*, %struct.xattr_handler**, %struct.hlist_bl_head, %struct.list_head, %struct.block_device*, %struct.backing_dev_info*, %struct.mtd_info*, %struct.hlist_node, i32, %struct.quota_info, %struct.sb_writers, i8*, i32, i64, i64, i32, %struct.fsnotify_mark_connector*, [32 x i8], %union.anon.127, i32, i32, %struct.mutex, i8*, %struct.dentry_operations*, i32, %struct.shrinker, %union.anon.13, %union.anon.13, i32, %struct.workqueue_struct*, %struct.hlist_head, %struct.user_namespace*, %struct.list_lru, %struct.list_lru, %struct.callback_head, %struct.work_struct, %struct.mutex, i32, [52 x i8], %struct.spinlock, %struct.list_head, %struct.spinlock, %struct.list_head, [16 x i8] }
%struct.file_system_type = type { i8*, i32, i32 (%struct.fs_context*)*, %struct.fs_parameter_description*, %struct.dentry* (%struct.file_system_type*, i32, i8*, i8*)*, void (%struct.super_block*)*, %struct.module*, %struct.file_system_type*, %struct.hlist_head, %struct.u64_stats_sync, %struct.u64_stats_sync, %struct.u64_stats_sync, [3 x %struct.u64_stats_sync], %struct.u64_stats_sync, %struct.u64_stats_sync, %struct.u64_stats_sync }
%struct.fs_context = type opaque
%struct.fs_parameter_description = type opaque
%struct.module = type { i32, %struct.list_head, [56 x i8], %struct.module_kobject, %struct.module_attribute*, i8*, i8*, %struct.kobject*, %struct.uid_gid_extent*, i32*, i32, %struct.mutex, %struct.kernel_param*, i32, i32, %struct.uid_gid_extent*, i32*, i8, %struct.uid_gid_extent*, i32*, i32, i32, %struct.uid_gid_extent*, i32 ()*, [40 x i8], %struct.module_layout, %struct.module_layout, %struct.mod_arch_specific, i64, i32, %struct.list_head, %struct.bug_entry*, %struct.mod_kallsyms*, %struct.mod_kallsyms, %struct.module_sect_attrs*, %struct.module_notes_attrs*, i8*, i8*, i32, i32, i32*, i32, %struct.srcu_struct**, i32, %struct.bpf_raw_event_map*, %struct.jump_entry*, i32, i32, i8**, %struct.trace_event_call**, i32, %struct.trace_eval_map**, i32, %struct.list_head, %struct.list_head, void ()*, %struct.atomic_t, %struct.thread_info*, i32, [52 x i8] }
%struct.module_kobject = type { %struct.kobject, %struct.module*, %struct.kobject*, %struct.module_param_attrs*, %struct.completion* }
%struct.kobject = type { i8*, %struct.list_head, %struct.kobject*, %struct.kset*, %struct.kobj_type*, %struct.kernfs_node*, %struct.qspinlock, i8 }
%struct.kset = type { %struct.list_head, %struct.spinlock, %struct.kobject, %struct.kset_uevent_ops* }
%struct.kset_uevent_ops = type { i32 (%struct.kset*, %struct.kobject*)*, i8* (%struct.kset*, %struct.kobject*)*, i32 (%struct.kset*, %struct.kobject*, %struct.kobj_uevent_env*)* }
%struct.kobj_uevent_env = type { [3 x i8*], [32 x i8*], i32, [2048 x i8], i32 }
%struct.kobj_type = type { void (%struct.kobject*)*, %struct.sysfs_ops*, %struct.attribute**, %struct.attribute_group**, %struct.kobj_ns_type_operations* (%struct.kobject*)*, i8* (%struct.kobject*)*, void (%struct.kobject*, %struct.atomic_t*, %struct.atomic_t*)* }
%struct.sysfs_ops = type { i64 (%struct.kobject*, %struct.attribute*, i8*)*, i64 (%struct.kobject*, %struct.attribute*, i8*, i64)* }
%struct.attribute = type { i8*, i16 }
%struct.attribute_group = type { i8*, i16 (%struct.kobject*, %struct.attribute*, i32)*, i16 (%struct.kobject*, %struct.bin_attribute*, i32)*, %struct.attribute**, %struct.bin_attribute** }
%struct.bin_attribute = type { %struct.attribute, i64, i8*, i64 (%struct.file*, %struct.kobject*, %struct.bin_attribute*, i8*, i64, i64)*, i64 (%struct.file*, %struct.kobject*, %struct.bin_attribute*, i8*, i64, i64)*, i32 (%struct.file*, %struct.kobject*, %struct.bin_attribute*, %struct.vm_area_struct*)* }
%struct.vm_area_struct = type { i64, i64, %struct.vm_area_struct*, %struct.vm_area_struct*, %struct.rb_node, i64, %struct.mm_struct*, %union.anon.13, i64, %struct.timerqueue_node, %struct.list_head, %struct.anon_vma*, %struct.vm_operations_struct*, i64, %struct.file*, i8*, %union.anon.13, %struct.mempolicy*, %struct.u64_stats_sync }
%struct.rb_node = type { i64, %struct.rb_node*, %struct.rb_node* }
%struct.mm_struct = type { %struct.anon.15, [0 x i64] }
%struct.anon.15 = type { %struct.vm_area_struct*, %struct.rb_root, i64, i64 (%struct.file*, i64, i64, i64, i64)*, i64, i64, i64, i64, i64, i64, %union.anon.13*, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %union.anon.13, i32, %struct.spinlock, %struct.rw_semaphore, %struct.list_head, i64, i64, i64, i64, %union.anon.13, i64, i64, i64, i64, %struct.spinlock, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, [46 x i64], %struct.mm_rss_stat, %struct.linux_binfmt*, %struct.mm_context_t, i64, %struct.core_state*, %struct.spinlock, %struct.kioctx_table*, %struct.user_namespace*, %struct.file*, %struct.mmu_notifier_mm*, %struct.atomic_t, i8, %struct.uprobes_state, %union.anon.13, %struct.work_struct }
%struct.rb_root = type { %struct.rb_node* }
%struct.mm_rss_stat = type { [4 x %union.anon.13] }
%struct.linux_binfmt = type opaque
%struct.mm_context_t = type { i64, %union.anon.13, %struct.rw_semaphore, %struct.ldt_struct*, i16, %struct.mutex, i8*, %struct.vdso_image*, %struct.atomic_t, i16, i16 }
%struct.ldt_struct = type opaque
%struct.vdso_image = type { i8*, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.core_state = type { %struct.atomic_t, %struct.core_thread, %struct.completion }
%struct.core_thread = type { %struct.task_struct*, %struct.core_thread* }
%struct.task_struct = type { %struct.thread_info, i64, i8*, %union.anon.17, i32, i32, %struct.llist_node, i32, i32, i32, i64, %struct.task_struct*, i32, i32, i32, i32, i32, i32, i32, %struct.sched_class*, %struct.sched_entity, %struct.sched_rt_entity, %struct.task_group*, %struct.sched_dl_entity, i32, i32, i32, %struct.cpumask*, %struct.cpumask, %struct.sched_info, %struct.list_head, %struct.plist_node, %struct.rb_node, %struct.mm_struct*, %struct.mm_struct*, %struct.vmacache, %struct.task_rss_stat, i32, i32, i32, i32, i64, i32, i8, [3 x i8], i8, i64, %struct.restart_block, i32, i32, i64, %struct.task_struct*, %struct.task_struct*, %struct.list_head, %struct.list_head, %struct.task_struct*, %struct.list_head, %struct.list_head, %struct.pid*, [4 x %struct.hlist_node], %struct.list_head, %struct.list_head, %struct.completion*, i32*, i32*, i64, i64, i64, %struct.prev_cputime, i64, i64, i64, i64, i64, i64, %struct.posix_cputimers, %struct.cred*, %struct.cred*, %struct.cred*, %struct.key*, [16 x i8], %struct.nameidata*, %struct.sysv_sem, %struct.sysv_shm, %struct.fs_struct*, %struct.files_struct*, %struct.nsproxy*, %struct.signal_struct*, %struct.sighand_struct*, %struct.cpumask, %struct.cpumask, %struct.cpumask, %struct.sigpending, i64, i64, i32, %struct.callback_head*, %struct.audit_context*, %struct.atomic_t, i32, %struct.seccomp, i32, i32, %struct.spinlock, %struct.raw_spinlock, %struct.wake_q_node, %struct.rb_root_cached, %struct.task_struct*, %struct.rt_mutex_waiter*, i8*, %struct.bio_list*, %struct.blk_plug*, %struct.reclaim_state*, %struct.backing_dev_info*, %struct.io_context*, %struct.capture_control*, i64, %struct.kernel_siginfo*, %struct.task_io_accounting, i64, i64, i64, %struct.cpumask, %struct.atomic_t, i32, i32, %struct.css_set*, %struct.list_head, %struct.robust_list_head*, %struct.compat_robust_list_head*, %struct.list_head, %struct.futex_pi_state*, [2 x %struct.perf_event_context*], %struct.mutex, %struct.list_head, %struct.mempolicy*, i16, i16, %struct.rseq*, i32, i64, %struct.tlbflush_unmap_batch, %union.anon.12, %struct.pipe_inode_info*, %struct.page_frag, %struct.task_delay_info*, i32, i32, i64, i64, i64, i64, i64, %struct.uprobe_task*, i32, %struct.task_struct*, %struct.vm_struct*, %union.anon.17, i8*, %struct.thread_struct }
%struct.thread_info = type { i64, i32 }
%struct.llist_node = type { %struct.llist_node* }
%struct.sched_class = type opaque
%struct.sched_entity = type { %struct.thread_info, i64, %struct.rb_node, %struct.list_head, i32, i64, i64, i64, i64, i64, %struct.sched_statistics, i32, %struct.sched_entity*, %struct.cfs_rq*, %struct.cfs_rq*, [24 x i8], %struct.sched_avg }
%struct.sched_statistics = type { i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.cfs_rq = type opaque
%struct.sched_avg = type { i64, i64, i64, i32, i32, i64, i64, i64, %struct.util_est }
%struct.util_est = type { i32, i32 }
%struct.sched_rt_entity = type { %struct.list_head, i64, i64, i32, i16, i16, %struct.sched_rt_entity* }
%struct.task_group = type opaque
%struct.sched_dl_entity = type { %struct.rb_node, i64, i64, i64, i64, i64, i64, i64, i32, i8, %struct.hrtimer, %struct.hrtimer }
%struct.hrtimer = type { %struct.timerqueue_node, i64, i32 (%struct.hrtimer*)*, %struct.hrtimer_clock_base*, i8, i8, i8, i8 }
%struct.hrtimer_clock_base = type { %struct.hrtimer_cpu_base*, i32, i32, %struct.atomic_t, %struct.hrtimer*, %struct.timerqueue_head, i64 ()*, i64 }
%struct.hrtimer_cpu_base = type { %struct.raw_spinlock, i32, i32, i32, i8, i32, i16, i16, i32, i64, %struct.hrtimer*, i64, %struct.hrtimer*, [8 x %struct.hrtimer_clock_base] }
%struct.timerqueue_head = type { %struct.rb_root_cached }
%struct.sched_info = type { i64, i64, i64, i64 }
%struct.plist_node = type { i32, %struct.list_head, %struct.list_head }
%struct.vmacache = type { i64, [4 x %struct.vm_area_struct*] }
%struct.task_rss_stat = type { i32, [4 x i32] }
%struct.restart_block = type { i64 (%struct.restart_block*)*, %union.anon.20 }
%union.anon.20 = type { %struct.anon.21 }
%struct.anon.21 = type { i32*, i32, i32, i32, i64, i32* }
%struct.pid = type { %union.anon.17, i32, [4 x %struct.hlist_head], %struct.wait_queue_head, %struct.callback_head, [1 x %struct.upid] }
%struct.wait_queue_head = type { %struct.spinlock, %struct.list_head }
%struct.upid = type { i32, %struct.pid_namespace* }
%struct.pid_namespace = type { %struct.qspinlock, %struct.idr, %struct.callback_head, i32, %struct.task_struct*, %struct.kmem_cache*, i32, %struct.pid_namespace*, %struct.vfsmount*, %struct.dentry*, %struct.dentry*, %struct.fs_pin*, %struct.user_namespace*, %struct.ucounts*, %struct.work_struct, %struct.atomic_t, i32, i32, %struct.ns_common }
%struct.idr = type { %struct.xarray, i32, i32 }
%struct.xarray = type { %struct.spinlock, i32, i8* }
%struct.kmem_cache = type opaque
%struct.fs_pin = type opaque
%struct.ucounts = type { %struct.hlist_node, %struct.user_namespace*, %struct.atomic_t, i32, [9 x %struct.atomic_t] }
%struct.ns_common = type { %union.anon.13, %struct.proc_ns_operations*, i32 }
%struct.proc_ns_operations = type opaque
%struct.prev_cputime = type { i64, i64, %struct.raw_spinlock }
%struct.posix_cputimers = type { [3 x %struct.posix_cputimer_base], i32, i32 }
%struct.posix_cputimer_base = type { i64, %struct.timerqueue_head }
%struct.key = type { %union.anon.17, i32, %union.anon.27, %struct.rw_semaphore, %struct.key_user*, i8*, %union.anon.13, i64, %struct.atomic_t, %struct.atomic_t, i32, i16, i16, i16, i64, %union.anon.29, %union.anon.33, %struct.key_restriction* }
%union.anon.27 = type { %struct.rb_node }
%struct.key_user = type opaque
%union.anon.29 = type { %struct.keyring_index_key }
%struct.keyring_index_key = type { i64, %union.anon.13, %struct.key_type*, %struct.key_tag*, i8* }
%struct.key_type = type opaque
%struct.key_tag = type { %struct.callback_head, %union.anon.17, i8 }
%union.anon.33 = type { %union.key_payload }
%union.key_payload = type { [4 x i8*] }
%struct.key_restriction = type { i32 (%struct.key*, %struct.key_type*, %union.key_payload*, %struct.key*)*, %struct.key*, %struct.key_type* }
%struct.nameidata = type opaque
%struct.sysv_sem = type { %struct.sem_undo_list* }
%struct.sem_undo_list = type opaque
%struct.fs_struct = type opaque
%struct.files_struct = type opaque
%struct.nsproxy = type { %struct.atomic_t, %struct.uts_namespace*, %struct.ipc_namespace*, %struct.mnt_namespace*, %struct.pid_namespace*, %struct.net*, %struct.cgroup_namespace* }
%struct.uts_namespace = type opaque
%struct.ipc_namespace = type opaque
%struct.mnt_namespace = type opaque
%struct.net = type { %union.anon.17, %union.anon.17, %struct.spinlock, i32, i32, i32, %struct.spinlock, %struct.atomic_t, %struct.list_head, %struct.list_head, %struct.llist_node, %struct.key_tag*, %struct.user_namespace*, %struct.ucounts*, %struct.idr, %struct.ns_common, %struct.list_head, %struct.proc_dir_entry*, %struct.proc_dir_entry*, %struct.ctl_table_set, %struct.sock*, %struct.sock*, %struct.uevent_sock*, %struct.hlist_head*, %struct.hlist_head*, i32, %struct.net_device*, %struct.list_head, %struct.netns_core, %struct.netns_mib, %struct.netns_packet, %struct.netns_unix, %struct.netns_nexthop, [16 x i8], %struct.netns_ipv4, %struct.netns_ipv6, %struct.netns_nf, %struct.netns_xt, %struct.netns_ct, %struct.netns_nf_frag, %struct.ctl_table_header*, %struct.sock*, %struct.sock*, %struct.net_generic*, %struct.bpf_prog*, [56 x i8], %struct.netns_xfrm, %struct.sock*, [56 x i8] }
%struct.proc_dir_entry = type opaque
%struct.ctl_table_set = type { i32 (%struct.ctl_table_set*)*, %struct.ctl_dir }
%struct.ctl_dir = type { %struct.ctl_table_header, %struct.rb_root }
%struct.ctl_table_header = type { %union.anon.35, %struct.completion*, %struct.ctl_table*, %struct.ctl_table_root*, %struct.ctl_table_set*, %struct.ctl_dir*, %struct.ctl_node*, %struct.hlist_head }
%union.anon.35 = type { %struct.anon.36 }
%struct.anon.36 = type { %struct.ctl_table*, i32, i32, i32 }
%struct.ctl_table = type { i8*, i8*, i32, i16, %struct.ctl_table*, i32 (%struct.ctl_table*, i32, i8*, i64*, i64*)*, %struct.ctl_table_poll*, i8*, i8* }
%struct.ctl_table_poll = type { %struct.atomic_t, %struct.wait_queue_head }
%struct.ctl_table_root = type { %struct.ctl_table_set, %struct.ctl_table_set* (%struct.ctl_table_root*)*, void (%struct.ctl_table_header*, %struct.ctl_table*, %struct.atomic_t*, %struct.atomic_t*)*, i32 (%struct.ctl_table_header*, %struct.ctl_table*)* }
%struct.ctl_node = type { %struct.rb_node, %struct.ctl_table_header* }
%struct.uevent_sock = type opaque
%struct.net_device = type { [16 x i8], %struct.hlist_node, %struct.dev_ifalias*, i64, i64, i64, i32, i64, %struct.list_head, %struct.list_head, %struct.list_head, %struct.list_head, %struct.list_head, %struct.list_head, %struct.anon.126, i64, i64, i64, i64, i64, i64, i64, i32, i32, %struct.net_device_stats, %union.anon.13, %union.anon.13, %union.anon.13, %struct.atomic_t, %struct.atomic_t, %struct.net_device_ops*, %struct.ethtool_ops*, %struct.ndisc_ops*, %struct.header_ops*, i32, i32, i16, i16, i8, i8, i8, i8, i32, i32, i32, i16, i16, i8, i16, i16, [32 x i8], i8, i8, i8, i8, i16, i16, i16, %struct.spinlock, i8, i8, %struct.netdev_hw_addr_list, %struct.netdev_hw_addr_list, %struct.netdev_hw_addr_list, %struct.kset*, i32, i32, %struct.in_device*, %struct.inet6_dev*, %struct.wireless_dev*, %struct.wpan_dev*, i8*, %struct.netdev_rx_queue*, i32, i32, %struct.bpf_prog*, i64, i32 (%struct.sk_buff**)*, i8*, %struct.mini_Qdisc*, %struct.netdev_queue*, %struct.nf_hook_entries*, [32 x i8], %struct.cpu_rmap*, %struct.hlist_node, [32 x i8], %struct.netdev_queue*, i32, i32, %struct.Qdisc*, [16 x %struct.hlist_head], i32, %struct.spinlock, i32, %struct.xps_dev_maps*, %struct.xps_dev_maps*, %struct.mini_Qdisc*, %struct.timer_list, i32*, %struct.list_head, %struct.list_head, i8, i8, i16, i8, void (%struct.net_device*)*, %struct.netpoll_info*, %struct.possible_net_t, %union.anon.142, %struct.device, [4 x %struct.attribute_group*], %struct.attribute_group*, %struct.rtnl_link_ops*, i32, i16, i16, [16 x %struct.nlattr], [16 x i8], %struct.phy_device*, %struct.sfp_bus*, %struct.u64_stats_sync, %struct.u64_stats_sync, %struct.u64_stats_sync, %struct.u64_stats_sync, i8, i8, [38 x i8] }
%struct.dev_ifalias = type { %struct.callback_head, [0 x i8] }
%struct.anon.126 = type { %struct.list_head, %struct.list_head }
%struct.net_device_stats = type { i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.net_device_ops = type { i32 (%struct.net_device*)*, void (%struct.net_device*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*)*, i32 (%struct.sk_buff*, %struct.net_device*)*, i64 (%struct.sk_buff*, %struct.net_device*, i64)*, i16 (%struct.net_device*, %struct.sk_buff*, %struct.net_device*)*, void (%struct.net_device*, i32)*, void (%struct.net_device*)*, i32 (%struct.net_device*, i8*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*, %struct.ifreq*, i32)*, i32 (%struct.net_device*, %struct.ifmap*)*, i32 (%struct.net_device*, i32)*, i32 (%struct.net_device*, %struct.neigh_parms*)*, void (%struct.net_device*)*, void (%struct.net_device*, %struct.rtnl_link_stats64*)*, i1 (%struct.net_device*, i32)*, i32 (i32, %struct.net_device*, i8*)*, %struct.net_device_stats* (%struct.net_device*)*, i32 (%struct.net_device*, i16, i16)*, i32 (%struct.net_device*, i16, i16)*, void (%struct.net_device*)*, i32 (%struct.net_device*, %struct.netpoll_info*)*, void (%struct.net_device*)*, i32 (%struct.net_device*, i32, i8*)*, i32 (%struct.net_device*, i32, i16, i8, i16)*, i32 (%struct.net_device*, i32, i32, i32)*, i32 (%struct.net_device*, i32, i1)*, i32 (%struct.net_device*, i32, i1)*, i32 (%struct.net_device*, i32, %struct.ifla_vf_info*)*, i32 (%struct.net_device*, i32, i32)*, i32 (%struct.net_device*, i32, %struct.ifla_vf_stats*)*, i32 (%struct.net_device*, i32, %struct.nlattr**)*, i32 (%struct.net_device*, i32, %struct.sk_buff*)*, i32 (%struct.net_device*, i32, i64, i32)*, i32 (%struct.net_device*, i32, i1)*, i32 (%struct.net_device*, i32, i8*)*, i32 (%struct.net_device*, %struct.sk_buff*, i16, i32)*, i32 (%struct.net_device*, %struct.net_device*, %struct.netlink_ext_ack*)*, i32 (%struct.net_device*, %struct.net_device*)*, i64 (%struct.net_device*, i64)*, i32 (%struct.net_device*, i64)*, i32 (%struct.net_device*, %struct.neighbour*)*, void (%struct.net_device*, %struct.neighbour*)*, i32 (%struct.ndmsg*, %struct.nlattr**, %struct.net_device*, i8*, i16, i16, %struct.netlink_ext_ack*)*, i32 (%struct.ndmsg*, %struct.nlattr**, %struct.net_device*, i8*, i16)*, i32 (%struct.sk_buff*, %struct.netlink_callback*, %struct.net_device*, %struct.net_device*, i32*)*, i32 (%struct.sk_buff*, %struct.nlattr**, %struct.net_device*, i8*, i16, i32, i32, %struct.netlink_ext_ack*)*, i32 (%struct.net_device*, %struct.nlmsghdr*, i16, %struct.netlink_ext_ack*)*, i32 (%struct.sk_buff*, i32, i32, %struct.net_device*, i32, i32)*, i32 (%struct.net_device*, %struct.nlmsghdr*, i16)*, i32 (%struct.net_device*, i1)*, i32 (%struct.net_device*, %struct.netdev_phys_item_id*)*, i32 (%struct.net_device*, %struct.netdev_phys_item_id*)*, i32 (%struct.net_device*, i8*, i64)*, void (%struct.net_device*, %struct.udp_tunnel_info*)*, void (%struct.net_device*, %struct.udp_tunnel_info*)*, i8* (%struct.net_device*, %struct.net_device*)*, void (%struct.net_device*, i8*)*, i32 (%struct.net_device*, i32, i32)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*, i1)*, i32 (%struct.net_device*, %struct.sk_buff*)*, void (%struct.net_device*, i32)*, i32 (%struct.net_device*, %struct.netdev_bpf*)*, i32 (%struct.net_device*, i32, %struct.xdp_frame**, i32)*, i32 (%struct.net_device*, i32, i32)*, %struct.devlink_port* (%struct.net_device*)* }
%struct.sk_buff = type { %union.anon.40, %union.anon.43, %union.anon.13, [48 x i8], %union.anon.45, i64, i32, i32, i16, i16, i16, [0 x i8], i8, i8, [0 x i32], [0 x i8], i16, [0 x i8], i16, i16, %struct.atomic_t, i32, i32, i32, i16, i16, %struct.atomic_t, i32, %struct.atomic_t, %union.anon.51, i16, i16, i16, i16, i16, i16, i16, [0 x i32], i32, i32, i8*, i8*, i32, %union.anon.17, %struct.skb_ext* }
%union.anon.40 = type { %struct.anon.41 }
%struct.anon.41 = type { %struct.sk_buff*, %struct.sk_buff*, %union.anon.42 }
%union.anon.42 = type { %struct.net_device* }
%union.anon.43 = type { %struct.sock* }
%union.anon.45 = type { %struct.anon.46 }
%struct.anon.46 = type { i64, void (%struct.sk_buff*)* }
%union.anon.51 = type { i16 }
%struct.skb_ext = type { %union.anon.17, [1 x i8], i8, [2 x i8], [0 x i8] }
%struct.ifreq = type { %union.anon.127, %union.anon.128 }
%union.anon.128 = type { %struct.ifmap }
%struct.ifmap = type { i64, i64, i16, i8, i8, i8 }
%struct.neigh_parms = type opaque
%struct.rtnl_link_stats64 = type { i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.ifla_vf_info = type { i32, [32 x i8], i32, i32, i32, i32, i32, i32, i32, i32, i16 }
%struct.ifla_vf_stats = type { i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.nlattr = type { i16, i16 }
%struct.netlink_ext_ack = type { i8*, %struct.nlattr*, [20 x i8], i8 }
%struct.neighbour = type opaque
%struct.ndmsg = type { i8, i8, i16, i32, i16, i8, i8 }
%struct.netlink_callback = type { %struct.sk_buff*, %struct.nlmsghdr*, i32 (%struct.sk_buff*, %struct.netlink_callback*)*, i32 (%struct.netlink_callback*)*, i8*, %struct.module*, %struct.netlink_ext_ack*, i16, i16, i8, i16, i32, i32, %union.anon.130 }
%struct.nlmsghdr = type { i32, i16, i16, i32, i32 }
%union.anon.130 = type { [6 x i64] }
%struct.netdev_phys_item_id = type { [32 x i8], i8 }
%struct.udp_tunnel_info = type opaque
%struct.netdev_bpf = type { i32, %union.anon.131 }
%union.anon.131 = type { %struct.anon.132 }
%struct.anon.132 = type { i32, %struct.bpf_prog*, %struct.netlink_ext_ack* }
%struct.xdp_frame = type { i8*, i16, i16, i16, %struct.util_est, %struct.net_device* }
%struct.devlink_port = type opaque
%struct.ethtool_ops = type { void (%struct.net_device*, %struct.ethtool_drvinfo*)*, i32 (%struct.net_device*)*, void (%struct.net_device*, %struct.ethtool_regs*, i8*)*, void (%struct.net_device*, %struct.ethtool_wolinfo*)*, i32 (%struct.net_device*, %struct.ethtool_wolinfo*)*, i32 (%struct.net_device*)*, void (%struct.net_device*, i32)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*, %struct.ethtool_eeprom*, i8*)*, i32 (%struct.net_device*, %struct.ethtool_eeprom*, i8*)*, i32 (%struct.net_device*, %struct.ethtool_coalesce*)*, i32 (%struct.net_device*, %struct.ethtool_coalesce*)*, void (%struct.net_device*, %struct.ethtool_ringparam*)*, i32 (%struct.net_device*, %struct.ethtool_ringparam*)*, void (%struct.net_device*, %struct.ethtool_pauseparam*)*, i32 (%struct.net_device*, %struct.ethtool_pauseparam*)*, void (%struct.net_device*, %struct.ethtool_test*, i64*)*, void (%struct.net_device*, i32, i8*)*, i32 (%struct.net_device*, i32)*, void (%struct.net_device*, %struct.ethtool_stats*, i64*)*, i32 (%struct.net_device*)*, void (%struct.net_device*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*, i32)*, i32 (%struct.net_device*, i32)*, i32 (%struct.net_device*, %struct.ethtool_rxnfc*, i32*)*, i32 (%struct.net_device*, %struct.ethtool_rxnfc*)*, i32 (%struct.net_device*, %struct.ethtool_flash*)*, i32 (%struct.net_device*, i32*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*)*, i32 (%struct.net_device*, i32*, i8*, i8*)*, i32 (%struct.net_device*, i32*, i8*, i8)*, i32 (%struct.net_device*, i32*, i8*, i8*, i32)*, i32 (%struct.net_device*, i32*, i8*, i8, i32*, i1)*, void (%struct.net_device*, %struct.ethtool_ringparam*)*, i32 (%struct.net_device*, %struct.ethtool_ringparam*)*, i32 (%struct.net_device*, %struct.ethtool_eeprom*)*, i32 (%struct.net_device*, %struct.ethtool_eeprom*, i8*)*, i32 (%struct.net_device*, %struct.ethtool_eeprom*)*, i32 (%struct.net_device*, %struct.ethtool_ts_info*)*, i32 (%struct.net_device*, %struct.ethtool_modinfo*)*, i32 (%struct.net_device*, %struct.ethtool_eeprom*, i8*)*, i32 (%struct.net_device*, %struct.ethtool_eee*)*, i32 (%struct.net_device*, %struct.ethtool_eee*)*, i32 (%struct.net_device*, %struct.ethtool_tunable*, i8*)*, i32 (%struct.net_device*, %struct.ethtool_tunable*, i8*)*, i32 (%struct.net_device*, i32, %struct.ethtool_coalesce*)*, i32 (%struct.net_device*, i32, %struct.ethtool_coalesce*)*, i32 (%struct.net_device*, %struct.ethtool_link_ksettings*)*, i32 (%struct.net_device*, %struct.ethtool_link_ksettings*)*, i32 (%struct.net_device*, %struct.ethtool_pauseparam*)*, i32 (%struct.net_device*, %struct.ethtool_pauseparam*)*, void (%struct.net_device*, %struct.ethtool_stats*, i64*)* }
%struct.ethtool_drvinfo = type { i32, [32 x i8], [32 x i8], [32 x i8], [32 x i8], [32 x i8], [12 x i8], i32, i32, i32, i32, i32 }
%struct.ethtool_regs = type { i32, i32, i32, [0 x i8] }
%struct.ethtool_wolinfo = type { i32, i32, i32, [6 x i8] }
%struct.ethtool_coalesce = type { i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32 }
%struct.ethtool_pauseparam = type { i32, i32, i32, i32 }
%struct.ethtool_test = type { i32, i32, i32, i32, [0 x i64] }
%struct.ethtool_rxnfc = type { i32, i32, i64, %struct.ethtool_rx_flow_spec, %struct.atomic_t, [0 x i32] }
%struct.ethtool_rx_flow_spec = type { i32, %union.ethtool_flow_union, %struct.ethtool_flow_ext, %union.ethtool_flow_union, %struct.ethtool_flow_ext, i64, i32 }
%union.ethtool_flow_union = type { %struct.ethtool_tcpip6_spec, [12 x i8] }
%struct.ethtool_tcpip6_spec = type { [4 x i32], [4 x i32], i16, i16, i8 }
%struct.ethtool_flow_ext = type { [2 x i8], [6 x i8], i16, i16, [2 x i32] }
%struct.ethtool_flash = type { i32, i32, [128 x i8] }
%struct.ethtool_ringparam = type { i32, i32, i32, i32, i32, i32, i32, i32, i32 }
%struct.ethtool_eeprom = type { i32, i32, i32, i32, [0 x i8] }
%struct.ethtool_ts_info = type { i32, i32, i32, i32, [3 x i32], i32, [3 x i32] }
%struct.ethtool_modinfo = type { i32, i32, i32, [8 x i32] }
%struct.ethtool_eee = type { i32, i32, i32, i32, i32, i32, i32, i32, [2 x i32] }
%struct.ethtool_tunable = type { i32, i32, i32, i32, [0 x i8*] }
%struct.ethtool_link_ksettings = type { %struct.ethtool_link_settings, %struct.anon.137 }
%struct.ethtool_link_settings = type { i32, i32, i8, i8, i8, i8, i8, i8, i8, i8, i8, [3 x i8], [7 x i32], [0 x i32] }
%struct.anon.137 = type { [2 x i64], [2 x i64], [2 x i64] }
%struct.ethtool_stats = type { i32, i32, [0 x i64] }
%struct.ndisc_ops = type opaque
%struct.header_ops = type { i32 (%struct.sk_buff*, %struct.net_device*, i16, i8*, i8*, i32)*, i32 (%struct.sk_buff*, i8*)*, i32 (%struct.neighbour*, %struct.hh_cache*, i16)*, void (%struct.hh_cache*, %struct.net_device*, i8*)*, i1 (i8*, i32)*, i16 (%struct.sk_buff*)* }
%struct.hh_cache = type { i32, %struct.seqlock_t, [12 x i64] }
%struct.seqlock_t = type { %struct.atomic_t, %struct.spinlock }
%struct.netdev_hw_addr_list = type { %struct.list_head, i32 }
%struct.in_device = type opaque
%struct.inet6_dev = type opaque
%struct.wireless_dev = type opaque
%struct.wpan_dev = type opaque
%struct.netdev_rx_queue = type { %struct.rps_map*, %struct.rps_dev_flow_table*, %struct.kobject, %struct.net_device*, [40 x i8], %struct.xdp_rxq_info }
%struct.rps_map = type { i32, %struct.callback_head, [0 x i16] }
%struct.rps_dev_flow_table = type { i32, %struct.callback_head, [0 x %struct.rps_dev_flow] }
%struct.rps_dev_flow = type { i16, i16, i32 }
%struct.xdp_rxq_info = type { %struct.net_device*, i32, i32, %struct.util_est, [40 x i8] }
%struct.nf_hook_entries = type opaque
%struct.cpu_rmap = type opaque
%struct.netdev_queue = type { %struct.net_device*, %struct.Qdisc*, %struct.Qdisc*, %struct.kobject, i32, i64, i64, %struct.net_device*, [8 x i8], %struct.spinlock, i32, i64, i64, [40 x i8], %struct.dql }
%struct.dql = type { i32, i32, i32, [52 x i8], i32, i32, i32, i32, i32, i32, i64, i32, i32, i32, [20 x i8] }
%struct.Qdisc = type { i32 (%struct.sk_buff*, %struct.Qdisc*, %struct.sk_buff**)*, %struct.sk_buff* (%struct.Qdisc*)*, i32, i32, %struct.Qdisc_ops*, %struct.qdisc_size_table*, %struct.hlist_node, i32, i32, %struct.netdev_queue*, %struct.net_rate_estimator*, %struct.gnet_stats_basic_cpu*, %struct.gnet_stats_queue*, i32, %union.anon.17, [24 x i8], %struct.sk_buff_head, %struct.sk_buff_head, %struct.gnet_stats_basic_packed, %struct.atomic_t, %struct.gnet_stats_queue, i64, %struct.Qdisc*, %struct.sk_buff_head, %struct.spinlock, %struct.spinlock, i8, %struct.callback_head, [32 x i8] }
%struct.Qdisc_ops = type { %struct.Qdisc_ops*, %struct.Qdisc_class_ops*, [16 x i8], i32, i32, i32 (%struct.sk_buff*, %struct.Qdisc*, %struct.sk_buff**)*, %struct.sk_buff* (%struct.Qdisc*)*, %struct.sk_buff* (%struct.Qdisc*)*, i32 (%struct.Qdisc*, %struct.nlattr*, %struct.netlink_ext_ack*)*, void (%struct.Qdisc*)*, void (%struct.Qdisc*)*, i32 (%struct.Qdisc*, %struct.nlattr*, %struct.netlink_ext_ack*)*, void (%struct.Qdisc*)*, i32 (%struct.Qdisc*, i32)*, i32 (%struct.Qdisc*, %struct.sk_buff*)*, i32 (%struct.Qdisc*, %struct.gnet_dump*)*, void (%struct.Qdisc*, i32)*, void (%struct.Qdisc*, i32)*, i32 (%struct.Qdisc*)*, i32 (%struct.Qdisc*)*, %struct.module* }
%struct.Qdisc_class_ops = type { i32, %struct.netdev_queue* (%struct.Qdisc*, %struct.tcmsg*)*, i32 (%struct.Qdisc*, i64, %struct.Qdisc*, %struct.Qdisc**, %struct.netlink_ext_ack*)*, %struct.Qdisc* (%struct.Qdisc*, i64)*, void (%struct.Qdisc*, i64)*, i64 (%struct.Qdisc*, i32)*, i32 (%struct.Qdisc*, i32, i32, %struct.nlattr**, i64*, %struct.netlink_ext_ack*)*, i32 (%struct.Qdisc*, i64)*, void (%struct.Qdisc*, %struct.qdisc_walker*)*, %struct.tcf_block* (%struct.Qdisc*, i64, %struct.netlink_ext_ack*)*, i64 (%struct.Qdisc*, i64, i32)*, void (%struct.Qdisc*, i64)*, i32 (%struct.Qdisc*, i64, %struct.sk_buff*, %struct.tcmsg*)*, i32 (%struct.Qdisc*, i64, %struct.gnet_dump*)* }
%struct.tcmsg = type { i8, i8, i16, i32, i32, i32, i32 }
%struct.qdisc_walker = type opaque
%struct.tcf_block = type { %struct.mutex, %struct.list_head, i32, %union.anon.17, %struct.net*, %struct.Qdisc*, %struct.rw_semaphore, %struct.sysv_shm, %struct.list_head, i8, %struct.atomic_t, i32, i32, %struct.anon.141, %struct.callback_head, [128 x %struct.hlist_head], %struct.mutex }
%struct.anon.141 = type { %struct.tcf_chain*, %struct.list_head }
%struct.tcf_chain = type { %struct.mutex, %struct.tcf_proto*, %struct.list_head, %struct.tcf_block*, i32, i32, i32, i8, i8, %struct.tcf_proto_ops*, i8*, %struct.callback_head }
%struct.tcf_proto = type { %struct.tcf_proto*, i8*, i32 (%struct.sk_buff*, %struct.tcf_proto*, %struct.tcf_result*)*, i16, i32, i8*, %struct.tcf_proto_ops*, %struct.tcf_chain*, %struct.spinlock, i8, %union.anon.17, %struct.callback_head, %struct.hlist_node }
%struct.tcf_result = type { %union.anon.138 }
%union.anon.138 = type { %struct.thread_info }
%struct.tcf_proto_ops = type { %struct.list_head, [16 x i8], i32 (%struct.sk_buff*, %struct.tcf_proto*, %struct.tcf_result*)*, i32 (%struct.tcf_proto*)*, void (%struct.tcf_proto*, i1, %struct.netlink_ext_ack*)*, i8* (%struct.tcf_proto*, i32)*, void (%struct.tcf_proto*, i8*)*, i32 (%struct.net*, %struct.sk_buff*, %struct.tcf_proto*, i64, i32, %struct.nlattr**, i8**, i1, i1, %struct.netlink_ext_ack*)*, i32 (%struct.tcf_proto*, i8*, i8*, i1, %struct.netlink_ext_ack*)*, void (%struct.tcf_proto*, %struct.tcf_walker*, i1)*, i32 (%struct.tcf_proto*, i1, i32 (i32, i8*, i8*)*, i8*, %struct.netlink_ext_ack*)*, void (%struct.tcf_proto*, i8*)*, void (%struct.tcf_proto*, i8*)*, void (i8*, i32, i64)*, i8* (%struct.net*, %struct.tcf_chain*, %struct.nlattr**, %struct.netlink_ext_ack*)*, void (i8*)*, i32 (%struct.net*, %struct.tcf_proto*, i8*, %struct.sk_buff*, %struct.tcmsg*, i1)*, i32 (%struct.sk_buff*, %struct.net*, i8*)*, %struct.module*, i32 }
%struct.tcf_walker = type opaque
%struct.gnet_dump = type { %struct.spinlock*, %struct.sk_buff*, %struct.nlattr*, i32, i32, i32, i8*, i32, %struct.tc_stats }
%struct.tc_stats = type { i64, i32, i32, i32, i32, i32, i32, i32 }
%struct.qdisc_size_table = type { %struct.callback_head, %struct.list_head, %struct.tc_sizespec, i32, [0 x i16] }
%struct.tc_sizespec = type { i8, i8, i16, i32, i32, i32, i32, i32 }
%struct.net_rate_estimator = type opaque
%struct.gnet_stats_basic_cpu = type { %struct.gnet_stats_basic_packed, %struct.u64_stats_sync, [4 x i8] }
%struct.gnet_stats_basic_packed = type <{ i64, i32 }>
%struct.gnet_stats_queue = type { i32, i32, i32, i32, i32 }
%struct.sk_buff_head = type { %struct.sk_buff*, %struct.sk_buff*, i32, %struct.spinlock }
%struct.xps_dev_maps = type { %struct.callback_head, [0 x %struct.xps_map*] }
%struct.xps_map = type { i32, i32, %struct.callback_head, [0 x i16] }
%struct.mini_Qdisc = type { %struct.tcf_proto*, %struct.gnet_stats_basic_cpu*, %struct.gnet_stats_queue*, %struct.callback_head }
%struct.timer_list = type { %struct.hlist_node, i64, void (%struct.timer_list*)*, i32 }
%struct.netpoll_info = type opaque
%struct.possible_net_t = type { %struct.net* }
%union.anon.142 = type { i8* }
%struct.device = type { %struct.kobject, %struct.device*, %struct.device_private*, i8*, %struct.device_type*, %struct.bus_type*, %struct.device_driver*, i8*, i8*, %struct.mutex, %struct.dev_links_info, %struct.dev_pm_info, %struct.dev_pm_domain*, %struct.irq_domain*, %struct.list_head, %struct.dma_map_ops*, i64*, i64, i64, i64, %struct.device_dma_parameters*, %struct.list_head, %union.anon.142, %struct.device_node*, %struct.fwnode_handle*, i32, i32, i32, %struct.spinlock, %struct.list_head, %struct.class*, %struct.attribute_group**, void (%struct.device*)*, %struct.iommu_group*, %struct.iommu_fwspec*, %struct.iommu_param*, i8 }
%struct.device_private = type opaque
%struct.device_type = type { i8*, %struct.attribute_group**, i32 (%struct.device*, %struct.kobj_uevent_env*)*, i8* (%struct.device*, i16*, %struct.atomic_t*, %struct.atomic_t*)*, void (%struct.device*)*, %struct.dev_pm_ops* }
%struct.dev_pm_ops = type { i32 (%struct.device*)*, void (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)* }
%struct.bus_type = type { i8*, i8*, %struct.device*, %struct.attribute_group**, %struct.attribute_group**, %struct.attribute_group**, i32 (%struct.device*, %struct.device_driver*)*, i32 (%struct.device*, %struct.kobj_uevent_env*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, void (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*, i32)*, i32 (%struct.device*)*, i32 (%struct.device*)*, i32 (%struct.device*)*, %struct.dev_pm_ops*, %struct.iommu_ops*, %struct.subsys_private*, %struct.u64_stats_sync, i8 }
%struct.iommu_ops = type opaque
%struct.subsys_private = type opaque
%struct.device_driver = type { i8*, %struct.bus_type*, %struct.module*, i8*, i8, i32, %struct.of_device_id*, %struct.acpi_device_id*, i32 (%struct.device*)*, i32 (%struct.device*)*, void (%struct.device*)*, i32 (%struct.device*, i32)*, i32 (%struct.device*)*, %struct.attribute_group**, %struct.attribute_group**, %struct.dev_pm_ops*, void (%struct.device*)*, %struct.driver_private* }
%struct.of_device_id = type opaque
%struct.acpi_device_id = type opaque
%struct.driver_private = type opaque
%struct.dev_links_info = type { %struct.list_head, %struct.list_head, i32 }
%struct.dev_pm_info = type { %struct.atomic_t, i16, i32, %struct.spinlock, %struct.list_head, %struct.completion, %struct.wakeup_source*, i8, %struct.hrtimer, i64, %struct.work_struct, %struct.wait_queue_head, %struct.wake_irq*, %struct.atomic_t, %struct.atomic_t, i16, i32, i32, i32, i32, i32, i64, i64, i64, i64, %struct.pm_subsys_data*, void (%struct.device*, i32)*, %struct.dev_pm_qos* }
%struct.wakeup_source = type { i8*, i32, %struct.list_head, %struct.spinlock, %struct.wake_irq*, %struct.timer_list, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, %struct.device*, i8 }
%struct.wake_irq = type opaque
%struct.pm_subsys_data = type { %struct.spinlock, i32, %struct.list_head }
%struct.dev_pm_qos = type opaque
%struct.dev_pm_domain = type { %struct.dev_pm_ops, void (%struct.device*, i1)*, i32 (%struct.device*)*, void (%struct.device*)*, void (%struct.device*)* }
%struct.irq_domain = type opaque
%struct.dma_map_ops = type { i8* (%struct.device*, i64, i64*, i32, i64)*, void (%struct.device*, i64, i8*, i64, i64)*, i32 (%struct.device*, %struct.vm_area_struct*, i8*, i64, i64, i64)*, i32 (%struct.device*, %struct.sg_table*, i8*, i64, i64, i64)*, i64 (%struct.device*, %struct.page*, i64, i64, i32, i64)*, void (%struct.device*, i64, i64, i32, i64)*, i32 (%struct.device*, %struct.scatterlist*, i32, i32, i64)*, void (%struct.device*, %struct.scatterlist*, i32, i32, i64)*, i64 (%struct.device*, i64, i64, i32, i64)*, void (%struct.device*, i64, i64, i32, i64)*, void (%struct.device*, i64, i64, i32)*, void (%struct.device*, i64, i64, i32)*, void (%struct.device*, %struct.scatterlist*, i32, i32)*, void (%struct.device*, %struct.scatterlist*, i32, i32)*, void (%struct.device*, i8*, i64, i32)*, i32 (%struct.device*, i64)*, i64 (%struct.device*)*, i64 (%struct.device*)*, i64 (%struct.device*)* }
%struct.sg_table = type { %struct.scatterlist*, i32, i32 }
%struct.scatterlist = type { i64, i32, i32, i64, i32 }
%struct.page = type { i64, %union.anon.57, %union.anon.17, %struct.atomic_t, [8 x i8] }
%union.anon.57 = type { %struct.anon.58 }
%struct.anon.58 = type { %struct.list_head, %struct.address_space*, i64, i64 }
%struct.device_dma_parameters = type { i32, i64 }
%struct.device_node = type opaque
%struct.fwnode_handle = type { %struct.fwnode_handle*, %struct.fwnode_operations* }
%struct.fwnode_operations = type { %struct.fwnode_handle* (%struct.fwnode_handle*)*, void (%struct.fwnode_handle*)*, i1 (%struct.fwnode_handle*)*, i8* (%struct.fwnode_handle*, %struct.device*)*, i1 (%struct.fwnode_handle*, i8*)*, i32 (%struct.fwnode_handle*, i8*, i32, i8*, i64)*, i32 (%struct.fwnode_handle*, i8*, i8**, i64)*, %struct.fwnode_handle* (%struct.fwnode_handle*)*, %struct.fwnode_handle* (%struct.fwnode_handle*, %struct.fwnode_handle*)*, %struct.fwnode_handle* (%struct.fwnode_handle*, i8*)*, i32 (%struct.fwnode_handle*, i8*, i8*, i32, i32, %struct.fwnode_reference_args*)*, %struct.fwnode_handle* (%struct.fwnode_handle*, %struct.fwnode_handle*)*, %struct.fwnode_handle* (%struct.fwnode_handle*)*, %struct.fwnode_handle* (%struct.fwnode_handle*)*, i32 (%struct.fwnode_handle*, %struct.fwnode_endpoint*)* }
%struct.fwnode_reference_args = type { %struct.fwnode_handle*, i32, [8 x i64] }
%struct.fwnode_endpoint = type { i32, i32, %struct.fwnode_handle* }
%struct.class = type { i8*, %struct.module*, %struct.attribute_group**, %struct.attribute_group**, %struct.kobject*, i32 (%struct.device*, %struct.kobj_uevent_env*)*, i8* (%struct.device*, i16*)*, void (%struct.class*)*, void (%struct.device*)*, i32 (%struct.device*)*, %struct.kobj_ns_type_operations*, i8* (%struct.device*)*, void (%struct.device*, %struct.atomic_t*, %struct.atomic_t*)*, %struct.dev_pm_ops*, %struct.subsys_private* }
%struct.kobj_ns_type_operations = type { i32, i1 ()*, i8* ()*, i8* (%struct.sock*)*, i8* ()*, void (i8*)* }
%struct.iommu_group = type opaque
%struct.iommu_fwspec = type opaque
%struct.iommu_param = type opaque
%struct.rtnl_link_ops = type { %struct.list_head, i8*, i64, void (%struct.net_device*)*, i32, %struct.nla_policy*, i32 (%struct.nlattr**, %struct.nlattr**, %struct.netlink_ext_ack*)*, i32 (%struct.net*, %struct.net_device*, %struct.nlattr**, %struct.nlattr**, %struct.netlink_ext_ack*)*, i32 (%struct.net_device*, %struct.nlattr**, %struct.nlattr**, %struct.netlink_ext_ack*)*, void (%struct.net_device*, %struct.list_head*)*, i64 (%struct.net_device*)*, i32 (%struct.sk_buff*, %struct.net_device*)*, i64 (%struct.net_device*)*, i32 (%struct.sk_buff*, %struct.net_device*)*, i32 ()*, i32 ()*, i32, %struct.nla_policy*, i32 (%struct.net_device*, %struct.net_device*, %struct.nlattr**, %struct.nlattr**, %struct.netlink_ext_ack*)*, i64 (%struct.net_device*, %struct.net_device*)*, i32 (%struct.sk_buff*, %struct.net_device*, %struct.net_device*)*, %struct.net* (%struct.net_device*)*, i64 (%struct.net_device*, i32)*, i32 (%struct.sk_buff*, %struct.net_device*, i32*, i32)* }
%struct.nla_policy = type { i8, i8, i16, %union.anon.142 }
%struct.phy_device = type opaque
%struct.sfp_bus = type opaque
%struct.netns_core = type { %struct.ctl_table_header*, i32, i32*, %struct.prot_inuse* }
%struct.prot_inuse = type opaque
%struct.netns_mib = type { %struct.tcp_mib*, %struct.ipstats_mib*, %struct.linux_mib*, %struct.udp_mib*, %struct.udp_mib*, %struct.icmp_mib*, %struct.icmpmsg_mib*, %struct.proc_dir_entry*, %struct.udp_mib*, %struct.udp_mib*, %struct.ipstats_mib*, %union.anon.130*, %struct.icmpmsg_mib* }
%struct.tcp_mib = type { [16 x i64] }
%struct.linux_mib = type { [120 x i64] }
%struct.icmp_mib = type { [28 x i64] }
%struct.udp_mib = type { [9 x i64] }
%struct.ipstats_mib = type { [37 x i64], %struct.u64_stats_sync }
%struct.icmpmsg_mib = type { [512 x %union.anon.13] }
%struct.netns_packet = type { %struct.mutex, %struct.hlist_head }
%struct.netns_unix = type { i32, %struct.ctl_table_header* }
%struct.netns_nexthop = type { %struct.rb_root, %struct.hlist_head*, i32, i32 }
%struct.netns_ipv4 = type { %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ipv4_devconf*, %struct.ipv4_devconf*, %struct.ip_ra_chain*, %struct.mutex, %struct.fib_rules_ops*, i8, i32, %struct.fib_table*, %struct.fib_table*, i8, %struct.hlist_head*, i8, %struct.sock*, %struct.sock**, %struct.sock*, %struct.inet_peer_base*, %struct.sock**, %struct.fqdir*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, i32, i32, i32, i32, i32, i32, %struct.local_ports, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, [3 x i32], [3 x i32], i32, i64, %struct.inet_timewait_death_row, i32, i32, %struct.tcp_congestion_ops*, %struct.tcp_fastopen_context*, %struct.spinlock, i32, %struct.atomic_t, i64, i32, i32, i32, i32, i32, i32, %struct.ping_group_range, %struct.atomic_t, i64*, i32, %struct.mr_table*, i32, i32, %struct.fib_notifier_ops*, i32, %struct.fib_notifier_ops*, i32, %struct.atomic_t, %struct.siphash_key_t, [16 x i8] }
%struct.ipv4_devconf = type opaque
%struct.ip_ra_chain = type opaque
%struct.fib_rules_ops = type opaque
%struct.fib_table = type opaque
%struct.inet_peer_base = type opaque
%struct.fqdir = type { i64, i64, i32, i32, %struct.inet_frags*, %struct.net*, i8, [23 x i8], %struct.rhashtable, [56 x i8], %union.anon.13, %struct.work_struct, [24 x i8] }
%struct.inet_frags = type { i32, void (%struct.inet_frag_queue*, i8*)*, void (%struct.inet_frag_queue*)*, void (%struct.timer_list*)*, %struct.kmem_cache*, i8*, %struct.rhashtable_params, %union.anon.17, %struct.completion }
%struct.inet_frag_queue = type { %struct.rhash_head, %union.anon.38, %struct.timer_list, %struct.spinlock, %union.anon.17, %struct.rb_root, %struct.sk_buff*, %struct.sk_buff*, i64, i32, i32, i8, i16, %struct.fqdir*, %struct.callback_head }
%struct.rhash_head = type { %struct.rhash_head* }
%union.anon.38 = type { %struct.frag_v6_compare_key }
%struct.frag_v6_compare_key = type { %struct.in6_addr, %struct.in6_addr, i32, i32, i32 }
%struct.in6_addr = type { %union.anon.39 }
%union.anon.39 = type { [4 x i32] }
%struct.rhashtable_params = type { i16, i16, i16, i16, i32, i16, i8, i32 (i8*, i32, i32)*, i32 (i8*, i32, i32)*, i32 (%struct.rhashtable_compare_arg*, i8*)* }
%struct.rhashtable_compare_arg = type { %struct.rhashtable*, i8* }
%struct.rhashtable = type { %struct.bucket_table*, i32, i32, %struct.rhashtable_params, i8, %struct.work_struct, %struct.mutex, %struct.spinlock, %struct.atomic_t }
%struct.bucket_table = type { i32, i32, i32, %struct.list_head, %struct.callback_head, %struct.bucket_table*, %struct.u64_stats_sync, [8 x i8], [0 x %struct.u64_stats_sync*] }
%struct.xt_table = type opaque
%struct.local_ports = type { %struct.seqlock_t, [2 x i32], i8 }
%struct.inet_timewait_death_row = type { %struct.atomic_t, [60 x i8], %struct.inet_hashinfo*, i32, [52 x i8] }
%struct.inet_hashinfo = type opaque
%struct.tcp_congestion_ops = type opaque
%struct.tcp_fastopen_context = type opaque
%struct.ping_group_range = type { %struct.seqlock_t, [2 x %struct.atomic_t] }
%struct.mr_table = type opaque
%struct.fib_notifier_ops = type opaque
%struct.siphash_key_t = type { [2 x i64] }
%struct.netns_ipv6 = type { %struct.netns_sysctl_ipv6, %struct.ipv6_devconf*, %struct.ipv6_devconf*, %struct.inet_peer_base*, %struct.fqdir*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, %struct.xt_table*, %struct.fib6_info*, %struct.rt6_info*, %struct.rt6_statistics*, %struct.timer_list, %struct.hlist_head*, %struct.fib6_table*, %struct.list_head, [16 x i8], %struct.dst_ops, %struct.rwlock_t, %struct.spinlock, i32, i64, %struct.sock**, %struct.sock*, %struct.sock*, %struct.sock*, %struct.sock*, %struct.atomic_t, %struct.atomic_t, %struct.seg6_pernet_data*, %struct.fib_notifier_ops*, %struct.fib_notifier_ops*, i32, %struct.anon.54, [8 x i8] }
%struct.netns_sysctl_ipv6 = type { %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ctl_table_header*, %struct.ctl_table_header*, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, [4 x i64], i64*, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i8 }
%struct.ipv6_devconf = type opaque
%struct.fib6_info = type opaque
%struct.rt6_info = type opaque
%struct.rt6_statistics = type opaque
%struct.fib6_table = type opaque
%struct.dst_ops = type { i16, i32, i32 (%struct.dst_ops*)*, %struct.dst_entry* (%struct.dst_entry*, i32)*, i32 (%struct.dst_entry*)*, i32 (%struct.dst_entry*)*, i32* (%struct.dst_entry*, i64)*, void (%struct.dst_entry*)*, void (%struct.dst_entry*, %struct.net_device*, i32)*, %struct.dst_entry* (%struct.dst_entry*)*, void (%struct.sk_buff*)*, void (%struct.dst_entry*, %struct.sock*, %struct.sk_buff*, i32)*, void (%struct.dst_entry*, %struct.sock*, %struct.sk_buff*)*, i32 (%struct.net*, %struct.sock*, %struct.sk_buff*)*, %struct.neighbour* (%struct.dst_entry*, %struct.sk_buff*, i8*)*, void (%struct.dst_entry*, i8*)*, %struct.kmem_cache*, %struct.percpu_counter, [24 x i8] }
%struct.dst_entry = type opaque
%struct.percpu_counter = type { %struct.raw_spinlock, i64, %struct.list_head, i32* }
%struct.rwlock_t = type { %struct.qrwlock }
%struct.qrwlock = type { %union.anon.17, %struct.qspinlock }
%struct.seg6_pernet_data = type opaque
%struct.anon.54 = type { %struct.hlist_head, %struct.spinlock, i32 }
%struct.netns_nf = type { %struct.proc_dir_entry*, %struct.nf_queue_handler*, [13 x %struct.nf_logger*], %struct.ctl_table_header*, [5 x %struct.nf_hook_entries*], [5 x %struct.nf_hook_entries*], i8, i8 }
%struct.nf_queue_handler = type opaque
%struct.nf_logger = type opaque
%struct.netns_xt = type { [13 x %struct.list_head], i8, i8 }
%struct.netns_ct = type { %struct.atomic_t, i32, i8, %struct.ctl_table_header*, i32, i32, i32, i32, i32, i32, %struct.ct_pcpu*, %struct.ip_conntrack_stat*, %struct.nf_ct_event_notifier*, %struct.nf_exp_event_notifier*, %struct.nf_ip_net }
%struct.ct_pcpu = type { %struct.spinlock, %struct.hlist_nulls_head, %struct.hlist_nulls_head }
%struct.hlist_nulls_head = type { %struct.hlist_nulls_node* }
%struct.hlist_nulls_node = type { %struct.hlist_nulls_node*, %struct.hlist_nulls_node** }
%struct.ip_conntrack_stat = type { i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32 }
%struct.nf_ct_event_notifier = type opaque
%struct.nf_exp_event_notifier = type opaque
%struct.nf_ip_net = type { %struct.atomic_t, %struct.nf_tcp_net, %struct.kernel_cap_struct, %struct.atomic_t, %struct.atomic_t }
%struct.nf_tcp_net = type { [14 x i32], i32, i32, i32 }
%struct.kernel_cap_struct = type { [2 x i32] }
%struct.netns_nf_frag = type { %struct.fqdir* }
%struct.net_generic = type opaque
%struct.bpf_prog = type { i16, i16, i32, i32, i32, i32, [8 x i8], %struct.bpf_prog_aux*, %struct.sock_fprog_kern*, i32 (i8*, %struct.bpf_insn*)*, %union.anon.146 }
%struct.bpf_prog_aux = type { %struct.atomic_t, i32, i32, i32, i32, i32, i32, i32, i32, i8, i8, %struct.bpf_prog**, i8*, %struct.latch_tree_node, %struct.list_head, %struct.bpf_prog_ops*, %struct.bpf_map**, %struct.bpf_prog*, %struct.user_struct*, i64, [2 x %struct.bpf_map*], [16 x i8], i8*, %struct.bpf_prog_offload*, %struct.btf*, %struct.util_est*, %struct.ethtool_pauseparam*, i8**, i32, i32, i32, %struct.bpf_prog_stats*, %union.anon.145 }
%struct.latch_tree_node = type { [2 x %struct.rb_node] }
%struct.bpf_prog_ops = type { i32 (%struct.bpf_prog*, %union.bpf_attr*, %union.bpf_attr*)* }
%struct.user_struct = type { %union.anon.17, %struct.atomic_t, %struct.atomic_t, %union.anon.13, i64, i64, i64, %union.anon.13, %struct.hlist_node, %struct.atomic_t, %union.anon.13, %struct.ratelimit_state }
%struct.ratelimit_state = type { %struct.raw_spinlock, i32, i32, i32, i32, i64, i64 }
%struct.bpf_prog_offload = type { %struct.bpf_prog*, %struct.net_device*, %struct.bpf_offload_dev*, i8*, %struct.list_head, i8, i8, i8*, i32 }
%struct.bpf_offload_dev = type opaque
%struct.bpf_prog_stats = type { i64, i64, %struct.u64_stats_sync }
%union.anon.145 = type { %struct.work_struct }
%struct.sock_fprog_kern = type { i16, %struct.sock_filter* }
%struct.sock_filter = type { i16, i8, i8, i32 }
%struct.bpf_insn = type { i8, i8, i16, i32 }
%union.anon.146 = type { [0 x %struct.sock_filter] }
%struct.netns_xfrm = type { %struct.list_head, %struct.hlist_head*, %struct.hlist_head*, %struct.hlist_head*, i32, i32, %struct.work_struct, %struct.list_head, %struct.hlist_head*, i32, [3 x %struct.hlist_head], [3 x %struct.xfrm_policy_hash], [6 x i32], %struct.work_struct, %struct.xfrm_policy_hthresh, %struct.list_head, %struct.sock*, %struct.sock*, i32, i32, i32, i32, %struct.ctl_table_header*, [40 x i8], %struct.dst_ops, %struct.dst_ops, %struct.spinlock, %struct.spinlock, %struct.mutex, [24 x i8] }
%struct.xfrm_policy_hash = type { %struct.hlist_head*, i32, i8, i8, i8, i8 }
%struct.xfrm_policy_hthresh = type { %struct.work_struct, %struct.seqlock_t, i8, i8, i8, i8 }
%struct.sock = type opaque
%struct.cgroup_namespace = type { %union.anon.17, %struct.ns_common, %struct.user_namespace*, %struct.ucounts*, %struct.css_set* }
%struct.signal_struct = type { %union.anon.17, %struct.atomic_t, i32, %struct.list_head, %struct.wait_queue_head, %struct.task_struct*, %struct.sigpending, %struct.hlist_head, i32, i32, %struct.task_struct*, i32, i32, i8, i32, %struct.list_head, %struct.hrtimer, i64, [2 x %struct.tnum], %struct.thread_group_cputimer, %struct.posix_cputimers, [4 x %struct.pid*], %struct.pid*, i32, %struct.tty_struct*, %struct.seqlock_t, i64, i64, i64, i64, i64, i64, %struct.prev_cputime, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, %struct.task_io_accounting, i64, [16 x %struct.tnum], %struct.pacct_struct, %struct.taskstats*, i32, %struct.tty_audit_buf*, i8, i16, i16, %struct.mm_struct*, %struct.mutex }
%struct.thread_group_cputimer = type { %struct.task_cputime_atomic }
%struct.task_cputime_atomic = type { %union.anon.13, %union.anon.13, %union.anon.13 }
%struct.tty_struct = type opaque
%struct.pacct_struct = type { i32, i64, i64, i64, i64, i64, i64 }
%struct.taskstats = type { i16, i32, i8, i8, i64, i64, i64, i64, i64, i64, i64, i64, [32 x i8], i8, [3 x i8], [4 x i8], i32, i32, i32, i32, i32, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.tty_audit_buf = type opaque
%struct.sighand_struct = type { %struct.spinlock, %union.anon.17, %struct.wait_queue_head, [64 x %struct.k_sigaction] }
%struct.k_sigaction = type { %struct.sigaction }
%struct.sigaction = type { void (i32)*, i64, void ()*, %struct.cpumask }
%struct.sigpending = type { %struct.list_head, %struct.cpumask }
%struct.audit_context = type opaque
%struct.seccomp = type { i32, %struct.seccomp_filter* }
%struct.seccomp_filter = type opaque
%struct.raw_spinlock = type { %struct.qspinlock }
%struct.wake_q_node = type { %struct.wake_q_node* }
%struct.rb_root_cached = type { %struct.rb_root, %struct.rb_node* }
%struct.rt_mutex_waiter = type opaque
%struct.bio_list = type opaque
%struct.blk_plug = type opaque
%struct.reclaim_state = type opaque
%struct.io_context = type { %union.anon.13, %struct.atomic_t, %struct.atomic_t, %struct.spinlock, i16, i32, i64, %struct.xarray, %struct.io_cq*, %struct.hlist_head, %struct.work_struct }
%struct.io_cq = type { %struct.request_queue*, %struct.io_context*, %struct.sysv_shm, %union.anon.75, i32 }
%struct.request_queue = type opaque
%struct.capture_control = type opaque
%struct.kernel_siginfo = type { %struct.anon.76 }
%struct.anon.76 = type { i32, i32, i32, %union.__sifields }
%union.__sifields = type { %struct.anon.80 }
%struct.anon.80 = type { i32, i32, i32, i64, i64 }
%struct.task_io_accounting = type { i64, i64, i64, i64, i64, i64, i64 }
%struct.cpumask = type { [1 x i64] }
%struct.css_set = type { [4 x %struct.cgroup_subsys_state*], %union.anon.17, %struct.css_set*, %struct.cgroup*, i32, %struct.list_head, %struct.list_head, %struct.list_head, %struct.list_head, [4 x %struct.list_head], %struct.list_head, %struct.list_head, %struct.hlist_node, %struct.list_head, %struct.list_head, %struct.list_head, %struct.cgroup*, %struct.cgroup*, %struct.css_set*, i8, %struct.callback_head }
%struct.cgroup_subsys_state = type { %struct.cgroup*, %struct.cgroup_subsys*, %struct.percpu_ref, %struct.list_head, %struct.list_head, %struct.list_head, i32, i32, i64, %struct.atomic_t, %struct.work_struct, %struct.rcu_work, %struct.cgroup_subsys_state* }
%struct.cgroup_subsys = type { %struct.cgroup_subsys_state* (%struct.cgroup_subsys_state*)*, i32 (%struct.cgroup_subsys_state*)*, void (%struct.cgroup_subsys_state*)*, void (%struct.cgroup_subsys_state*)*, void (%struct.cgroup_subsys_state*)*, void (%struct.cgroup_subsys_state*)*, void (%struct.cgroup_subsys_state*, i32)*, i32 (%struct.seq_file*, %struct.cgroup_subsys_state*)*, i32 (%struct.cgroup_taskset*)*, void (%struct.cgroup_taskset*)*, void (%struct.cgroup_taskset*)*, void ()*, i32 (%struct.task_struct*)*, void (%struct.task_struct*)*, void (%struct.task_struct*)*, void (%struct.task_struct*)*, void (%struct.task_struct*)*, void (%struct.cgroup_subsys_state*)*, i8, i32, i8*, i8*, %struct.cgroup_root*, %struct.idr, %struct.list_head, %struct.cftype*, %struct.cftype*, i32 }
%struct.seq_file = type { i8*, i64, i64, i64, i64, i64, i64, i64, %struct.mutex, %struct.seq_operations*, i32, %struct.file*, i8* }
%struct.seq_operations = type { i8* (%struct.seq_file*, i64*)*, void (%struct.seq_file*, i8*)*, i8* (%struct.seq_file*, i8*, i64*)*, i32 (%struct.seq_file*, i8*)* }
%struct.cgroup_taskset = type opaque
%struct.cgroup_root = type { %struct.kernfs_root*, i32, i32, %struct.cgroup, i32, %struct.atomic_t, %struct.list_head, i32, %struct.idr, [4096 x i8], [64 x i8] }
%struct.kernfs_root = type { %struct.kernfs_node*, i32, %struct.idr, i32, %struct.kernfs_syscall_ops*, %struct.list_head, %struct.wait_queue_head }
%struct.kernfs_syscall_ops = type { i32 (%struct.seq_file*, %struct.kernfs_root*)*, i32 (%struct.kernfs_node*, i8*, i16)*, i32 (%struct.kernfs_node*)*, i32 (%struct.kernfs_node*, %struct.kernfs_node*, i8*)*, i32 (%struct.seq_file*, %struct.kernfs_node*, %struct.kernfs_root*)* }
%struct.cgroup = type { %struct.cgroup_subsys_state, i64, i32, i32, i32, i32, i32, i32, i32, i32, i32, i32, %struct.kernfs_node*, %struct.cgroup_file, %struct.cgroup_file, i16, i16, i16, i16, [4 x %struct.cgroup_subsys_state*], %struct.cgroup_root*, %struct.list_head, [4 x %struct.list_head], %struct.cgroup*, %struct.cgroup*, %struct.cgroup_rstat_cpu*, %struct.list_head, %struct.cgroup_base_stat, %struct.cgroup_base_stat, %struct.prev_cputime, %struct.list_head, %struct.mutex, %struct.wait_queue_head, %struct.work_struct, %struct.u64_stats_sync, %struct.u64_stats_sync, %struct.atomic_t, %struct.cgroup_freezer_state, [0 x i32] }
%struct.cgroup_file = type { %struct.kernfs_node*, i64, %struct.timer_list }
%struct.cgroup_rstat_cpu = type { %struct.u64_stats_sync, %struct.cgroup_base_stat, %struct.cgroup_base_stat, %struct.cgroup*, %struct.cgroup* }
%struct.cgroup_base_stat = type { %struct.task_cputime }
%struct.task_cputime = type { i64, i64, i64 }
%struct.cgroup_freezer_state = type { i8, i32, i32, i32 }
%struct.cftype = type { [64 x i8], i64, i64, i32, i32, %struct.cgroup_subsys*, %struct.list_head, %struct.kernfs_ops*, i32 (%struct.kernfs_open_file*)*, void (%struct.kernfs_open_file*)*, i64 (%struct.cgroup_subsys_state*, %struct.cftype*)*, i64 (%struct.cgroup_subsys_state*, %struct.cftype*)*, i32 (%struct.seq_file*, i8*)*, i8* (%struct.seq_file*, i64*)*, i8* (%struct.seq_file*, i8*, i64*)*, void (%struct.seq_file*, i8*)*, i32 (%struct.cgroup_subsys_state*, %struct.cftype*, i64)*, i32 (%struct.cgroup_subsys_state*, %struct.cftype*, i64)*, i64 (%struct.kernfs_open_file*, i8*, i64, i64)*, i32 (%struct.kernfs_open_file*, %struct.poll_table_struct*)* }
%struct.kernfs_ops = type { i32 (%struct.kernfs_open_file*)*, void (%struct.kernfs_open_file*)*, i32 (%struct.seq_file*, i8*)*, i8* (%struct.seq_file*, i64*)*, i8* (%struct.seq_file*, i8*, i64*)*, void (%struct.seq_file*, i8*)*, i64 (%struct.kernfs_open_file*, i8*, i64, i64)*, i64, i8, i64 (%struct.kernfs_open_file*, i8*, i64, i64)*, i32 (%struct.kernfs_open_file*, %struct.poll_table_struct*)*, i32 (%struct.kernfs_open_file*, %struct.vm_area_struct*)* }
%struct.kernfs_open_file = type { %struct.kernfs_node*, %struct.file*, %struct.seq_file*, i8*, %struct.mutex, %struct.mutex, i32, %struct.list_head, i8*, i64, i8, %struct.vm_operations_struct* }
%struct.poll_table_struct = type opaque
%struct.percpu_ref = type { %union.anon.13, i64, void (%struct.percpu_ref*)*, void (%struct.percpu_ref*)*, i8, %struct.callback_head }
%struct.rcu_work = type { %struct.work_struct, %struct.callback_head, %struct.workqueue_struct* }
%struct.robust_list_head = type opaque
%struct.compat_robust_list_head = type { %struct.atomic_t, i32, i32 }
%struct.futex_pi_state = type opaque
%struct.perf_event_context = type { %struct.pmu*, %struct.raw_spinlock, %struct.mutex, %struct.list_head, %struct.perf_event_groups, %struct.perf_event_groups, %struct.list_head, %struct.list_head, %struct.list_head, i32, i32, i32, i32, i32, i32, i32, %union.anon.17, %struct.task_struct*, i64, i64, %struct.perf_event_context*, i64, i64, i32, i8*, %struct.callback_head }
%struct.pmu = type { %struct.list_head, %struct.module*, %struct.device*, %struct.attribute_group**, %struct.attribute_group**, i8*, i32, i32, i32*, %struct.perf_cpu_context*, %struct.atomic_t, i32, i32, i32, void (%struct.pmu*)*, void (%struct.pmu*)*, i32 (%struct.perf_event*)*, void (%struct.perf_event*, %struct.mm_struct*)*, void (%struct.perf_event*, %struct.mm_struct*)*, i32 (%struct.perf_event*, i32)*, void (%struct.perf_event*, i32)*, void (%struct.perf_event*, i32)*, void (%struct.perf_event*, i32)*, void (%struct.perf_event*)*, void (%struct.pmu*, i32)*, i32 (%struct.pmu*)*, void (%struct.pmu*)*, i32 (%struct.perf_event*)*, void (%struct.perf_event_context*, i1)*, i64, i8* (%struct.perf_event*, i8**, i32, i1)*, void (i8*)*, i32 (%struct.list_head*)*, void (%struct.perf_event*)*, i32 (%struct.perf_event*)*, i32 (%struct.perf_event*)*, i32 (%struct.perf_event*, i64)* }
%struct.perf_cpu_context = type { %struct.perf_event_context, %struct.perf_event_context*, i32, i32, %struct.raw_spinlock, %struct.hrtimer, i64, i32, %struct.list_head, i32, i32 }
%struct.perf_event = type { %struct.list_head, %struct.list_head, %struct.list_head, %struct.rb_node, i64, %struct.list_head, %struct.hlist_node, %struct.list_head, i32, i32, i32, %struct.perf_event*, %struct.pmu*, i8*, i32, i32, %struct.local64_t, %union.anon.13, i64, i64, i64, i64, %struct.perf_event_attr, i16, i16, i16, %struct.hw_perf_event, %struct.perf_event_context*, %union.anon.13, %union.anon.13, %union.anon.13, %struct.mutex, %struct.list_head, %struct.perf_event*, i32, i32, %struct.list_head, %struct.task_struct*, %struct.mutex, %struct.atomic_t, %struct.ring_buffer*, %struct.list_head, i64, i32, %struct.wait_queue_head, %struct.fasync_struct*, i32, i32, i32, %struct.irq_work, %struct.atomic_t, %struct.perf_addr_filters_head, %struct.tnum*, i64, %struct.perf_event*, void (%struct.perf_event*)*, %struct.callback_head, %struct.pid_namespace*, i64, i64 ()*, void (%struct.perf_event*, %struct.perf_sample_data*, %struct.pt_regs*)*, i8*, void (%struct.perf_event*, %struct.perf_sample_data*, %struct.pt_regs*)*, %struct.bpf_prog*, %struct.trace_event_call*, %struct.event_filter*, %struct.list_head }
%struct.local64_t = type { %struct.local_t }
%struct.perf_event_attr = type { i32, i32, i64, %union.anon.13, i64, i64, i64, %struct.atomic_t, i32, %union.anon.13, %union.anon.13, i64, i64, i32, i32, i64, i32, i16, i16 }
%struct.hw_perf_event = type { %union.anon.91, %struct.task_struct*, i8*, i64, i32, %struct.local64_t, i64, i64, %struct.local64_t, i64, i64, i64, i64 }
%union.anon.91 = type { %struct.anon.92 }
%struct.anon.92 = type { i64, i64, i64, i64, i32, i32, i32, i32, %struct.hw_perf_event_extra, %struct.hw_perf_event_extra }
%struct.hw_perf_event_extra = type { i64, i32, i32, i32 }
%struct.ring_buffer = type opaque
%struct.fasync_struct = type { %struct.rwlock_t, i32, i32, %struct.fasync_struct*, %struct.file*, %struct.callback_head }
%struct.irq_work = type { i64, %struct.llist_node, void (%struct.irq_work*)* }
%struct.perf_addr_filters_head = type { %struct.list_head, %struct.raw_spinlock, i32 }
%struct.perf_sample_data = type { i64, %struct.perf_raw_record*, %struct.perf_branch_stack*, i64, i64, i64, %union.anon.13, i64, i64, %struct.util_est, i64, i64, i64, %struct.util_est, %struct.perf_callchain_entry*, %struct.perf_regs, %struct.pt_regs, %struct.perf_regs, i64, i64, [48 x i8] }
%struct.perf_raw_record = type { %struct.perf_raw_frag, i32 }
%struct.perf_raw_frag = type <{ %union.anon.98, i64 (i8*, i8*, i64, i64)*, i8*, i32 }>
%union.anon.98 = type { %struct.perf_raw_frag* }
%struct.perf_branch_stack = type { i64, [0 x %struct.task_cputime] }
%struct.perf_callchain_entry = type { i64, [0 x i64] }
%struct.pt_regs = type { i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.perf_regs = type { i64, %struct.pt_regs* }
%struct.trace_event_call = type opaque
%struct.event_filter = type opaque
%struct.perf_event_groups = type { %struct.rb_root, i64 }
%struct.rseq = type { i32, i32, %union.anon.13, i32, [12 x i8] }
%struct.tlbflush_unmap_batch = type { %struct.arch_tlbflush_unmap_batch, i8, i8 }
%struct.arch_tlbflush_unmap_batch = type { %struct.cpumask }
%struct.pipe_inode_info = type { %struct.mutex, %struct.wait_queue_head, i32, i32, i32, i32, i32, i32, i32, i32, i32, %struct.page*, %struct.fasync_struct*, %struct.fasync_struct*, %struct.pipe_buffer*, %struct.user_struct* }
%struct.pipe_buffer = type { %struct.page*, i32, i32, %struct.pipe_buf_operations*, i32, i64 }
%struct.pipe_buf_operations = type { i32 (%struct.pipe_inode_info*, %struct.pipe_buffer*)*, void (%struct.pipe_inode_info*, %struct.pipe_buffer*)*, i32 (%struct.pipe_inode_info*, %struct.pipe_buffer*)*, i1 (%struct.pipe_inode_info*, %struct.pipe_buffer*)* }
%struct.page_frag = type { %struct.page*, i32, i32 }
%struct.task_delay_info = type opaque
%struct.uprobe_task = type { i32, %union.anon.104, %struct.uprobe*, i64, %struct.return_instance*, i32 }
%union.anon.104 = type { %struct.anon.105 }
%struct.anon.105 = type { %struct.arch_uprobe_task, i64 }
%struct.arch_uprobe_task = type { i64, i32, i32 }
%struct.uprobe = type opaque
%struct.return_instance = type { %struct.uprobe*, i64, i64, i64, i8, %struct.return_instance* }
%struct.vm_struct = type { %struct.vm_struct*, i8*, i64, i64, %struct.page**, i32, i64, i8* }
%union.anon.17 = type { %struct.atomic_t }
%struct.thread_struct = type { [3 x %struct.rps_dev_flow], i64, i16, i16, i16, i16, i64, i64, [4 x %struct.perf_event*], i64, i64, i64, i64, i64, i64*, i64, i32, %union.anon.13, i8, [31 x i8], %struct.fpu }
%struct.fpu = type { i32, i64, [48 x i8], %union.fpregs_state }
%union.fpregs_state = type { %struct.xregs_state, [3520 x i8] }
%struct.xregs_state = type { %struct.fxregs_state, %struct.xstate_header, [0 x i8] }
%struct.fxregs_state = type { i16, i16, i16, i16, %union.anon.107, i32, i32, [32 x i32], [64 x i32], [12 x i32], %union.anon.110 }
%union.anon.107 = type { %struct.tnum }
%union.anon.110 = type { [12 x i32] }
%struct.xstate_header = type { i64, i64, [6 x i64] }
%struct.completion = type { i32, %struct.wait_queue_head }
%struct.kioctx_table = type opaque
%struct.mmu_notifier_mm = type opaque
%struct.uprobes_state = type { %struct.xol_area* }
%struct.xol_area = type opaque
%struct.timerqueue_node = type { %struct.rb_node, i64 }
%struct.anon_vma = type opaque
%struct.vm_operations_struct = type { void (%struct.vm_area_struct*)*, void (%struct.vm_area_struct*)*, i32 (%struct.vm_area_struct*, i64)*, i32 (%struct.vm_area_struct*)*, i32 (%struct.vm_fault*)*, i32 (%struct.vm_fault*, i32)*, void (%struct.vm_fault*, i64, i64)*, i64 (%struct.vm_area_struct*)*, i32 (%struct.vm_fault*)*, i32 (%struct.vm_fault*)*, i32 (%struct.vm_area_struct*, i64, i8*, i32, i32)*, i8* (%struct.vm_area_struct*)*, i32 (%struct.vm_area_struct*, %struct.mempolicy*)*, %struct.mempolicy* (%struct.vm_area_struct*, i64)*, %struct.page* (%struct.vm_area_struct*, i64)* }
%struct.vm_fault = type { %struct.vm_area_struct*, i32, i32, i64, i64, %union.anon.13*, %union.anon.13*, %union.anon.13, %struct.page*, %struct.mem_cgroup*, %struct.page*, %union.anon.13*, %struct.spinlock*, %struct.page* }
%struct.mem_cgroup = type opaque
%struct.mempolicy = type opaque
%struct.kernfs_node = type { %struct.atomic_t, %struct.atomic_t, %struct.kernfs_node*, i8*, %struct.rb_node, i8*, i32, %union.anon.55, i8*, %union.anon.13, i16, i16, %struct.kernfs_iattrs* }
%union.anon.55 = type { %struct.kernfs_elem_attr }
%struct.kernfs_elem_attr = type { %struct.kernfs_ops*, %struct.kernfs_open_node*, i64, %struct.kernfs_node* }
%struct.kernfs_open_node = type opaque
%struct.kernfs_iattrs = type opaque
%struct.qspinlock = type { %union.anon.17 }
%struct.module_param_attrs = type opaque
%struct.module_attribute = type { %struct.attribute, i64 (%struct.module_attribute*, %struct.module_kobject*, i8*)*, i64 (%struct.module_attribute*, %struct.module_kobject*, i8*, i64)*, void (%struct.module*, i8*)*, i32 (%struct.module*)*, void (%struct.module*)* }
%struct.kernel_param = type { i8*, %struct.module*, %struct.kernel_param_ops*, i16, i8, i8, %union.anon.142 }
%struct.kernel_param_ops = type { i32, i32 (i8*, %struct.kernel_param*)*, i32 (i8*, %struct.kernel_param*)*, void (i8*)* }
%struct.uid_gid_extent = type { i32, i32, i32 }
%struct.module_layout = type { i8*, i32, i32, i32, i32, %struct.mod_tree_node }
%struct.mod_tree_node = type { %struct.module*, %struct.latch_tree_node }
%struct.mod_arch_specific = type { i32, i32*, %struct.orc_entry* }
%struct.orc_entry = type { i16, i16, i16 }
%struct.bug_entry = type { i32, i32, i16, i16 }
%struct.mod_kallsyms = type { %struct.elf64_sym*, i32, i8*, i8* }
%struct.elf64_sym = type { i32, i8, i8, i16, i64, i64 }
%struct.module_sect_attrs = type opaque
%struct.module_notes_attrs = type opaque
%struct.srcu_struct = type { [5 x %struct.srcu_node], [3 x %struct.srcu_node*], %struct.mutex, %struct.spinlock, %struct.mutex, i32, i64, i64, i64, i64, %struct.srcu_data*, i64, %struct.mutex, %struct.completion, %struct.atomic_t, %struct.delayed_work }
%struct.srcu_node = type { %struct.spinlock, [4 x i64], [4 x i64], i64, %struct.srcu_node*, i32, i32 }
%struct.srcu_data = type { [2 x i64], [2 x i64], [32 x i8], %struct.spinlock, %struct.rcu_segcblist, i64, i64, i8, %struct.timer_list, %struct.work_struct, %struct.callback_head, %struct.srcu_node*, i64, i32, %struct.srcu_struct*, [8 x i8] }
%struct.rcu_segcblist = type { %struct.callback_head*, [4 x %struct.callback_head**], [4 x i64], i64, i64, i8, i8 }
%struct.delayed_work = type { %struct.work_struct, %struct.timer_list, %struct.workqueue_struct*, i32 }
%struct.bpf_raw_event_map = type { %struct.tracepoint*, i8*, i32, i32, [8 x i8] }
%struct.tracepoint = type { i8*, %struct.static_key, i32 ()*, void ()*, %struct.tracepoint_func* }
%struct.static_key = type { %struct.atomic_t, %union.anon.13 }
%struct.tracepoint_func = type { i8*, i8*, i32 }
%struct.jump_entry = type { i32, i32, i64 }
%struct.trace_eval_map = type opaque
%struct.u64_stats_sync = type {}
%struct.super_operations = type { %struct.inode* (%struct.super_block*)*, void (%struct.inode*)*, void (%struct.inode*)*, void (%struct.inode*, i32)*, i32 (%struct.inode*, %struct.writeback_control*)*, i32 (%struct.inode*)*, void (%struct.inode*)*, void (%struct.super_block*)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*)*, i32 (%struct.super_block*)*, i32 (%struct.super_block*)*, i32 (%struct.super_block*)*, i32 (%struct.dentry*, %struct.kstatfs*)*, i32 (%struct.super_block*, i32*, i8*)*, void (%struct.super_block*)*, i32 (%struct.seq_file*, %struct.dentry*)*, i32 (%struct.seq_file*, %struct.dentry*)*, i32 (%struct.seq_file*, %struct.dentry*)*, i32 (%struct.seq_file*, %struct.dentry*)*, i64 (%struct.super_block*, i32, i8*, i64, i64)*, i64 (%struct.super_block*, i32, i8*, i64, i64)*, %struct.dquot** (%struct.inode*)*, i32 (%struct.super_block*, %struct.page*, i32)*, i64 (%struct.super_block*, %struct.shrink_control*)*, i64 (%struct.super_block*, %struct.shrink_control*)* }
%struct.writeback_control = type opaque
%struct.kstatfs = type opaque
%struct.dquot = type { %struct.hlist_node, %struct.list_head, %struct.list_head, %struct.list_head, %struct.mutex, %struct.spinlock, %struct.atomic_t, %struct.super_block*, %struct.kqid, i64, i64, %struct.mem_dqblk }
%struct.kqid = type { %union.anon.17, i32 }
%struct.mem_dqblk = type { i64, i64, i64, i64, i64, i64, i64, i64, i64 }
%struct.shrink_control = type { i32, i32, i64, i64, %struct.mem_cgroup* }
%struct.dquot_operations = type { i32 (%struct.dquot*)*, %struct.dquot* (%struct.super_block*, i32)*, void (%struct.dquot*)*, i32 (%struct.dquot*)*, i32 (%struct.dquot*)*, i32 (%struct.dquot*)*, i32 (%struct.super_block*, i32)*, i64* (%struct.inode*)*, i32 (%struct.inode*, %struct.atomic_t*)*, i32 (%struct.inode*, i64*)*, i32 (%struct.super_block*, %struct.kqid*)* }
%struct.quotactl_ops = type { i32 (%struct.super_block*, i32, i32, %struct.path*)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32, %struct.qc_info*)*, i32 (%struct.super_block*, i64, %struct.qc_dqblk*)*, i32 (%struct.super_block*, %struct.kqid*, %struct.qc_dqblk*)*, i32 (%struct.super_block*, i64, %struct.qc_dqblk*)*, i32 (%struct.super_block*, %struct.qc_state*)*, i32 (%struct.super_block*, i32)* }
%struct.qc_info = type { i32, i32, i32, i32, i32, i32, i32, i32 }
%struct.qc_dqblk = type { i32, i64, i64, i64, i64, i64, i64, i64, i64, i32, i32, i64, i64, i64, i64, i32 }
%struct.qc_state = type { i32, [3 x %struct.qc_type_state] }
%struct.qc_type_state = type { i32, i32, i32, i32, i32, i32, i32, i64, i64, i64 }
%struct.export_operations = type opaque
%struct.rw_semaphore = type { %union.anon.13, %union.anon.13, %union.anon.17, %struct.raw_spinlock, %struct.list_head }
%struct.xattr_handler = type opaque
%struct.hlist_bl_head = type { %struct.hlist_bl_node* }
%struct.block_device = type { i32, i32, %struct.inode*, %struct.super_block*, %struct.mutex, i8*, i8*, i32, i8, %struct.list_head, %struct.block_device*, i32, i8, %struct.hd_struct*, i32, i32, %struct.gendisk*, %struct.request_queue*, %struct.backing_dev_info*, %struct.list_head, i64, i32, %struct.mutex }
%struct.hd_struct = type opaque
%struct.gendisk = type opaque
%struct.backing_dev_info = type opaque
%struct.mtd_info = type opaque
%struct.hlist_node = type { %struct.hlist_node*, %struct.hlist_node** }
%struct.quota_info = type { i32, %struct.rw_semaphore, [3 x %struct.inode*], [3 x %struct.mem_dqinfo], [3 x %struct.quota_format_ops*] }
%struct.mem_dqinfo = type { %struct.quota_format_type*, i32, %struct.list_head, i64, i32, i32, i64, i64, i8* }
%struct.quota_format_type = type { i32, %struct.quota_format_ops*, %struct.module*, %struct.quota_format_type* }
%struct.quota_format_ops = type { i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32)*, i32 (%struct.super_block*, i32)*, i32 (%struct.dquot*)*, i32 (%struct.dquot*)*, i32 (%struct.dquot*)*, i32 (%struct.super_block*, %struct.kqid*)* }
%struct.sb_writers = type { i32, %struct.wait_queue_head, [3 x %struct.percpu_rw_semaphore] }
%struct.percpu_rw_semaphore = type { %struct.rcu_sync, i32*, %struct.rw_semaphore, %struct.rcuwait, i32 }
%struct.rcu_sync = type { i32, i32, %struct.wait_queue_head, %struct.callback_head }
%struct.rcuwait = type { %struct.task_struct* }
%struct.fsnotify_mark_connector = type opaque
%union.anon.127 = type { [16 x i8] }
%struct.shrinker = type { i64 (%struct.shrinker*, %struct.shrink_control*)*, i64 (%struct.shrinker*, %struct.shrink_control*)*, i64, i32, i32, %struct.list_head, %union.anon.13* }
%struct.workqueue_struct = type opaque
%struct.hlist_head = type { %struct.hlist_node* }
%struct.user_namespace = type { %struct.uid_gid_map, %struct.uid_gid_map, %struct.uid_gid_map, %struct.atomic_t, %struct.user_namespace*, i32, %struct.atomic_t, %struct.atomic_t, %struct.ns_common, i64, %struct.list_head, %struct.key*, %struct.rw_semaphore, %struct.work_struct, %struct.ctl_table_set, %struct.ctl_table_header*, %struct.ucounts*, [9 x i32] }
%struct.uid_gid_map = type { i32, %union.anon.25 }
%union.anon.25 = type { %struct.anon.26, [48 x i8] }
%struct.anon.26 = type { %struct.uid_gid_extent*, %struct.uid_gid_extent* }
%struct.list_lru = type { %struct.list_lru_node* }
%struct.list_lru_node = type { %struct.spinlock, %struct.list_lru_one, i64, [24 x i8] }
%struct.list_lru_one = type { %struct.list_head, i64 }
%struct.sysv_shm = type { %struct.list_head }
%union.anon.75 = type { %struct.hlist_node }
%struct.inode = type { i16, i16, %struct.atomic_t, %struct.atomic_t, i32, %struct.posix_acl*, %struct.posix_acl*, %struct.inode_operations*, %struct.super_block*, %struct.address_space*, i8*, i64, %struct.atomic_t, i32, i64, %struct.tnum, %struct.tnum, %struct.tnum, %struct.spinlock, i16, i8, i8, i64, i64, %struct.rw_semaphore, i64, i64, %struct.hlist_node, %struct.list_head, %struct.list_head, %struct.list_head, %struct.list_head, %union.anon.12, %union.anon.13, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %union.anon.117, %struct.file_lock_context*, %struct.address_space, %struct.list_head, %union.anon.120, i32, i32, %struct.fsnotify_mark_connector*, i8* }
%struct.posix_acl = type opaque
%struct.inode_operations = type { %struct.dentry* (%struct.inode*, %struct.dentry*, i32)*, i8* (%struct.dentry*, %struct.inode*, %struct.delayed_call*)*, i32 (%struct.inode*, i32)*, %struct.posix_acl* (%struct.inode*, i32)*, i32 (%struct.dentry*, i8*, i32)*, i32 (%struct.inode*, %struct.dentry*, i16, i1)*, i32 (%struct.dentry*, %struct.inode*, %struct.dentry*)*, i32 (%struct.inode*, %struct.dentry*)*, i32 (%struct.inode*, %struct.dentry*, i8*)*, i32 (%struct.inode*, %struct.dentry*, i16)*, i32 (%struct.inode*, %struct.dentry*)*, i32 (%struct.inode*, %struct.dentry*, i16, i32)*, i32 (%struct.inode*, %struct.dentry*, %struct.inode*, %struct.dentry*, i32)*, i32 (%struct.dentry*, %struct.iattr*)*, i32 (%struct.path*, %struct.kstat*, i32, i32)*, i64 (%struct.dentry*, i8*, i64)*, i32 (%struct.inode*, %struct.fiemap_extent_info*, i64, i64)*, i32 (%struct.inode*, %struct.tnum*, i32)*, i32 (%struct.inode*, %struct.dentry*, %struct.file*, i32, i16)*, i32 (%struct.inode*, %struct.dentry*, i16)*, i32 (%struct.inode*, %struct.posix_acl*, i32)*, [24 x i8] }
%struct.delayed_call = type { void (i8*)*, i8* }
%struct.iattr = type { i32, i16, %struct.atomic_t, %struct.atomic_t, i64, %struct.tnum, %struct.tnum, %struct.tnum, %struct.file* }
%struct.kstat = type { i32, i16, i32, i32, i64, i64, i64, i32, i32, %struct.atomic_t, %struct.atomic_t, i64, %struct.tnum, %struct.tnum, %struct.tnum, %struct.tnum, i64 }
%struct.fiemap_extent_info = type { i32, i32, i32, %struct.fiemap_extent* }
%struct.fiemap_extent = type { i64, i64, i64, [2 x i64], i32, [3 x i32] }
%union.anon.117 = type { %struct.file_operations* }
%struct.file_lock_context = type { %struct.spinlock, %struct.list_head, %struct.list_head, %struct.list_head }
%struct.address_space = type { %struct.inode*, %struct.xarray, i32, %struct.atomic_t, %struct.rb_root_cached, %struct.rw_semaphore, i64, i64, i64, %struct.address_space_operations*, i64, i32, %struct.spinlock, %struct.list_head, i8* }
%struct.address_space_operations = type { i32 (%struct.page*, %struct.writeback_control*)*, i32 (%struct.file*, %struct.page*)*, i32 (%struct.address_space*, %struct.writeback_control*)*, i32 (%struct.page*)*, i32 (%struct.file*, %struct.address_space*, %struct.list_head*, i32)*, i32 (%struct.file*, %struct.address_space*, i64, i32, i32, %struct.page**, i8**)*, i32 (%struct.file*, %struct.address_space*, i64, i32, i32, %struct.page*, i8*)*, i64 (%struct.address_space*, i64)*, void (%struct.page*, i32, i32)*, i32 (%struct.page*, i32)*, void (%struct.page*)*, i64 (%struct.kiocb*, %struct.iov_iter*)*, i32 (%struct.address_space*, %struct.page*, %struct.page*, i32)*, i1 (%struct.page*, i32)*, void (%struct.page*)*, i32 (%struct.page*)*, i32 (%struct.page*, i64, i64)*, void (%struct.page*, i8*, i8*)*, i32 (%struct.address_space*, %struct.page*)*, i32 (%struct.swap_info_struct*, %struct.file*, i64*)*, void (%struct.file*)* }
%struct.kiocb = type { %struct.file*, i64, void (%struct.kiocb*, i64, i64)*, i8*, i32, i16, i16, i32 }
%struct.iov_iter = type { i32, i64, i64, %union.anon.59, %union.anon.13 }
%union.anon.59 = type { %struct.iovec* }
%struct.iovec = type { i8*, i64 }
%struct.swap_info_struct = type opaque
%union.anon.120 = type { %struct.pipe_inode_info* }
%struct.file_operations = type { %struct.module*, i64 (%struct.file*, i64, i32)*, i64 (%struct.file*, i8*, i64, i64*)*, i64 (%struct.file*, i8*, i64, i64*)*, i64 (%struct.kiocb*, %struct.iov_iter*)*, i64 (%struct.kiocb*, %struct.iov_iter*)*, i32 (%struct.kiocb*, i1)*, i32 (%struct.file*, %struct.dir_context*)*, i32 (%struct.file*, %struct.dir_context*)*, i32 (%struct.file*, %struct.poll_table_struct*)*, i64 (%struct.file*, i32, i64)*, i64 (%struct.file*, i32, i64)*, i32 (%struct.file*, %struct.vm_area_struct*)*, i64, i32 (%struct.inode*, %struct.file*)*, i32 (%struct.file*, i8*)*, i32 (%struct.inode*, %struct.file*)*, i32 (%struct.file*, i64, i64, i32)*, i32 (i32, %struct.file*, i32)*, i32 (%struct.file*, i32, %struct.file_lock*)*, i64 (%struct.file*, %struct.page*, i32, i64, i64*, i32)*, i64 (%struct.file*, i64, i64, i64, i64)*, i32 (i32)*, i32 (%struct.file*, i32, %struct.file_lock*)*, i64 (%struct.pipe_inode_info*, %struct.file*, i64*, i64, i32)*, i64 (%struct.file*, i64*, %struct.pipe_inode_info*, i64, i32)*, i32 (%struct.file*, i64, %struct.file_lock**, i8**)*, i64 (%struct.file*, i32, i64, i64)*, void (%struct.seq_file*, %struct.file*)*, i64 (%struct.file*, i64, %struct.file*, i64, i64, i32)*, i64 (%struct.file*, i64, %struct.file*, i64, i64, i32)*, i32 (%struct.file*, i64, i64, i32)* }
%struct.dir_context = type { i32 (%struct.dir_context*, i8*, i32, i64, i64, i32)*, i64 }
%struct.file_lock = type { %struct.file_lock*, %struct.list_head, %struct.hlist_node, %struct.list_head, %struct.list_head, i8*, i32, i8, i32, i32, %struct.wait_queue_head, %struct.file*, i64, i64, %struct.fasync_struct*, i64, i64, %struct.file_lock_operations*, %struct.lock_manager_operations*, %union.anon.118 }
%struct.file_lock_operations = type { void (%struct.file_lock*, %struct.file_lock*)*, void (%struct.file_lock*)* }
%struct.lock_manager_operations = type { i8* (i8*)*, void (i8*)*, void (%struct.file_lock*)*, i32 (%struct.file_lock*, i32)*, i1 (%struct.file_lock*)*, i32 (%struct.file_lock*, i32, %struct.list_head*)*, void (%struct.file_lock*, i8**)* }
%union.anon.118 = type { %struct.nfs_lock_info }
%struct.nfs_lock_info = type { i32, %struct.nlm_lockowner*, %struct.list_head }
%struct.nlm_lockowner = type opaque
%struct.spinlock = type { %union.anon.16 }
%union.anon.16 = type { %struct.raw_spinlock }
%union.anon.13 = type { i64 }
%struct.mutex = type { %union.anon.13, %struct.spinlock, %union.anon.17, %struct.list_head }
%struct.fown_struct = type { %struct.rwlock_t, %struct.pid*, i32, %struct.atomic_t, %struct.atomic_t, i32 }
%struct.cred = type { %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, %struct.atomic_t, i32, %struct.kernel_cap_struct, %struct.kernel_cap_struct, %struct.kernel_cap_struct, %struct.kernel_cap_struct, %struct.kernel_cap_struct, i8, %struct.key*, %struct.key*, %struct.key*, %struct.key*, i8*, %struct.user_struct*, %struct.user_namespace*, %struct.group_info*, %union.anon.12 }
%struct.group_info = type { %struct.atomic_t, i32, [0 x %struct.atomic_t] }
%struct.file_ra_state = type { i64, i32, i32, i32, i32, i64 }
%struct.list_head = type { %struct.list_head*, %struct.list_head* }
%struct.btf_type = type { i32, i32, %struct.atomic_t }
%struct.btf = type opaque
%struct.bpf_map_memory = type { i32, %struct.user_struct* }
%struct.atomic_t = type { i32 }
%struct.work_struct = type { %union.anon.13, %struct.list_head, void (%struct.work_struct*)* }
%struct.tnum = type { i64, i64 }

; Function Attrs: mustprogress nofree noinline norecurse noredzone nosync nounwind null_pointer_is_valid sspstrong willreturn
define dso_local void @check_cond_jmp_op_wrapper_BPF_JSLE(%struct.bpf_reg_state* nocapture noundef %dst_reg, %struct.bpf_reg_state* nocapture noundef %src_reg, %struct.bpf_reg_state* nocapture noundef %other_branch_dst_reg, %struct.bpf_reg_state* nocapture noundef %other_branch_src_reg) local_unnamed_addr #0 {
entry:
  %type = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 0
  store i32 1, i32* %type, align 8
  %type8 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 0
  store i32 1, i32* %type8, align 8
  %i.i = load i32, i32* %type, align 8
  %type1.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 0
  store i32 %i.i, i32* %type1.i, align 8
  %value.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 5, i32 0
  %i13.i = load i64, i64* %value.i, align 8
  %value3.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 5, i32 0
  store i64 %i13.i, i64* %value3.i, align 8
  %mask.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 5, i32 1
  %i14.i = load i64, i64* %mask.i, align 8
  %mask6.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 5, i32 1
  store i64 %i14.i, i64* %mask6.i, align 8
  %smin_value.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 6
  %i15.i = load i64, i64* %smin_value.i, align 8
  %smin_value7.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 6
  store i64 %i15.i, i64* %smin_value7.i, align 8
  %smax_value.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 7
  %i16.i = load i64, i64* %smax_value.i, align 8
  %smax_value8.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 7
  store i64 %i16.i, i64* %smax_value8.i, align 8
  %umin_value.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 8
  %i17.i = load i64, i64* %umin_value.i, align 8
  %umin_value9.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 8
  store i64 %i17.i, i64* %umin_value9.i, align 8
  %umax_value.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %dst_reg, i64 0, i32 9
  %i18.i = load i64, i64* %umax_value.i, align 8
  %umax_value10.i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_dst_reg, i64 0, i32 9
  store i64 %i18.i, i64* %umax_value10.i, align 8
  %i.i2 = load i32, i32* %type8, align 8
  %type1.i3 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 0
  store i32 %i.i2, i32* %type1.i3, align 8
  %value.i4 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 5, i32 0
  %i13.i5 = load i64, i64* %value.i4, align 8
  %value3.i6 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 5, i32 0
  store i64 %i13.i5, i64* %value3.i6, align 8
  %mask.i7 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 5, i32 1
  %i14.i8 = load i64, i64* %mask.i7, align 8
  %mask6.i9 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 5, i32 1
  store i64 %i14.i8, i64* %mask6.i9, align 8
  %smin_value.i10 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 6
  %i15.i11 = load i64, i64* %smin_value.i10, align 8
  %smin_value7.i12 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 6
  store i64 %i15.i11, i64* %smin_value7.i12, align 8
  %smax_value.i13 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 7
  %i16.i14 = load i64, i64* %smax_value.i13, align 8
  %smax_value8.i15 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 7
  store i64 %i16.i14, i64* %smax_value8.i15, align 8
  %umin_value.i16 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 8
  %i17.i17 = load i64, i64* %umin_value.i16, align 8
  %umin_value9.i18 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 8
  store i64 %i17.i17, i64* %umin_value9.i18, align 8
  %umax_value.i19 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %src_reg, i64 0, i32 9
  %i18.i20 = load i64, i64* %umax_value.i19, align 8
  %umax_value10.i21 = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state* %other_branch_src_reg, i64 0, i32 9
  store i64 %i18.i20, i64* %umax_value10.i21, align 8
  %i = load i32, i32* %type8, align 8
  %cmp21 = icmp eq i32 %i, 1
  br i1 %cmp21, label %land.lhs.true, label %if.then44

land.lhs.true:                                    ; preds = %entry
  %i57 = load i64, i64* %mask.i7, align 8
  %tobool.not.i = icmp eq i64 %i57, 0
  br i1 %tobool.not.i, label %if.then25, label %if.then44

if.then25:                                        ; preds = %land.lhs.true
  %i58 = load i64, i64* %value.i4, align 8
  %i89.i = load i64, i64* %smax_value.i, align 8
  %cmp134.not.i = icmp sgt i64 %i89.i, %i58
  br i1 %cmp134.not.i, label %if.else137.i, label %is_branch_taken.exit

if.else137.i:                                     ; preds = %if.then25
  %i90.i = load i64, i64* %smin_value.i, align 8
  %cmp139.i = icmp sle i64 %i90.i, %i58
  %spec.select = sext i1 %cmp139.i to i32
  br label %is_branch_taken.exit

is_branch_taken.exit:                             ; preds = %if.else137.i, %if.then25
  %retval.0.i = phi i32 [ 1, %if.then25 ], [ %spec.select, %if.else137.i ]
  %phi.cmp = icmp ult i32 %retval.0.i, 2
  br i1 %phi.cmp, label %if.end117, label %if.then44

if.then44:                                        ; preds = %is_branch_taken.exit, %land.lhs.true, %entry
  %i63 = load i32, i32* %type, align 8
  %cmp46 = icmp ne i32 %i63, 1
  %cmp21.not = xor i1 %cmp21, true
  %brmerge = select i1 %cmp46, i1 true, i1 %cmp21.not
  br i1 %brmerge, label %if.end117, label %if.then52

if.then52:                                        ; preds = %if.then44
  %i66 = load i64, i64* %mask.i7, align 8
  %tobool.not.i52 = icmp eq i64 %i66, 0
  br i1 %tobool.not.i52, label %cond.end, label %if.else70

cond.end:                                         ; preds = %if.then52
  %i67 = load i64, i64* %value.i4, align 8
  %cond168.i = add i64 %i67, 1
  %i135.i = load i64, i64* %smin_value.i, align 8
  %cmp185.i = icmp sgt i64 %i135.i, %cond168.i
  %cond190.i = select i1 %cmp185.i, i64 %i135.i, i64 %cond168.i
  store i64 %cond190.i, i64* %smin_value.i, align 8
  %i136.i = load i64, i64* %smax_value8.i, align 8
  %cmp194.i = icmp slt i64 %i136.i, %i67
  %cond199.i = select i1 %cmp194.i, i64 %i136.i, i64 %i67
  store i64 %cond199.i, i64* %smax_value8.i, align 8
  %i.i42.i = load i64, i64* %smin_value.i, align 8
  %cmp.i43.i = icmp sgt i64 %i.i42.i, -1
  br i1 %cmp.i43.i, label %if.then.i.i, label %lor.lhs.false.i.i

lor.lhs.false.i.i:                                ; preds = %cond.end
  %i33.i.i = load i64, i64* %smax_value.i, align 8
  %cmp1.i45.i = icmp slt i64 %i33.i.i, 0
  br i1 %cmp1.i45.i, label %if.then.i.i, label %if.end.i.i

if.then.i.i:                                      ; preds = %lor.lhs.false.i.i, %cond.end
  %i34.i.i = load i64, i64* %umin_value.i, align 8
  %cmp3.i.i = icmp ugt i64 %i.i42.i, %i34.i.i
  %cond.i.i = select i1 %cmp3.i.i, i64 %i.i42.i, i64 %i34.i.i
  store i64 %cond.i.i, i64* %umin_value.i, align 8
  store i64 %cond.i.i, i64* %smin_value.i, align 8
  %i35.i.i = load i64, i64* %smax_value.i, align 8
  %i36.i.i = load i64, i64* %umax_value.i, align 8
  %cmp8.i48.i = icmp ult i64 %i35.i.i, %i36.i.i
  %cond12.i.i = select i1 %cmp8.i48.i, i64 %i35.i.i, i64 %i36.i.i
  store i64 %cond12.i.i, i64* %umax_value.i, align 8
  br label %__reg_deduce_bounds.exit.i.sink.split

if.end.i.i:                                       ; preds = %lor.lhs.false.i.i
  %i37.i.i = load i64, i64* %umax_value.i, align 8
  %cmp16.i.i = icmp sgt i64 %i37.i.i, -1
  %i38.i.i = load i64, i64* %umin_value.i, align 8
  br i1 %cmp16.i.i, label %if.then17.i.i, label %if.else.i.i

if.then17.i.i:                                    ; preds = %if.end.i.i
  store i64 %i38.i.i, i64* %smin_value.i, align 8
  %cmp23.i.i = icmp ult i64 %i33.i.i, %i37.i.i
  %cond27.i.i = select i1 %cmp23.i.i, i64 %i33.i.i, i64 %i37.i.i
  store i64 %cond27.i.i, i64* %umax_value.i, align 8
  br label %__reg_deduce_bounds.exit.i.sink.split

if.else.i.i:                                      ; preds = %if.end.i.i
  %cmp31.i.i = icmp slt i64 %i38.i.i, 0
  br i1 %cmp31.i.i, label %if.then32.i.i, label %__reg_deduce_bounds.exit.i

if.then32.i.i:                                    ; preds = %if.else.i.i
  %cmp36.i.i = icmp ugt i64 %i.i42.i, %i38.i.i
  %cond40.i.i = select i1 %cmp36.i.i, i64 %i.i42.i, i64 %i38.i.i
  store i64 %cond40.i.i, i64* %umin_value.i, align 8
  store i64 %cond40.i.i, i64* %smin_value.i, align 8
  br label %__reg_deduce_bounds.exit.i.sink.split

__reg_deduce_bounds.exit.i.sink.split:            ; preds = %if.then32.i.i, %if.then17.i.i, %if.then.i.i
  %i37.i.i.sink = phi i64 [ %i37.i.i, %if.then32.i.i ], [ %cond27.i.i, %if.then17.i.i ], [ %cond12.i.i, %if.then.i.i ]
  store i64 %i37.i.i.sink, i64* %smax_value.i, align 8
  br label %__reg_deduce_bounds.exit.i

__reg_deduce_bounds.exit.i:                       ; preds = %__reg_deduce_bounds.exit.i.sink.split, %if.else.i.i
  %i.i50.i = load i64, i64* %smin_value7.i, align 8
  %cmp.i51.i = icmp sgt i64 %i.i50.i, -1
  br i1 %cmp.i51.i, label %if.then.i66.i, label %lor.lhs.false.i55.i

lor.lhs.false.i55.i:                              ; preds = %__reg_deduce_bounds.exit.i
  %i33.i53.i = load i64, i64* %smax_value8.i, align 8
  %cmp1.i54.i = icmp slt i64 %i33.i53.i, 0
  br i1 %cmp1.i54.i, label %if.then.i66.i, label %if.end.i72.i

if.then.i66.i:                                    ; preds = %lor.lhs.false.i55.i, %__reg_deduce_bounds.exit.i
  %i34.i57.i = load i64, i64* %umin_value9.i, align 8
  %cmp3.i58.i = icmp ugt i64 %i.i50.i, %i34.i57.i
  %cond.i59.i = select i1 %cmp3.i58.i, i64 %i.i50.i, i64 %i34.i57.i
  store i64 %cond.i59.i, i64* %umin_value9.i, align 8
  store i64 %cond.i59.i, i64* %smin_value7.i, align 8
  %i35.i61.i = load i64, i64* %smax_value8.i, align 8
  %i36.i63.i = load i64, i64* %umax_value10.i, align 8
  %cmp8.i64.i = icmp ult i64 %i35.i61.i, %i36.i63.i
  %cond12.i65.i = select i1 %cmp8.i64.i, i64 %i35.i61.i, i64 %i36.i63.i
  store i64 %cond12.i65.i, i64* %umax_value10.i, align 8
  br label %__reg_deduce_bounds.exit81.i.sink.split

if.end.i72.i:                                     ; preds = %lor.lhs.false.i55.i
  %i37.i68.i = load i64, i64* %umax_value10.i, align 8
  %cmp16.i69.i = icmp sgt i64 %i37.i68.i, -1
  %i38.i71.i = load i64, i64* %umin_value9.i, align 8
  br i1 %cmp16.i69.i, label %if.then17.i75.i, label %if.else.i77.i

if.then17.i75.i:                                  ; preds = %if.end.i72.i
  store i64 %i38.i71.i, i64* %smin_value7.i, align 8
  %cmp23.i73.i = icmp ult i64 %i33.i53.i, %i37.i68.i
  %cond27.i74.i = select i1 %cmp23.i73.i, i64 %i33.i53.i, i64 %i37.i68.i
  store i64 %cond27.i74.i, i64* %umax_value10.i, align 8
  br label %__reg_deduce_bounds.exit81.i.sink.split

if.else.i77.i:                                    ; preds = %if.end.i72.i
  %cmp31.i76.i = icmp slt i64 %i38.i71.i, 0
  br i1 %cmp31.i76.i, label %if.then32.i80.i, label %__reg_deduce_bounds.exit81.i

if.then32.i80.i:                                  ; preds = %if.else.i77.i
  %cmp36.i78.i = icmp ugt i64 %i.i50.i, %i38.i71.i
  %cond40.i79.i = select i1 %cmp36.i78.i, i64 %i.i50.i, i64 %i38.i71.i
  store i64 %cond40.i79.i, i64* %umin_value9.i, align 8
  store i64 %cond40.i79.i, i64* %smin_value7.i, align 8
  br label %__reg_deduce_bounds.exit81.i.sink.split

__reg_deduce_bounds.exit81.i.sink.split:          ; preds = %if.then32.i80.i, %if.then17.i75.i, %if.then.i66.i
  %i37.i68.i.sink = phi i64 [ %i37.i68.i, %if.then32.i80.i ], [ %cond27.i74.i, %if.then17.i75.i ], [ %cond12.i65.i, %if.then.i66.i ]
  store i64 %i37.i68.i.sink, i64* %smax_value8.i, align 8
  br label %__reg_deduce_bounds.exit81.i

__reg_deduce_bounds.exit81.i:                     ; preds = %__reg_deduce_bounds.exit81.i.sink.split, %if.else.i77.i
  %i.i83.i = load i64, i64* %umin_value.i, align 8
  %i5.i85.i = load i64, i64* %umax_value.i, align 8
  %xor.i.i.i = xor i64 %i5.i85.i, %i.i83.i
  %cmp.i.i.i.i = icmp eq i64 %xor.i.i.i, 0
  br i1 %cmp.i.i.i.i, label %__reg_bound_offset.exit.i, label %if.end.i.i.i.i

if.end.i.i.i.i:                                   ; preds = %__reg_deduce_bounds.exit81.i
  %tobool.not.i.i.i.i.i = icmp ult i64 %xor.i.i.i, 4294967296
  %shl.i.i.i.i.i = shl i64 %xor.i.i.i, 32
  %spec.select.i.i.i.i.i = select i1 %tobool.not.i.i.i.i.i, i64 %shl.i.i.i.i.i, i64 %xor.i.i.i
  %spec.select17.i.i.i.i.i = select i1 %tobool.not.i.i.i.i.i, i32 31, i32 63
  %tobool2.not.i.i.i.i.i = icmp ult i64 %spec.select.i.i.i.i.i, 281474976710656
  %sub4.i.i.i.i.i = add nsw i32 %spec.select17.i.i.i.i.i, -16
  %shl5.i.i.i.i.i = shl i64 %spec.select.i.i.i.i.i, 16
  %word.addr.1.i.i.i.i.i = select i1 %tobool2.not.i.i.i.i.i, i64 %shl5.i.i.i.i.i, i64 %spec.select.i.i.i.i.i
  %num.1.i.i.i.i.i = select i1 %tobool2.not.i.i.i.i.i, i32 %sub4.i.i.i.i.i, i32 %spec.select17.i.i.i.i.i
  %tobool8.not.i.i.i.i.i = icmp ult i64 %word.addr.1.i.i.i.i.i, 72057594037927936
  %sub10.i.i.i.i.i = add nsw i32 %num.1.i.i.i.i.i, -8
  %shl11.i.i.i.i.i = shl i64 %word.addr.1.i.i.i.i.i, 8
  %word.addr.2.i.i.i.i.i = select i1 %tobool8.not.i.i.i.i.i, i64 %shl11.i.i.i.i.i, i64 %word.addr.1.i.i.i.i.i
  %num.2.i.i.i.i.i = select i1 %tobool8.not.i.i.i.i.i, i32 %sub10.i.i.i.i.i, i32 %num.1.i.i.i.i.i
  %tobool14.not.i.i.i.i.i = icmp ult i64 %word.addr.2.i.i.i.i.i, 1152921504606846976
  %sub16.i.i.i.i.i = add nsw i32 %num.2.i.i.i.i.i, -4
  %shl17.i.i.i.i.i = shl i64 %word.addr.2.i.i.i.i.i, 4
  %word.addr.3.i.i.i.i.i = select i1 %tobool14.not.i.i.i.i.i, i64 %shl17.i.i.i.i.i, i64 %word.addr.2.i.i.i.i.i
  %num.3.i.i.i.i.i = select i1 %tobool14.not.i.i.i.i.i, i32 %sub16.i.i.i.i.i, i32 %num.2.i.i.i.i.i
  %tobool20.not.i.i.i.i.i = icmp ult i64 %word.addr.3.i.i.i.i.i, 4611686018427387904
  %sub22.i.i.i.i.i = add i32 %num.3.i.i.i.i.i, 254
  %shl23.i.i.i.i.i = shl i64 %word.addr.3.i.i.i.i.i, 2
  %word.addr.4.i.i.i.i.i = select i1 %tobool20.not.i.i.i.i.i, i64 %shl23.i.i.i.i.i, i64 %word.addr.3.i.i.i.i.i
  %num.4.i.i.i.i.i = select i1 %tobool20.not.i.i.i.i.i, i32 %sub22.i.i.i.i.i, i32 %num.3.i.i.i.i.i
  %word.addr.4.lobit.i.i.i.i.i.neg = lshr i64 %word.addr.4.i.i.i.i.i, 63
  %i.i.i.i.i.i.neg = trunc i64 %word.addr.4.lobit.i.i.i.i.i.neg to i32
  %add.i.i.i.i = add i32 %num.4.i.i.i.i.i, %i.i.i.i.i.i.neg
  %phi.bo14 = and i32 %add.i.i.i.i, 255
  br label %__reg_bound_offset.exit.i

__reg_bound_offset.exit.i:                        ; preds = %if.end.i.i.i.i, %__reg_deduce_bounds.exit81.i
  %retval.0.i.i.i.i = phi i32 [ %phi.bo14, %if.end.i.i.i.i ], [ 0, %__reg_deduce_bounds.exit81.i ]
  %cmp.i.i.i = icmp ugt i32 %retval.0.i.i.i.i, 63
  %sh_prom.i.i.i = zext i32 %retval.0.i.i.i.i to i64
  %notmask.i.i.i = shl nsw i64 -1, %sh_prom.i.i.i
  %sub.i.i.i = xor i64 %notmask.i.i.i, -1
  %and.i.i.i = and i64 %notmask.i.i.i, %i.i83.i
  %retval.sroa.0.0.i.i.i = select i1 %cmp.i.i.i, i64 0, i64 %and.i.i.i
  %retval.sroa.3.0.i.i.i = select i1 %cmp.i.i.i, i64 -1, i64 %sub.i.i.i
  %i9.i.i = load i64, i64* %value.i, align 8
  %i11.i.i = load i64, i64* %mask.i, align 8
  %or.i.i.i = or i64 %retval.sroa.0.0.i.i.i, %i9.i.i
  %and.i1.i.i = and i64 %retval.sroa.3.0.i.i.i, %i11.i.i
  %neg.i.i.i = xor i64 %and.i1.i.i, -1
  %and4.i.i.i = and i64 %or.i.i.i, %neg.i.i.i
  store i64 %and4.i.i.i, i64* %value.i, align 8
  store i64 %and.i1.i.i, i64* %mask.i, align 8
  %i.i90.i = load i64, i64* %umin_value9.i, align 8
  %i5.i92.i = load i64, i64* %umax_value10.i, align 8
  %xor.i.i93.i = xor i64 %i5.i92.i, %i.i90.i
  %cmp.i.i.i94.i = icmp eq i64 %xor.i.i93.i, 0
  br i1 %cmp.i.i.i94.i, label %reg_set_min_max.exit, label %if.end.i.i.i124.i

if.end.i.i.i124.i:                                ; preds = %__reg_bound_offset.exit.i
  %tobool.not.i.i.i.i95.i = icmp ult i64 %xor.i.i93.i, 4294967296
  %shl.i.i.i.i96.i = shl i64 %xor.i.i93.i, 32
  %spec.select.i.i.i.i97.i = select i1 %tobool.not.i.i.i.i95.i, i64 %shl.i.i.i.i96.i, i64 %xor.i.i93.i
  %spec.select17.i.i.i.i98.i = select i1 %tobool.not.i.i.i.i95.i, i32 31, i32 63
  %tobool2.not.i.i.i.i99.i = icmp ult i64 %spec.select.i.i.i.i97.i, 281474976710656
  %sub4.i.i.i.i100.i = add nsw i32 %spec.select17.i.i.i.i98.i, -16
  %shl5.i.i.i.i101.i = shl i64 %spec.select.i.i.i.i97.i, 16
  %word.addr.1.i.i.i.i102.i = select i1 %tobool2.not.i.i.i.i99.i, i64 %shl5.i.i.i.i101.i, i64 %spec.select.i.i.i.i97.i
  %num.1.i.i.i.i103.i = select i1 %tobool2.not.i.i.i.i99.i, i32 %sub4.i.i.i.i100.i, i32 %spec.select17.i.i.i.i98.i
  %tobool8.not.i.i.i.i104.i = icmp ult i64 %word.addr.1.i.i.i.i102.i, 72057594037927936
  %sub10.i.i.i.i105.i = add nsw i32 %num.1.i.i.i.i103.i, -8
  %shl11.i.i.i.i106.i = shl i64 %word.addr.1.i.i.i.i102.i, 8
  %word.addr.2.i.i.i.i107.i = select i1 %tobool8.not.i.i.i.i104.i, i64 %shl11.i.i.i.i106.i, i64 %word.addr.1.i.i.i.i102.i
  %num.2.i.i.i.i108.i = select i1 %tobool8.not.i.i.i.i104.i, i32 %sub10.i.i.i.i105.i, i32 %num.1.i.i.i.i103.i
  %tobool14.not.i.i.i.i109.i = icmp ult i64 %word.addr.2.i.i.i.i107.i, 1152921504606846976
  %sub16.i.i.i.i110.i = add nsw i32 %num.2.i.i.i.i108.i, -4
  %shl17.i.i.i.i111.i = shl i64 %word.addr.2.i.i.i.i107.i, 4
  %word.addr.3.i.i.i.i112.i = select i1 %tobool14.not.i.i.i.i109.i, i64 %shl17.i.i.i.i111.i, i64 %word.addr.2.i.i.i.i107.i
  %num.3.i.i.i.i113.i = select i1 %tobool14.not.i.i.i.i109.i, i32 %sub16.i.i.i.i110.i, i32 %num.2.i.i.i.i108.i
  %tobool20.not.i.i.i.i114.i = icmp ult i64 %word.addr.3.i.i.i.i112.i, 4611686018427387904
  %sub22.i.i.i.i115.i = add i32 %num.3.i.i.i.i113.i, 254
  %shl23.i.i.i.i116.i = shl i64 %word.addr.3.i.i.i.i112.i, 2
  %word.addr.4.i.i.i.i117.i = select i1 %tobool20.not.i.i.i.i114.i, i64 %shl23.i.i.i.i116.i, i64 %word.addr.3.i.i.i.i112.i
  %num.4.i.i.i.i118.i = select i1 %tobool20.not.i.i.i.i114.i, i32 %sub22.i.i.i.i115.i, i32 %num.3.i.i.i.i113.i
  %word.addr.4.lobit.i.i.i.i119.i.neg = lshr i64 %word.addr.4.i.i.i.i117.i, 63
  %i.i.i.i.i120.i.neg = trunc i64 %word.addr.4.lobit.i.i.i.i119.i.neg to i32
  %add.i.i.i123.i = add i32 %num.4.i.i.i.i118.i, %i.i.i.i.i120.i.neg
  %phi.bo15 = and i32 %add.i.i.i123.i, 255
  br label %reg_set_min_max.exit

reg_set_min_max.exit:                             ; preds = %if.end.i.i.i124.i, %__reg_bound_offset.exit.i
  %retval.0.i.i.i125.i = phi i32 [ %phi.bo15, %if.end.i.i.i124.i ], [ 0, %__reg_bound_offset.exit.i ]
  %cmp.i.i127.i = icmp ugt i32 %retval.0.i.i.i125.i, 63
  %sh_prom.i.i128.i = zext i32 %retval.0.i.i.i125.i to i64
  %notmask.i.i129.i = shl nsw i64 -1, %sh_prom.i.i128.i
  %sub.i.i130.i = xor i64 %notmask.i.i129.i, -1
  %and.i.i131.i = and i64 %notmask.i.i129.i, %i.i90.i
  %retval.sroa.0.0.i.i132.i = select i1 %cmp.i.i127.i, i64 0, i64 %and.i.i131.i
  %retval.sroa.3.0.i.i133.i = select i1 %cmp.i.i127.i, i64 -1, i64 %sub.i.i130.i
  %i9.i137.i = load i64, i64* %value3.i, align 8
  %i11.i139.i = load i64, i64* %mask6.i, align 8
  %or.i.i140.i = or i64 %retval.sroa.0.0.i.i132.i, %i9.i137.i
  %and.i1.i141.i = and i64 %retval.sroa.3.0.i.i133.i, %i11.i139.i
  %neg.i.i142.i = xor i64 %and.i1.i141.i, -1
  %and4.i.i143.i = and i64 %or.i.i140.i, %neg.i.i142.i
  store i64 %and4.i.i143.i, i64* %value3.i, align 8
  store i64 %and.i1.i141.i, i64* %mask6.i, align 8
  %i.i148.i = load i64, i64* %smin_value.i, align 8
  %i23.i.i = load i64, i64* %value.i, align 8
  %i24.i.i = load i64, i64* %mask.i, align 8
  %and.i149.i = and i64 %i24.i.i, -9223372036854775808
  %or.i150.i = or i64 %and.i149.i, %i23.i.i
  %cmp.i151.i = icmp sgt i64 %i.i148.i, %or.i150.i
  %cond.i152.i = select i1 %cmp.i151.i, i64 %i.i148.i, i64 %or.i150.i
  store i64 %cond.i152.i, i64* %smin_value.i, align 8
  %i25.i.i = load i64, i64* %smax_value.i, align 8
  %and7.i.i = and i64 %i24.i.i, 9223372036854775807
  %or8.i.i = or i64 %and7.i.i, %i23.i.i
  %cmp10.i.i = icmp slt i64 %i25.i.i, %or8.i.i
  %cond14.i.i = select i1 %cmp10.i.i, i64 %i25.i.i, i64 %or8.i.i
  store i64 %cond14.i.i, i64* %smax_value.i, align 8
  %i26.i.i = load i64, i64* %umin_value.i, align 8
  %cmp19.i.i = icmp ugt i64 %i26.i.i, %i23.i.i
  %cond23.i.i = select i1 %cmp19.i.i, i64 %i26.i.i, i64 %i23.i.i
  store i64 %cond23.i.i, i64* %umin_value.i, align 8
  %i27.i.i = load i64, i64* %umax_value.i, align 8
  %or29.i.i = or i64 %i24.i.i, %i23.i.i
  %cmp31.i156.i = icmp ult i64 %i27.i.i, %or29.i.i
  %cond35.i.i = select i1 %cmp31.i156.i, i64 %i27.i.i, i64 %or29.i.i
  store i64 %cond35.i.i, i64* %umax_value.i, align 8
  %i.i158.i = load i64, i64* %smin_value7.i, align 8
  %i23.i160.i = load i64, i64* %value3.i, align 8
  %i24.i162.i = load i64, i64* %mask6.i, align 8
  %and.i163.i = and i64 %i24.i162.i, -9223372036854775808
  %or.i164.i = or i64 %and.i163.i, %i23.i160.i
  %cmp.i165.i = icmp sgt i64 %i.i158.i, %or.i164.i
  %cond.i166.i = select i1 %cmp.i165.i, i64 %i.i158.i, i64 %or.i164.i
  store i64 %cond.i166.i, i64* %smin_value7.i, align 8
  %i25.i168.i = load i64, i64* %smax_value8.i, align 8
  %and7.i169.i = and i64 %i24.i162.i, 9223372036854775807
  %or8.i170.i = or i64 %and7.i169.i, %i23.i160.i
  %cmp10.i171.i = icmp slt i64 %i25.i168.i, %or8.i170.i
  %cond14.i172.i = select i1 %cmp10.i171.i, i64 %i25.i168.i, i64 %or8.i170.i
  store i64 %cond14.i172.i, i64* %smax_value8.i, align 8
  %i26.i174.i = load i64, i64* %umin_value9.i, align 8
  %cmp19.i175.i = icmp ugt i64 %i26.i174.i, %i23.i160.i
  %cond23.i176.i = select i1 %cmp19.i175.i, i64 %i26.i174.i, i64 %i23.i160.i
  store i64 %cond23.i176.i, i64* %umin_value9.i, align 8
  %i27.i178.i = load i64, i64* %umax_value10.i, align 8
  %or29.i179.i = or i64 %i24.i162.i, %i23.i160.i
  %cmp31.i180.i = icmp ult i64 %i27.i178.i, %or29.i179.i
  %cond35.i181.i = select i1 %cmp31.i180.i, i64 %i27.i178.i, i64 %or29.i179.i
  store i64 %cond35.i181.i, i64* %umax_value10.i, align 8
  br label %if.end117

if.else70:                                        ; preds = %if.then52
  %i69 = load i64, i64* %mask.i, align 8
  %tobool.not.i54 = icmp eq i64 %i69, 0
  br i1 %tobool.not.i54, label %cond.end90, label %if.end117

cond.end90:                                       ; preds = %if.else70
  %i70 = load i64, i64* %value.i, align 8
  %cond168.i58 = add i64 %i70, -1
  %i135.i59 = load i64, i64* %smax_value.i13, align 8
  %cmp185.i60 = icmp slt i64 %i135.i59, %cond168.i58
  %cond190.i61 = select i1 %cmp185.i60, i64 %i135.i59, i64 %cond168.i58
  store i64 %cond190.i61, i64* %smax_value.i13, align 8
  %i136.i62 = load i64, i64* %smin_value7.i12, align 8
  %cmp194.i63 = icmp sgt i64 %i136.i62, %i70
  %cond199.i64 = select i1 %cmp194.i63, i64 %i136.i62, i64 %i70
  store i64 %cond199.i64, i64* %smin_value7.i12, align 8
  %i.i42.i66 = load i64, i64* %smin_value.i10, align 8
  %cmp.i43.i67 = icmp sgt i64 %i.i42.i66, -1
  br i1 %cmp.i43.i67, label %if.then.i.i83, label %lor.lhs.false.i.i72

lor.lhs.false.i.i72:                              ; preds = %cond.end90
  %i33.i.i70 = load i64, i64* %smax_value.i13, align 8
  %cmp1.i45.i71 = icmp slt i64 %i33.i.i70, 0
  br i1 %cmp1.i45.i71, label %if.then.i.i83, label %if.end.i.i89

if.then.i.i83:                                    ; preds = %lor.lhs.false.i.i72, %cond.end90
  %i34.i.i74 = load i64, i64* %umin_value.i16, align 8
  %cmp3.i.i75 = icmp ugt i64 %i.i42.i66, %i34.i.i74
  %cond.i.i76 = select i1 %cmp3.i.i75, i64 %i.i42.i66, i64 %i34.i.i74
  store i64 %cond.i.i76, i64* %umin_value.i16, align 8
  store i64 %cond.i.i76, i64* %smin_value.i10, align 8
  %i35.i.i78 = load i64, i64* %smax_value.i13, align 8
  %i36.i.i80 = load i64, i64* %umax_value.i19, align 8
  %cmp8.i48.i81 = icmp ult i64 %i35.i.i78, %i36.i.i80
  %cond12.i.i82 = select i1 %cmp8.i48.i81, i64 %i35.i.i78, i64 %i36.i.i80
  store i64 %cond12.i.i82, i64* %umax_value.i19, align 8
  br label %__reg_deduce_bounds.exit.i101.sink.split

if.end.i.i89:                                     ; preds = %lor.lhs.false.i.i72
  %i37.i.i85 = load i64, i64* %umax_value.i19, align 8
  %cmp16.i.i86 = icmp sgt i64 %i37.i.i85, -1
  %i38.i.i88 = load i64, i64* %umin_value.i16, align 8
  br i1 %cmp16.i.i86, label %if.then17.i.i92, label %if.else.i.i94

if.then17.i.i92:                                  ; preds = %if.end.i.i89
  store i64 %i38.i.i88, i64* %smin_value.i10, align 8
  %cmp23.i.i90 = icmp ult i64 %i33.i.i70, %i37.i.i85
  %cond27.i.i91 = select i1 %cmp23.i.i90, i64 %i33.i.i70, i64 %i37.i.i85
  store i64 %cond27.i.i91, i64* %umax_value.i19, align 8
  br label %__reg_deduce_bounds.exit.i101.sink.split

if.else.i.i94:                                    ; preds = %if.end.i.i89
  %cmp31.i.i93 = icmp slt i64 %i38.i.i88, 0
  br i1 %cmp31.i.i93, label %if.then32.i.i97, label %__reg_deduce_bounds.exit.i101

if.then32.i.i97:                                  ; preds = %if.else.i.i94
  %cmp36.i.i95 = icmp ugt i64 %i.i42.i66, %i38.i.i88
  %cond40.i.i96 = select i1 %cmp36.i.i95, i64 %i.i42.i66, i64 %i38.i.i88
  store i64 %cond40.i.i96, i64* %umin_value.i16, align 8
  store i64 %cond40.i.i96, i64* %smin_value.i10, align 8
  br label %__reg_deduce_bounds.exit.i101.sink.split

__reg_deduce_bounds.exit.i101.sink.split:         ; preds = %if.then32.i.i97, %if.then17.i.i92, %if.then.i.i83
  %i37.i.i85.sink = phi i64 [ %i37.i.i85, %if.then32.i.i97 ], [ %cond27.i.i91, %if.then17.i.i92 ], [ %cond12.i.i82, %if.then.i.i83 ]
  store i64 %i37.i.i85.sink, i64* %smax_value.i13, align 8
  br label %__reg_deduce_bounds.exit.i101

__reg_deduce_bounds.exit.i101:                    ; preds = %__reg_deduce_bounds.exit.i101.sink.split, %if.else.i.i94
  %i.i50.i99 = load i64, i64* %smin_value7.i12, align 8
  %cmp.i51.i100 = icmp sgt i64 %i.i50.i99, -1
  br i1 %cmp.i51.i100, label %if.then.i66.i116, label %lor.lhs.false.i55.i105

lor.lhs.false.i55.i105:                           ; preds = %__reg_deduce_bounds.exit.i101
  %i33.i53.i103 = load i64, i64* %smax_value8.i15, align 8
  %cmp1.i54.i104 = icmp slt i64 %i33.i53.i103, 0
  br i1 %cmp1.i54.i104, label %if.then.i66.i116, label %if.end.i72.i122

if.then.i66.i116:                                 ; preds = %lor.lhs.false.i55.i105, %__reg_deduce_bounds.exit.i101
  %i34.i57.i107 = load i64, i64* %umin_value9.i18, align 8
  %cmp3.i58.i108 = icmp ugt i64 %i.i50.i99, %i34.i57.i107
  %cond.i59.i109 = select i1 %cmp3.i58.i108, i64 %i.i50.i99, i64 %i34.i57.i107
  store i64 %cond.i59.i109, i64* %umin_value9.i18, align 8
  store i64 %cond.i59.i109, i64* %smin_value7.i12, align 8
  %i35.i61.i111 = load i64, i64* %smax_value8.i15, align 8
  %i36.i63.i113 = load i64, i64* %umax_value10.i21, align 8
  %cmp8.i64.i114 = icmp ult i64 %i35.i61.i111, %i36.i63.i113
  %cond12.i65.i115 = select i1 %cmp8.i64.i114, i64 %i35.i61.i111, i64 %i36.i63.i113
  store i64 %cond12.i65.i115, i64* %umax_value10.i21, align 8
  br label %__reg_deduce_bounds.exit81.i137.sink.split

if.end.i72.i122:                                  ; preds = %lor.lhs.false.i55.i105
  %i37.i68.i118 = load i64, i64* %umax_value10.i21, align 8
  %cmp16.i69.i119 = icmp sgt i64 %i37.i68.i118, -1
  %i38.i71.i121 = load i64, i64* %umin_value9.i18, align 8
  br i1 %cmp16.i69.i119, label %if.then17.i75.i125, label %if.else.i77.i127

if.then17.i75.i125:                               ; preds = %if.end.i72.i122
  store i64 %i38.i71.i121, i64* %smin_value7.i12, align 8
  %cmp23.i73.i123 = icmp ult i64 %i33.i53.i103, %i37.i68.i118
  %cond27.i74.i124 = select i1 %cmp23.i73.i123, i64 %i33.i53.i103, i64 %i37.i68.i118
  store i64 %cond27.i74.i124, i64* %umax_value10.i21, align 8
  br label %__reg_deduce_bounds.exit81.i137.sink.split

if.else.i77.i127:                                 ; preds = %if.end.i72.i122
  %cmp31.i76.i126 = icmp slt i64 %i38.i71.i121, 0
  br i1 %cmp31.i76.i126, label %if.then32.i80.i130, label %__reg_deduce_bounds.exit81.i137

if.then32.i80.i130:                               ; preds = %if.else.i77.i127
  %cmp36.i78.i128 = icmp ugt i64 %i.i50.i99, %i38.i71.i121
  %cond40.i79.i129 = select i1 %cmp36.i78.i128, i64 %i.i50.i99, i64 %i38.i71.i121
  store i64 %cond40.i79.i129, i64* %umin_value9.i18, align 8
  store i64 %cond40.i79.i129, i64* %smin_value7.i12, align 8
  br label %__reg_deduce_bounds.exit81.i137.sink.split

__reg_deduce_bounds.exit81.i137.sink.split:       ; preds = %if.then32.i80.i130, %if.then17.i75.i125, %if.then.i66.i116
  %i37.i68.i118.sink = phi i64 [ %i37.i68.i118, %if.then32.i80.i130 ], [ %cond27.i74.i124, %if.then17.i75.i125 ], [ %cond12.i65.i115, %if.then.i66.i116 ]
  store i64 %i37.i68.i118.sink, i64* %smax_value8.i15, align 8
  br label %__reg_deduce_bounds.exit81.i137

__reg_deduce_bounds.exit81.i137:                  ; preds = %__reg_deduce_bounds.exit81.i137.sink.split, %if.else.i77.i127
  %i.i83.i132 = load i64, i64* %umin_value.i16, align 8
  %i5.i85.i134 = load i64, i64* %umax_value.i19, align 8
  %xor.i.i.i135 = xor i64 %i5.i85.i134, %i.i83.i132
  %cmp.i.i.i.i136 = icmp eq i64 %xor.i.i.i135, 0
  br i1 %cmp.i.i.i.i136, label %__reg_bound_offset.exit.i195, label %if.end.i.i.i.i167

if.end.i.i.i.i167:                                ; preds = %__reg_deduce_bounds.exit81.i137
  %tobool.not.i.i.i.i.i138 = icmp ult i64 %xor.i.i.i135, 4294967296
  %shl.i.i.i.i.i139 = shl i64 %xor.i.i.i135, 32
  %spec.select.i.i.i.i.i140 = select i1 %tobool.not.i.i.i.i.i138, i64 %shl.i.i.i.i.i139, i64 %xor.i.i.i135
  %spec.select17.i.i.i.i.i141 = select i1 %tobool.not.i.i.i.i.i138, i32 31, i32 63
  %tobool2.not.i.i.i.i.i142 = icmp ult i64 %spec.select.i.i.i.i.i140, 281474976710656
  %sub4.i.i.i.i.i143 = add nsw i32 %spec.select17.i.i.i.i.i141, -16
  %shl5.i.i.i.i.i144 = shl i64 %spec.select.i.i.i.i.i140, 16
  %word.addr.1.i.i.i.i.i145 = select i1 %tobool2.not.i.i.i.i.i142, i64 %shl5.i.i.i.i.i144, i64 %spec.select.i.i.i.i.i140
  %num.1.i.i.i.i.i146 = select i1 %tobool2.not.i.i.i.i.i142, i32 %sub4.i.i.i.i.i143, i32 %spec.select17.i.i.i.i.i141
  %tobool8.not.i.i.i.i.i147 = icmp ult i64 %word.addr.1.i.i.i.i.i145, 72057594037927936
  %sub10.i.i.i.i.i148 = add nsw i32 %num.1.i.i.i.i.i146, -8
  %shl11.i.i.i.i.i149 = shl i64 %word.addr.1.i.i.i.i.i145, 8
  %word.addr.2.i.i.i.i.i150 = select i1 %tobool8.not.i.i.i.i.i147, i64 %shl11.i.i.i.i.i149, i64 %word.addr.1.i.i.i.i.i145
  %num.2.i.i.i.i.i151 = select i1 %tobool8.not.i.i.i.i.i147, i32 %sub10.i.i.i.i.i148, i32 %num.1.i.i.i.i.i146
  %tobool14.not.i.i.i.i.i152 = icmp ult i64 %word.addr.2.i.i.i.i.i150, 1152921504606846976
  %sub16.i.i.i.i.i153 = add nsw i32 %num.2.i.i.i.i.i151, -4
  %shl17.i.i.i.i.i154 = shl i64 %word.addr.2.i.i.i.i.i150, 4
  %word.addr.3.i.i.i.i.i155 = select i1 %tobool14.not.i.i.i.i.i152, i64 %shl17.i.i.i.i.i154, i64 %word.addr.2.i.i.i.i.i150
  %num.3.i.i.i.i.i156 = select i1 %tobool14.not.i.i.i.i.i152, i32 %sub16.i.i.i.i.i153, i32 %num.2.i.i.i.i.i151
  %tobool20.not.i.i.i.i.i157 = icmp ult i64 %word.addr.3.i.i.i.i.i155, 4611686018427387904
  %sub22.i.i.i.i.i158 = add i32 %num.3.i.i.i.i.i156, 254
  %shl23.i.i.i.i.i159 = shl i64 %word.addr.3.i.i.i.i.i155, 2
  %word.addr.4.i.i.i.i.i160 = select i1 %tobool20.not.i.i.i.i.i157, i64 %shl23.i.i.i.i.i159, i64 %word.addr.3.i.i.i.i.i155
  %num.4.i.i.i.i.i161 = select i1 %tobool20.not.i.i.i.i.i157, i32 %sub22.i.i.i.i.i158, i32 %num.3.i.i.i.i.i156
  %word.addr.4.lobit.i.i.i.i.i162.neg = lshr i64 %word.addr.4.i.i.i.i.i160, 63
  %i.i.i.i.i.i163.neg = trunc i64 %word.addr.4.lobit.i.i.i.i.i162.neg to i32
  %add.i.i.i.i166 = add i32 %num.4.i.i.i.i.i161, %i.i.i.i.i.i163.neg
  %phi.bo = and i32 %add.i.i.i.i166, 255
  br label %__reg_bound_offset.exit.i195

__reg_bound_offset.exit.i195:                     ; preds = %if.end.i.i.i.i167, %__reg_deduce_bounds.exit81.i137
  %retval.0.i.i.i.i168 = phi i32 [ %phi.bo, %if.end.i.i.i.i167 ], [ 0, %__reg_deduce_bounds.exit81.i137 ]
  %cmp.i.i.i170 = icmp ugt i32 %retval.0.i.i.i.i168, 63
  %sh_prom.i.i.i171 = zext i32 %retval.0.i.i.i.i168 to i64
  %notmask.i.i.i172 = shl nsw i64 -1, %sh_prom.i.i.i171
  %sub.i.i.i173 = xor i64 %notmask.i.i.i172, -1
  %and.i.i.i174 = and i64 %notmask.i.i.i172, %i.i83.i132
  %retval.sroa.0.0.i.i.i175 = select i1 %cmp.i.i.i170, i64 0, i64 %and.i.i.i174
  %retval.sroa.3.0.i.i.i176 = select i1 %cmp.i.i.i170, i64 -1, i64 %sub.i.i.i173
  %i9.i.i180 = load i64, i64* %value.i4, align 8
  %i11.i.i182 = load i64, i64* %mask.i7, align 8
  %or.i.i.i183 = or i64 %retval.sroa.0.0.i.i.i175, %i9.i.i180
  %and.i1.i.i184 = and i64 %retval.sroa.3.0.i.i.i176, %i11.i.i182
  %neg.i.i.i185 = xor i64 %and.i1.i.i184, -1
  %and4.i.i.i186 = and i64 %or.i.i.i183, %neg.i.i.i185
  store i64 %and4.i.i.i186, i64* %value.i4, align 8
  store i64 %and.i1.i.i184, i64* %mask.i7, align 8
  %i.i90.i190 = load i64, i64* %umin_value9.i18, align 8
  %i5.i92.i192 = load i64, i64* %umax_value10.i21, align 8
  %xor.i.i93.i193 = xor i64 %i5.i92.i192, %i.i90.i190
  %cmp.i.i.i94.i194 = icmp eq i64 %xor.i.i93.i193, 0
  br i1 %cmp.i.i.i94.i194, label %reg_set_min_max_inv.exit, label %if.end.i.i.i124.i225

if.end.i.i.i124.i225:                             ; preds = %__reg_bound_offset.exit.i195
  %tobool.not.i.i.i.i95.i196 = icmp ult i64 %xor.i.i93.i193, 4294967296
  %shl.i.i.i.i96.i197 = shl i64 %xor.i.i93.i193, 32
  %spec.select.i.i.i.i97.i198 = select i1 %tobool.not.i.i.i.i95.i196, i64 %shl.i.i.i.i96.i197, i64 %xor.i.i93.i193
  %spec.select17.i.i.i.i98.i199 = select i1 %tobool.not.i.i.i.i95.i196, i32 31, i32 63
  %tobool2.not.i.i.i.i99.i200 = icmp ult i64 %spec.select.i.i.i.i97.i198, 281474976710656
  %sub4.i.i.i.i100.i201 = add nsw i32 %spec.select17.i.i.i.i98.i199, -16
  %shl5.i.i.i.i101.i202 = shl i64 %spec.select.i.i.i.i97.i198, 16
  %word.addr.1.i.i.i.i102.i203 = select i1 %tobool2.not.i.i.i.i99.i200, i64 %shl5.i.i.i.i101.i202, i64 %spec.select.i.i.i.i97.i198
  %num.1.i.i.i.i103.i204 = select i1 %tobool2.not.i.i.i.i99.i200, i32 %sub4.i.i.i.i100.i201, i32 %spec.select17.i.i.i.i98.i199
  %tobool8.not.i.i.i.i104.i205 = icmp ult i64 %word.addr.1.i.i.i.i102.i203, 72057594037927936
  %sub10.i.i.i.i105.i206 = add nsw i32 %num.1.i.i.i.i103.i204, -8
  %shl11.i.i.i.i106.i207 = shl i64 %word.addr.1.i.i.i.i102.i203, 8
  %word.addr.2.i.i.i.i107.i208 = select i1 %tobool8.not.i.i.i.i104.i205, i64 %shl11.i.i.i.i106.i207, i64 %word.addr.1.i.i.i.i102.i203
  %num.2.i.i.i.i108.i209 = select i1 %tobool8.not.i.i.i.i104.i205, i32 %sub10.i.i.i.i105.i206, i32 %num.1.i.i.i.i103.i204
  %tobool14.not.i.i.i.i109.i210 = icmp ult i64 %word.addr.2.i.i.i.i107.i208, 1152921504606846976
  %sub16.i.i.i.i110.i211 = add nsw i32 %num.2.i.i.i.i108.i209, -4
  %shl17.i.i.i.i111.i212 = shl i64 %word.addr.2.i.i.i.i107.i208, 4
  %word.addr.3.i.i.i.i112.i213 = select i1 %tobool14.not.i.i.i.i109.i210, i64 %shl17.i.i.i.i111.i212, i64 %word.addr.2.i.i.i.i107.i208
  %num.3.i.i.i.i113.i214 = select i1 %tobool14.not.i.i.i.i109.i210, i32 %sub16.i.i.i.i110.i211, i32 %num.2.i.i.i.i108.i209
  %tobool20.not.i.i.i.i114.i215 = icmp ult i64 %word.addr.3.i.i.i.i112.i213, 4611686018427387904
  %sub22.i.i.i.i115.i216 = add i32 %num.3.i.i.i.i113.i214, 254
  %shl23.i.i.i.i116.i217 = shl i64 %word.addr.3.i.i.i.i112.i213, 2
  %word.addr.4.i.i.i.i117.i218 = select i1 %tobool20.not.i.i.i.i114.i215, i64 %shl23.i.i.i.i116.i217, i64 %word.addr.3.i.i.i.i112.i213
  %num.4.i.i.i.i118.i219 = select i1 %tobool20.not.i.i.i.i114.i215, i32 %sub22.i.i.i.i115.i216, i32 %num.3.i.i.i.i113.i214
  %word.addr.4.lobit.i.i.i.i119.i220.neg = lshr i64 %word.addr.4.i.i.i.i117.i218, 63
  %i.i.i.i.i120.i221.neg = trunc i64 %word.addr.4.lobit.i.i.i.i119.i220.neg to i32
  %add.i.i.i123.i224 = add i32 %num.4.i.i.i.i118.i219, %i.i.i.i.i120.i221.neg
  %phi.bo13 = and i32 %add.i.i.i123.i224, 255
  br label %reg_set_min_max_inv.exit

reg_set_min_max_inv.exit:                         ; preds = %if.end.i.i.i124.i225, %__reg_bound_offset.exit.i195
  %retval.0.i.i.i125.i226 = phi i32 [ %phi.bo13, %if.end.i.i.i124.i225 ], [ 0, %__reg_bound_offset.exit.i195 ]
  %cmp.i.i127.i228 = icmp ugt i32 %retval.0.i.i.i125.i226, 63
  %sh_prom.i.i128.i229 = zext i32 %retval.0.i.i.i125.i226 to i64
  %notmask.i.i129.i230 = shl nsw i64 -1, %sh_prom.i.i128.i229
  %sub.i.i130.i231 = xor i64 %notmask.i.i129.i230, -1
  %and.i.i131.i232 = and i64 %notmask.i.i129.i230, %i.i90.i190
  %retval.sroa.0.0.i.i132.i233 = select i1 %cmp.i.i127.i228, i64 0, i64 %and.i.i131.i232
  %retval.sroa.3.0.i.i133.i234 = select i1 %cmp.i.i127.i228, i64 -1, i64 %sub.i.i130.i231
  %i9.i137.i238 = load i64, i64* %value3.i6, align 8
  %i11.i139.i240 = load i64, i64* %mask6.i9, align 8
  %or.i.i140.i241 = or i64 %retval.sroa.0.0.i.i132.i233, %i9.i137.i238
  %and.i1.i141.i242 = and i64 %retval.sroa.3.0.i.i133.i234, %i11.i139.i240
  %neg.i.i142.i243 = xor i64 %and.i1.i141.i242, -1
  %and4.i.i143.i244 = and i64 %or.i.i140.i241, %neg.i.i142.i243
  store i64 %and4.i.i143.i244, i64* %value3.i6, align 8
  store i64 %and.i1.i141.i242, i64* %mask6.i9, align 8
  %i.i148.i248 = load i64, i64* %smin_value.i10, align 8
  %i23.i.i250 = load i64, i64* %value.i4, align 8
  %i24.i.i252 = load i64, i64* %mask.i7, align 8
  %and.i149.i253 = and i64 %i24.i.i252, -9223372036854775808
  %or.i150.i254 = or i64 %and.i149.i253, %i23.i.i250
  %cmp.i151.i255 = icmp sgt i64 %i.i148.i248, %or.i150.i254
  %cond.i152.i256 = select i1 %cmp.i151.i255, i64 %i.i148.i248, i64 %or.i150.i254
  store i64 %cond.i152.i256, i64* %smin_value.i10, align 8
  %i25.i.i258 = load i64, i64* %smax_value.i13, align 8
  %and7.i.i259 = and i64 %i24.i.i252, 9223372036854775807
  %or8.i.i260 = or i64 %and7.i.i259, %i23.i.i250
  %cmp10.i.i261 = icmp slt i64 %i25.i.i258, %or8.i.i260
  %cond14.i.i262 = select i1 %cmp10.i.i261, i64 %i25.i.i258, i64 %or8.i.i260
  store i64 %cond14.i.i262, i64* %smax_value.i13, align 8
  %i26.i.i264 = load i64, i64* %umin_value.i16, align 8
  %cmp19.i.i265 = icmp ugt i64 %i26.i.i264, %i23.i.i250
  %cond23.i.i266 = select i1 %cmp19.i.i265, i64 %i26.i.i264, i64 %i23.i.i250
  store i64 %cond23.i.i266, i64* %umin_value.i16, align 8
  %i27.i.i268 = load i64, i64* %umax_value.i19, align 8
  %or29.i.i269 = or i64 %i24.i.i252, %i23.i.i250
  %cmp31.i156.i270 = icmp ult i64 %i27.i.i268, %or29.i.i269
  %cond35.i.i271 = select i1 %cmp31.i156.i270, i64 %i27.i.i268, i64 %or29.i.i269
  store i64 %cond35.i.i271, i64* %umax_value.i19, align 8
  %i.i158.i273 = load i64, i64* %smin_value7.i12, align 8
  %i23.i160.i275 = load i64, i64* %value3.i6, align 8
  %i24.i162.i277 = load i64, i64* %mask6.i9, align 8
  %and.i163.i278 = and i64 %i24.i162.i277, -9223372036854775808
  %or.i164.i279 = or i64 %and.i163.i278, %i23.i160.i275
  %cmp.i165.i280 = icmp sgt i64 %i.i158.i273, %or.i164.i279
  %cond.i166.i281 = select i1 %cmp.i165.i280, i64 %i.i158.i273, i64 %or.i164.i279
  store i64 %cond.i166.i281, i64* %smin_value7.i12, align 8
  %i25.i168.i283 = load i64, i64* %smax_value8.i15, align 8
  %and7.i169.i284 = and i64 %i24.i162.i277, 9223372036854775807
  %or8.i170.i285 = or i64 %and7.i169.i284, %i23.i160.i275
  %cmp10.i171.i286 = icmp slt i64 %i25.i168.i283, %or8.i170.i285
  %cond14.i172.i287 = select i1 %cmp10.i171.i286, i64 %i25.i168.i283, i64 %or8.i170.i285
  store i64 %cond14.i172.i287, i64* %smax_value8.i15, align 8
  %i26.i174.i289 = load i64, i64* %umin_value9.i18, align 8
  %cmp19.i175.i290 = icmp ugt i64 %i26.i174.i289, %i23.i160.i275
  %cond23.i176.i291 = select i1 %cmp19.i175.i290, i64 %i26.i174.i289, i64 %i23.i160.i275
  store i64 %cond23.i176.i291, i64* %umin_value9.i18, align 8
  %i27.i178.i293 = load i64, i64* %umax_value10.i21, align 8
  %or29.i179.i294 = or i64 %i24.i162.i277, %i23.i160.i275
  %cmp31.i180.i295 = icmp ult i64 %i27.i178.i293, %or29.i179.i294
  %cond35.i181.i296 = select i1 %cmp31.i180.i295, i64 %i27.i178.i293, i64 %or29.i179.i294
  store i64 %cond35.i181.i296, i64* %umax_value10.i21, align 8
  br label %if.end117

if.end117:                                        ; preds = %reg_set_min_max_inv.exit, %if.else70, %reg_set_min_max.exit, %if.then44, %is_branch_taken.exit
  ret void
}

attributes #0 = { mustprogress nofree noinline norecurse noredzone nosync nounwind null_pointer_is_valid sspstrong willreturn "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+retpoline-external-thunk,+retpoline-indirect-branches,+retpoline-indirect-calls,-3dnow,-3dnowa,-aes,-avx,-avx2,-avx512bf16,-avx512bitalg,-avx512bw,-avx512cd,-avx512dq,-avx512er,-avx512f,-avx512fp16,-avx512ifma,-avx512pf,-avx512vbmi,-avx512vbmi2,-avx512vl,-avx512vnni,-avx512vp2intersect,-avx512vpopcntdq,-avxvnni,-f16c,-fma,-fma4,-gfni,-kl,-mmx,-pclmul,-sha,-sse,-sse2,-sse3,-sse4.1,-sse4.2,-sse4a,-ssse3,-vaes,-vpclmulqdq,-widekl,-x87,-xop" "tune-cpu"="generic" "warn-stack-size"="2048" }

!llvm.ident = !{!0, !0}
!llvm.module.flags = !{!1, !2, !3, !4}

!0 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
!1 = !{i32 1, !"wchar_size", i32 2}
!2 = !{i32 1, !"Code Model", i32 2}
!3 = !{i32 1, !"override-stack-alignment", i32 8}
!4 = !{i32 4, !"SkipRaxSetup", i32 1}
