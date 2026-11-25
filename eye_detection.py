import math
from dataclasses import dataclass


@dataclass(frozen=True)
class EyeObservation:
    state: str
    closed_duration: float
    blink_detected: bool
    drowsy: bool


def eye_aspect_ratio(points, indexes):
    eye_points = [points[index] for index in indexes]
    if not all(math.isfinite(coordinate) for point in eye_points for coordinate in point):
        raise ValueError("Eye landmarks contain invalid coordinates.")

    vertical1 = math.dist(eye_points[1], eye_points[5])
    vertical2 = math.dist(eye_points[2], eye_points[4])
    horizontal = math.dist(eye_points[0], eye_points[3])
    if horizontal <= 1e-6:
        raise ValueError("Eye landmarks have zero horizontal width.")
    return (vertical1 + vertical2) / (2 * horizontal)


class EyeClosureTracker:
    def __init__(
        self,
        close_threshold,
        open_threshold,
        drowsiness_seconds,
        blink_min_seconds,
        blink_max_seconds,
        confirmation_frames,
    ):
        self.close_threshold = close_threshold
        self.open_threshold = open_threshold
        self.drowsiness_seconds = drowsiness_seconds
        self.blink_min_seconds = blink_min_seconds
        self.blink_max_seconds = blink_max_seconds
        self.confirmation_frames = confirmation_frames
        self.reset()

    def reset(self):
        self.closed_since = None
        self.closed_frames = 0
        self.is_closed = False

    def update(self, left_ear, right_ear, now):
        if not math.isfinite(left_ear) or not math.isfinite(right_ear):
            self.reset()
            return EyeObservation("UNKNOWN", 0.0, False, False)

        average_ear = (left_ear + right_ear) / 2
        if self.is_closed:
            duration = max(0.0, now - self.closed_since)
            if average_ear >= self.open_threshold:
                blink = (
                    self.blink_min_seconds <= duration <= self.blink_max_seconds
                    and duration < self.drowsiness_seconds
                )
                self.reset()
                return EyeObservation("OPEN", duration, blink, False)
            return EyeObservation(
                "CLOSED",
                duration,
                False,
                duration >= self.drowsiness_seconds,
            )

        both_eyes_closed = (
            left_ear < self.close_threshold and right_ear < self.close_threshold
        )
        if both_eyes_closed:
            if self.closed_since is None:
                self.closed_since = now
            self.closed_frames += 1
            duration = max(0.0, now - self.closed_since)
            if self.closed_frames >= self.confirmation_frames:
                self.is_closed = True
                return EyeObservation(
                    "CLOSED",
                    duration,
                    False,
                    duration >= self.drowsiness_seconds,
                )
            return EyeObservation("CLOSING", duration, False, False)

        self.reset()
        return EyeObservation("OPEN", 0.0, False, False)
