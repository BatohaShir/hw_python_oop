class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            f"Тип тренировки: {self.training_type};"
            f" Длительность: {self.duration} ч.;"
            f" Дистанция: {self.distance:0.3f} км;"
            f" Ср. скорость: {self.speed:0.3f} км/ч;"
            f" Потрачено ккал: {self.calories:0.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    HEIGHT_IN_METRE = 100

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Базовый класс тренировки"""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_CALORIE_1 * self.get_mean_speed() - self.COEFF_CALORIE_2)
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_HOUR)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            self.COEFF_CALORIE_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.COEFF_CALORIE_2
            * self.weight
        ) * (self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2.0

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        lenght_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trening_matching = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return trening_matching[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    return None


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
