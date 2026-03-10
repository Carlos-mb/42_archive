from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def safety_rules(self) -> "SpaceMission":
        errors: list[str] = []
        # 1) Mission ID must start with "M"
        if not self.mission_id.startswith("M"):
            errors.append('Mission ID must start with "M"')

        # 2) Must have at least one Commander or Captain
        ok: bool = False
        for person in self.crew:
            if person.rank == Rank.captain or person.rank == Rank.commander:
                ok = True
                break
        if not ok:
            errors.append(
                "Mission must have at least one Commander or Captain")

        # 3) Long missions (> 365 days) need 50% experienced crew (5+ years)
        if self.duration_days > 365:
            experienced = sum(1 for m in self.crew if m.years_experience >= 5)
            if experienced < len(self.crew) / 2:
                errors.append(
                    "Long missions need at least 50% "
                    "experienced crew (5+ years)")

        # 4) All crew members must be active
        if not all(person.is_active for person in self.crew):
            errors.append("All crew members must be active")

        if len(errors) > 0:
            raise ValueError("; ".join(errors))
            # To create a list of errors:
            # raise ValidationError.from_exception_data(
            #                                 title=self.__class__.__name__,line_errors=error_list)

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        mission_ok = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C01",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=40,
                    specialization="Mission Command",
                    years_experience=10,
                ),
                CrewMember(
                    member_id="C02",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=6,
                ),
                CrewMember(
                    member_id="C03",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=45,
                    specialization="Engineering",
                    years_experience=6,
                )
            ],
        )
        print("Valid mission created:")
        print(f"Mission: {mission_ok.mission_name}")
        print(f"ID: {mission_ok.mission_id}")
        print(f"Destination: {mission_ok.destination}")
        print(f"Duration: {mission_ok.duration_days} days")
        print(f"Budget: ${mission_ok.budget_millions}M")
        print(f"Crew size: {len(mission_ok.crew)}")
        for person in mission_ok.crew:
            print(f"-{person.name} ({person.rank.value}) -"
                  f" {person.specialization}")
        print()
    except ValidationError as e:
        print(e)

    print("=" * 45)

    try:
        SpaceMission(
            mission_id="BAD_01",
            mission_name="Test Mission",
            destination="Home",
            launch_date=datetime.now(),
            duration_days=-1,
            budget_millions=-1,
            crew=[
                CrewMember(
                    member_id="C03",
                    name="Alien 8th passanger",
                    rank=Rank.cadet,
                    age=30,
                    specialization="Engineering",
                    years_experience=3,
                )
            ],
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])

    print("=" * 45)
    try:
        SpaceMission(
            mission_id="BAD_01",
            mission_name="Test Mission",
            destination="Home",
            launch_date=datetime.now(),
            duration_days=10,
            budget_millions=10,
            crew=[
                CrewMember(
                    member_id="C03",
                    name="Alien 8th passanger",
                    rank=Rank.cadet,
                    age=30,
                    specialization="Engineering",
                    years_experience=3,
                )
            ],
        )
    except ValidationError as e:
        print("Expected validation error in model_validator:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
