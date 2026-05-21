from dataclasses import dataclass


@dataclass
class DBConfig:
    user: str
    password: str
    host: str
    name: str


@dataclass
class CORSConfig:
    allow_origins: list[str]


@dataclass
class Config:
    env: str
    jwt_secret_key: str
    db_cfg: DBConfig
    cors_cfg: CORSConfig

    def get_db_addr(self):
        return f"postgresql://{self.db_cfg.user}:{self.db_cfg.password}@{self.db_cfg.host}:5432/{self.db_cfg.name}"
