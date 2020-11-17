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


class LicenseCharm(CharmBase):
    """Facilitate licenses for slurm workloads."""

    stored = StoredState()

    def __init__(self, *args):
        """Initialize charm, configure states, and events to observe."""
        super().__init__(*args)
        self.stored.set_default(
            install=False,
        )

        self._license = SlurmLicense(self, 'prolog-epilog')
        event_handler_bindings = {
            self.on.install: self._on_install,
            self.on.start: self._on_start,
            self.on.config_changed: self._on_config_changed,
        }
        for event, handler in event_handler_bindings.items():
            self.framework.observe(event, handler)

    def _on_install(self, event):
        """Install Slurm-license snap."""
        subprocess.run(
            ["sudo", "snap", "install", self.model.resources.fetch('slurm-license'), "--dangerous"]
        )
        self.unit.status = ActiveStatus("License Snap Installed")

    def _on_start(self, event):
        """Start Snap."""
        self.unit.status = ActiveStatus("Snap Started")
    
    def _on_config_changed(self, event):
        """Set snap mode."""
        if self.model.config["snap-mode"]:
            subprocess.run(
                [
                    "snap",
                    "set",
                    "license-manager",
                    "snap.mode=" + self.model.config["snap-mode"]
                ]
            )
        self.unit.status = ActiveStatus("snap mode set")


if __name__ == "__main__":
    main(LicenseCharm)
