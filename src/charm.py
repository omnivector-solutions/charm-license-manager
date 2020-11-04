#!/usr/bin/python3
"""Slurm License Charm."""
import logging
import subprocess

from interface_slurm_license import SlurmLicense
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger()


class SlurmLicenseCharm(CharmBase):
    """Facilitate licenses for slurm workloads."""

    stored = StoredState()

    def __init__(self, *args):
        """Initialize charm, configure states, and events to observe."""
        super().__init__(*args)
        self.stored.set_default(
            install=False,
        )

        self._license = SlurmLicense(self, 'slurm-license')
        event_handler_bindings = {
            self.on.install: self._on_install,
            self.on.start: self._on_start,
        }
        for event, handler in event_handler_bindings.items():
            self.framework.observe(event, handler)

    def _on_install(self, event):
        """Install Slurm-license snap."""
        subprocess.run(
            ["sudo", "snap", "install", self.model.resources.fetch('slurm-lic-snap'), "--dangerous"]
        )
        self.unit.status = ActiveStatus("License Snap Installed")

    def _on_start(self, event):
        """Start Snap."""
        self.unit.status = ActiveStatus("Snap Started")


if __name__ == "__main__":
    main(SlurmLicenseCharm)
