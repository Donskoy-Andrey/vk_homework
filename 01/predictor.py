class SomeModel:
    def predict(self, message: str) -> float:
        return ((len(message) / 2) + (len(message) % 3) - 0.7) / 10


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"
    return "норм"
