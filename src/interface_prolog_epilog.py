#!/usr/bin/python3
"""Slurm License interface."""
from ops.framework import Object


class PrologEpilog(Object):
    """Prolog/Epilog interface."""

    def __init__(self, charm, relation_name):
        """Set the initial data."""
        super().__init__(charm, relation_name)

        self.framework.observe(
            charm.on[relation_name].relation_created,
            self._on_relation_created
        )

    def _on_relation_created(self, event):
        event.relation.data[self.model.unit]['epilog'] = \
            self.model.config['slurmctld_epilog_path']
        event.relation.data[self.model.unit]['prolog'] = \
            self.model.config['slurmctld_prolog_path']
