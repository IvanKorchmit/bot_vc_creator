class ActiveChannels:
    def __init__(self, guild : int) -> None:
        self.active_channels : list[int]
        self.active_channels = []

        self.guild : int
        self.guild = guild


    def __str__(self) -> str:
        return f"{self.active_channels}, {self.guild}"
class CustomOptions:
    def __init__(self, guild, vc, category) -> None:
        self.guild = guild
        self.vc = vc
        self.category = category