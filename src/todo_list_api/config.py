from dataclasses import dataclass


@dataclass
class DBConfig:
    user: str
    password: str
    host: str
    name: str


@dataclass
class Config:
    env: str
    db_cfg: DBConfig

    def get_db_addr(self):
        return f"postgresql://{self.db_cfg.user}:{self.db_cfg.password}@{self.db_cfg.host}:5432/{self.db_cfg.name}"
