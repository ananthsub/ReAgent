#!/usr/bin/env python3

from typing import Dict, List

from reagent.core.dataclasses import dataclass, field
from reagent.models.actor import GaussianFullyConnectedActor
from reagent.models.base import ModelBase
from reagent.net_builder.continuous_actor_net_builder import ContinuousActorNetBuilder
from reagent.parameters import NormalizationParameters, param_hash
from reagent.preprocessing.identify_types import CONTINUOUS_ACTION
from reagent.preprocessing.normalization import get_num_output_features


@dataclass
class GaussianFullyConnected(ContinuousActorNetBuilder):
    __hash__ = param_hash

    sizes: List[int] = field(default_factory=lambda: [128, 64])
    activations: List[str] = field(default_factory=lambda: ["relu", "relu"])
    use_batch_norm: bool = False
    use_layer_norm: bool = False

    def __post_init_post_parse__(self):
        super().__init__()
        assert len(self.sizes) == len(self.activations), (
            f"Must have the same numbers of sizes and activations; got: "
            f"{self.sizes}, {self.activations}"
        )

    @property
    def default_action_preprocessing(self) -> str:
        return CONTINUOUS_ACTION

    def build_actor(
        self,
        state_normalization: Dict[int, NormalizationParameters],
        action_normalization: Dict[int, NormalizationParameters],
    ) -> ModelBase:
        state_dim = get_num_output_features(state_normalization)
        action_dim = get_num_output_features(action_normalization)
        return GaussianFullyConnectedActor(
            state_dim=state_dim,
            action_dim=action_dim,
            sizes=self.sizes,
            activations=self.activations,
            use_batch_norm=self.use_batch_norm,
            use_layer_norm=self.use_layer_norm,
        )
