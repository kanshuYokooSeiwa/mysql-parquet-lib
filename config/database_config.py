class DatabaseConfig:
    def __init__(self, host: str = "", user: str = "", password: str = "", database: str = "") -> None:
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.database: str = database
    
    def to_dict(self) -> dict[str, str]:
        return {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database
        }