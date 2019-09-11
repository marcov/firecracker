# Copyright 2019 SUSE LLC
# SPDX-License-Identifier: Apache-2.0
"""Tests for initd."""

from host_tools.network import SSHConnection

INITRD_FILESYSTEM = "rootfs"


def test_microvm_initrd(
        test_microvm_with_initrd,
        network_config):
    """Check microvm started with an inird has / mounted as rootfs."""
    vm = test_microvm_with_initrd
    vm.spawn()
    vm.basic_config(
        add_root_device=False,
        use_initrd=True
    )
    _tap, _, _ = vm.ssh_network_config(network_config, '1')
    vm.start()

    # Find out  what is the filesystem of /, and make sure initrd is used
    conn = SSHConnection(vm.ssh_config)
    ecode, _, _ = conn.execute_command(
        f"findmnt / | grep -q -w {INITRD_FILESYSTEM}")
    assert ecode == 0
