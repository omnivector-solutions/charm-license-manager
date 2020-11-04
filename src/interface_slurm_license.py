#!/usr/bin/python3
"""Slurm License interface."""
import json
import logging

from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
)

logger = logging.getLogger()


class SlurmLicense(Object):
    """SlurmLicense interface."""

    def __init__(self, charm, relation_name):
        """Set the initial data."""
        super().__init__(charm, relation_name)

        self.charm = charm
        self.framework.observe(
            charm.on[relation_name].relation_created,
            self._on_relation_created
        )

    def _on_relation_created(self, event):
        event.relation.data[self.model.unit]['epilog'] = self.model.config['slurmctld_epilog_path']
        event.relation.data[self.model.unit]['prolog'] = self.model.config['slurmctld_prolog_path']
