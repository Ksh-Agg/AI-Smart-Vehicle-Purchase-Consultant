"""Specification models loader component."""

from sqlalchemy.orm import Session

from app.db.models.dimension_spec import DimensionSpec
from app.db.models.engine_spec import EngineSpec
from app.db.models.feature_spec import FeatureSpec
from app.db.models.ownership_spec import OwnershipSpec
from app.db.models.safety_spec import SafetySpec
from app.db.models.availability_spec import AvailabilitySpec
from app.db.models.environmental_spec import EnvironmentalSpec

from app.etl.models.specs import (
    CanonicalAvailabilitySpec,
    CanonicalDimensionSpec,
    CanonicalEngineSpec,
    CanonicalEnvironmentalSpec,
    CanonicalFeatureSpec,
    CanonicalOwnershipSpec,
    CanonicalSafetySpec,
)


class SpecsLoader:
    """Handles loading and updating child specification tables linked to a Vehicle ID."""

    def load_specs(
        self,
        session: Session,
        vehicle_id: int,
        engine_data: CanonicalEngineSpec,
        dimension_data: CanonicalDimensionSpec,
        safety_data: CanonicalSafetySpec,
        feature_data: CanonicalFeatureSpec,
        ownership_data: CanonicalOwnershipSpec,
        availability_data: CanonicalAvailabilitySpec,
        environmental_data: CanonicalEnvironmentalSpec,
    ) -> None:
        """Loads or updates all child specifications for a given vehicle_id.

        Args:
            session: Active SQLAlchemy Session.
            vehicle_id: Target Vehicle PK ID.
            engine_data: Engine specs.
            dimension_data: Dimension specs.
            safety_data: Safety specs.
            feature_data: Feature specs.
            ownership_data: Ownership specs.
            availability_data: Availability specs.
            environmental_data: Environmental specs.
        """
        # 1. Engine Spec
        engine = session.get(EngineSpec, vehicle_id)
        if not engine:
            engine = EngineSpec(vehicle_id=vehicle_id)
            session.add(engine)
        for field, val in engine_data.model_dump().items():
            setattr(engine, field, val)

        # 2. Dimension Spec
        dim = session.get(DimensionSpec, vehicle_id)
        if not dim:
            dim = DimensionSpec(vehicle_id=vehicle_id)
            session.add(dim)
        for field, val in dimension_data.model_dump().items():
            setattr(dim, field, val)

        # 3. Safety Spec
        safety = session.get(SafetySpec, vehicle_id)
        if not safety:
            safety = SafetySpec(vehicle_id=vehicle_id)
            session.add(safety)
        for field, val in safety_data.model_dump().items():
            setattr(safety, field, val)

        # 4. Feature Spec
        feat = session.get(FeatureSpec, vehicle_id)
        if not feat:
            feat = FeatureSpec(vehicle_id=vehicle_id)
            session.add(feat)
        for field, val in feature_data.model_dump().items():
            setattr(feat, field, val)

        # 5. Ownership Spec
        own = session.get(OwnershipSpec, vehicle_id)
        if not own:
            own = OwnershipSpec(vehicle_id=vehicle_id)
            session.add(own)
        for field, val in ownership_data.model_dump().items():
            setattr(own, field, val)

        # 6. Availability Spec
        avail = session.get(AvailabilitySpec, vehicle_id)
        if not avail:
            avail = AvailabilitySpec(vehicle_id=vehicle_id)
            session.add(avail)
        for field, val in availability_data.model_dump().items():
            setattr(avail, field, val)

        # 7. Environmental Spec
        env = session.get(EnvironmentalSpec, vehicle_id)
        if not env:
            env = EnvironmentalSpec(vehicle_id=vehicle_id)
            session.add(env)
        for field, val in environmental_data.model_dump().items():
            setattr(env, field, val)

        # Flush updates to session
        session.flush()
