#!/usr/bin/env python3.6
# for FreeBSD
import subprocess
import os
import sys
# define what host there should be
hostlist=['g0']
g0_props={'name': 'g0', 'cpucores': '2', 'RAM': '2048', 'nic0': 'tap0', 'zfstarget': '/dev/zvol/zroot/bhyveguest0', 'application': '/usr/share/examples/bhyve/vmrun.sh', 'inscreen': true}
# define bhyve guests

