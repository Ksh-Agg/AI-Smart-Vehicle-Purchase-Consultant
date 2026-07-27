"""Vehicle loader component."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.vehicle import Vehicle
from app.etl.models.vehicle import CanonicalVehicle


class VehicleLoader:
    """Handles checking and inserting Vehicle ORM records."""

    def load_vehicle(
        self, session: Session, vehicle_data: CanonicalVehicle, brand_id: int
    ) -> tuple[Vehicle, bool]:
        """Looks up a Vehicle by the uniqueness constraint (brand_id, model, variant, year).

        If it exists, returns the existing Vehicle. Otherwise, creates and returns a new Vehicle record.

        Returns:
            A tuple of (Vehicle ORM instance, created_bool).
        """
        model_name = vehicle_data.model.strip()
        variant_name = vehicle_data.variant.strip()

        stmt = select(Vehicle).where(
            Vehicle.brand_id == brand_id,
            Vehicle.model.ilike(model_name),
            Vehicle.variant.ilike(variant_name),
            Vehicle.year == vehicle_data.year,
        )
        existing_vehicle = session.execute(stmt).scalar_one_or_none()

        if existing_vehicle:
            # Vehicle already exists. Update its fields with latest spec mapping
            existing_vehicle.body_type = vehicle_data.body_type
            existing_vehicle.segment = vehicle_data.segment
            existing_vehicle.fuel_type = vehicle_data.fuel_type
            existing_vehicle.transmission = vehicle_data.transmission
            existing_vehicle.drivetrain = vehicle_data.drivetrain
            existing_vehicle.seating_capacity = vehicle_data.seating_capacity
            existing_vehicle.doors = vehicle_data.doors
            existing_vehicle.price_ex_showroom = vehicle_data.price_ex_showroom
            existing_vehicle.price_on_road = vehicle_data.price_on_road
            session.flush()
            return existing_vehicle, False

        # Create new Vehicle
        new_vehicle = Vehicle(
            brand_id=brand_id,
            model=model_name,
            variant=variant_name,
            year=vehicle_data.year,
            body_type=vehicle_data.body_type,
            segment=vehicle_data.segment,
            fuel_type=vehicle_data.fuel_type,
            transmission=vehicle_data.transmission,
            drivetrain=vehicle_data.drivetrain,
            seating_capacity=vehicle_data.seating_capacity,
            doors=vehicle_data.doors,
            price_ex_showroom=vehicle_data.price_ex_showroom,
            price_on_road=vehicle_data.price_on_road,
        )
        session.add(new_vehicle)
        session.flush()  # Populates new_vehicle.id for spec FK constraints

        return new_vehicle, True
