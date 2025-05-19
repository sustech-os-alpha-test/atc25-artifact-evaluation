/usr/local/benchmark/fio/bin/fio -rw=write -filename=./fio-test -name=seqwrite \
    -size=1G -bs=1M \
    -ioengine=sync -direct=1 -numjobs=1 \
    -time_based=1 -ramp_time=20 -runtime=40