#!/usr/bin/env python3
"""Slurm License Charm."""
import os
import subprocess

from interface_prolog_epilog import PrologEpilog
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus


class LicenseManagerCharm(CharmBase):
    """This charm manages the lifecycle of the license-manager snap."""

    _stored = StoredState()

    def __init__(self, *args):
        """Initialize charm, configure states, and events to observe."""
        super().__init__(*args)

        self._stored.set_default(license_manager_installed=False)

        self._license = PrologEpilog(self, 'prolog-epilog')

        event_handler_bindings = {
            self.on.install: self._on_install,
            self.on.update_status: self._on_update_status,
            self.on.upgrade_charm: self._on_upgrade_charm,

        }
        for event, handler in event_handler_bindings.items():
            self.framework.observe(event, handler)

    def _on_install(self, event):
        """Install license-manager snap."""
        if self._install_license_manager_snap():
            self._stored.license_manager_installed = True
        else:
            self._stored.license_manager_installed = False
        self._on_update_status(event)

    def _on_upgrade_charm(self, event):
        """upgrade-charm handler."""
        if self._install_license_manager_snap():
            self._stored.license_manager_installed = True
            self.unit.status = ActiveStatus("License Snap upgraded")
            self.unit.set_workload_version(self._get_version())
        else:
            self._stored.license_manager_installed = False
        self._on_update_status(event)

    def _on_update_status(self, event):
        """update-status handler."""
        if self._stored.license_manager_installed:
            self.unit.status = ActiveStatus("License Snap Installed")
        else:
            self.unit.status = BlockedStatus(
                "license-manager snap could not install, please debug"
            )

    def _get_version(self):
        """Retrieve, decode, strip, and return the version."""
        version = subprocess.check_output([
            "/snap/bin/license-manager.version"
        ])
        return version.decode().strip()

    def _install_license_manager_snap(self):
        """Install the license-manager snap."""
        ret = subprocess.check_call(
            [
                "/usr/bin/snap",
                "install",
                self.model.resources.fetch('license-manager'),
                "--dangerous",
                "--classic"
            ],
            env={
                'PATH': f"{os.environ['PATH']}:/var/lib/snapd/snap/bin"
            },
        )
        if ret != 0:
            return False
        return True


if __name__ == "__main__":
    main(LicenseManagerCharm)
