# Safety (TCB) evaluation

To measure codebase size and Trusted Computing Base metrics:

```shell
export SYSTEM={system_name} # Choose from: asterinas|redleaf|theseus|tock
./$SYSTEM-tcb.sh
```

The console will display the total and the TCB LoC of the target system. The output looks like:

```text
----------------------------------
Total:  {Total LoC}
----------------------------------
TCB:  {TCB LoC}
----------------------------------
```
