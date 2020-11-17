#!/usr/bin/python3
"""Slurm License Charm."""
import subprocess

from interface_prolog_epilog import PrologEpilog
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus


class LicenseCharm(CharmBase):
    """Facilitate licenses for slurm workloads."""

    def __init__(self, *args):
        """Initialize charm, configure states, and events to observe."""
        super().__init__(*args)

        self._license = PrologEpilog(self, 'prolog-epilog')

        event_handler_bindings = {
            self.on.install: self._on_install,

            self.on.upgrade_charm: self._on_upgrade_charm,

        }
        for event, handler in event_handler_bindings.items():
            self.framework.observe(event, handler)

    def _on_install(self, event):
        """Install Slurm-license snap."""
        subprocess.run(
            [
                "snap",
                "install",
                self.model.resources.fetch('license-manager'),
                "--dangerous",
                "--classic"
            ]
        )
        self.unit.status = ActiveStatus("License Snap Installed")

    def _on_upgrade_charm(self, event):
        """Install Slurm-license snap."""
        subprocess.run(
            [
                "snap",
                "refresh",
                self.model.resources.fetch('license-manager'),
                "--dangerous",
                "--classic",
            ]
        )
        self.unit.status = ActiveStatus("License Snap upgraded")


if __name__ == "__main__":
    main(LicenseCharm)
