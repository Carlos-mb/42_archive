from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.telepathic and \
                self.witness_count < 3:
            raise ValueError("Telepathic contact "
                             "requires at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) "
                             "should include received messages")

        return self


def main() -> None:

    print("Alien Contact Log Validation")
    print("=" * 40)

    try:
        contact1 = AlienContact(
            contact_id="AC_CNT_01",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received='Greetings from Zeta Reticuli'
        )
        print("Valid contact report:")
        print(f"ID: {contact1.contact_id}")
        print(f"Type: {contact1.contact_type}")
        print(f"Location: {contact1.location}")
        print(f"Signal: {contact1.signal_strength}/10")
        print(f"Duration: {contact1.duration_minutes} minutes")
        print(f"Witnesses: {contact1.witness_count}")
        print(f"Message: {contact1.message_received!r}")
    except ValidationError as e:
        print(e)

    print("")
    print("=" * 40)

    try:
        contact1 = AlienContact(
            contact_id="AC_CNT_01",
            timestamp=datetime.now(),
            location="Madrid",
            contact_type=ContactType.telepathic,
            signal_strength=0,
            duration_minutes=500,
            witness_count=1
        )
        print("Valid contact report:")
        print(f"ID: {contact1.contact_id}")
        print(f"Type: {contact1.contact_type}")
        print(f"Location: {contact1.location}")
        print(f"Signal: {contact1.signal_strength}/10")
        print(f"Duration: {contact1.duration_minutes} minutes")
        print(f"Witnesses: {contact1.witness_count}")
        print(f"Message: {contact1.message_received}")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
