#include <stdlib.h>
#include <linux/seccomp.h>

void __attribute__ ((constructor (0))) install_syscall_filter() {
  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0); // FROM 0
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(open), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(stat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(lstat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(lseek), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mprotect), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(munmap), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(access), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(select), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sched_yield), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mremap), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(madvise), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(dup), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(dup2), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(pause), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(nanosleep), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(alarm), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getpid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(sendfile), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(uname), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fcntl), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fsync), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fdatasync), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getcwd), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(gettimeofday), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(getrlimit), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(getrusage), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(sysinfo), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(times), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getuid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getgid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(geteuid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getegid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(getppid), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(getpgrp), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getgroups), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getresuid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getresgid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(getpgid), 1); // TO 126
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(mlock), 1); // FROM 149
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(munlock), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(mlockall), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(munlockall), 1);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(gettid), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(time), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(futex), 0); // TO 211
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(clock_nanosleep), 0); // FROM 230
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0); // TO 231
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(newfstatat), 0); // FROM 256
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(faccessat), 0); // TO 269
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getrandom), 0); // FROM 307 TO END
  seccomp_load(ctx);
  seccomp_release(ctx);
}
