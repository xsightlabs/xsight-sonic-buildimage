Avoid swss restart (SIGABT) on syncd communication timeout under gdb
====================================================================

**Descritpion**

If to attach to syncd via gdb - orchagent will get timeout, when there is no answers form syncd.
We can prevent orchagent from timeout exception with `SAI_REDIS_DEFAULT_SYNC_OPERATION_RESPONSE_TIMEOUT` increasing.

**Usage**

Just change string

```
exec /usr/bin/orchagent ${ORCHAGENT_ARGS}
```

to

```
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libsairedisnonstop.so.0 exec /usr/bin/orchagent ${ORCHAGENT_ARGS}
```

in `/usr/bin/orchagent.sh` file (swss container)
and reload services `config reload`.

