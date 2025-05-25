from enum import Enum


class TimeInterval(Enum):
    ZERO_TO_FORTY_NINE = 0
    FIFTY_TO_NINETY_NINE = 1
    HUNDRED_TO_HUNDRED_NINETY_NINE = 2
    TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE = 3
    FIVE_HUNDRED_PLUS = 4

    @classmethod
    def humanize(cls, value: "TimeInterval") -> str:
        match value:
            case TimeInterval.ZERO_TO_FORTY_NINE:
                return "0-49"
            case TimeInterval.FIFTY_TO_NINETY_NINE:
                return "50-99"
            case TimeInterval.HUNDRED_TO_HUNDRED_NINETY_NINE:
                return "100-199"
            case TimeInterval.TWO_HUNDRED_TO_FOUR_HUNDRED_NINETY_NINE:
                return "200-499"
            case TimeInterval.FIVE_HUNDRED_PLUS:
                return "500+"

        raise ValueError(f"Unknown TimeInterval value: {value}")
