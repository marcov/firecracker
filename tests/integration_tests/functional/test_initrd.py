# Copyright 2019 SUSE LLC
# SPDX-License-Identifier: Apache-2.0
"""Tests for initrd."""

from framework.microvm import Serial

INITRD_FILESYSTEM = "rootfs"


def test_microvm_initrd_with_serial(
        test_microvm_with_initrd):
    """Check microvm started with an inird has / mounted as rootfs."""
    vm = test_microvm_with_initrd
    vm.jailer.daemonize = False
    vm.spawn()
    vm.memory_events_queue = None

    vm.basic_config(
        add_root_device=False,
        boot_args='console=ttyS0 reboot=k panic=1 pci=off',
        use_initrd=True
    )

    vm.start()
    serial = Serial(vm)
    serial.open()
    serial.rx(token='login: ')
    serial.tx("root")

    serial.rx(token='Password: ')
    serial.tx("root")

    serial.rx(token='# ')

    serial.tx(f"findmnt /")
    serial.rx(
        token=f"/      {INITRD_FILESYSTEM} {INITRD_FILESYSTEM}")
