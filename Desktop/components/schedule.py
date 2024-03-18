from datetime import datetime, timedelta

class PUCDay:

    day_map: dict = {
    "L": "mon",
    "M": "tue",
    "W": "wed",
    "J": "thu",
    "V": "fri",
    "S": "sat",
    "D": "sun"}

    class PUCBlock:

        def __init__(self, starting: datetime, ending: datetime) -> None:
            self._starts = starting
            self._ends = ending
            self._id = id(self)
            self.holds: list = list()

    def __init__(self, day: str, block_params: dict) -> None:
        self.day_name: str = day
        self.blocks: list[PUCDay.PUCBlock] | tuple[PUCDay.PUCBlock] = []
        self.create_blocks(*block_params.values())

    def create_blocks(self, starting_hour: str, block_duration: int, 
                      break_duration: int, number_of_blocks: int) -> None:
        # Convert the starting_hour string to a datetime object
        current_time = datetime.strptime(starting_hour, "%H:%M")

        for _ in range(number_of_blocks):
            # Calculate the ending time of the block
            end_time = current_time + timedelta(minutes=block_duration)

            # Create a new PUCBlock and add it to the day_crono list
            self.blocks.append(self.PUCBlock(current_time, end_time))

            # Calculate the starting time of the next block
            current_time = end_time + timedelta(minutes=break_duration)

        # Once all blocks are created, turn list into tuple
        self.blocks = tuple(self.blocks)

class PUCWeek:

    def __init__(self, block_params: dict) -> None:
        self.days_crono: dict[str, PUCDay] = {"":None}
        for code in PUCDay.day_map:
            self.days_crono[code] = \
                PUCDay(PUCDay.day_map.get(code), block_params)

    def get_linear_courses(self) -> list:
        """
        Returns a list with all classes of the week in chronological order
        """
        linear_courses = []
        for day in self.days_crono.values():
            for block in day.blocks:
                if block.holds: linear_courses.append(block.holds)
        return linear_courses
    
    def get_linear_blocks(self) -> list:
        """
        Returns a list with all used blocks of the week in chronological order
        """
        linear_courses = []
        for day in self.days_crono.values():
            for block in day.blocks:
                if block.holds: linear_courses.append(block)
        return linear_courses

    def __str__(self) -> str:
        _me: str = ''
        for day in self.days_crono.values():
            _me += day.day_name + '\n' + '-' * 5 + '\n'
            for block in day.blocks:
                if block.holds: _me += block.holds.__str__() + '\n'
                else: _me += 'Vacío\n'
            _me += '\n'
        return _me
    