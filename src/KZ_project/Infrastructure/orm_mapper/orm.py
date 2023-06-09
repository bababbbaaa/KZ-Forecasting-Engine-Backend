from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, registry
from sqlalchemy.sql import func

from KZ_project.core.domain.tracker import Tracker
from KZ_project.core.domain.asset import Asset
from KZ_project.core.domain.aimodel import AIModel
from KZ_project.core.domain.crypto import Crypto
from KZ_project.core.domain.forecast_model import ForecastModel
from KZ_project.core.domain.signal_tracker import SignalTracker

mapper_registry = registry()

metadata = MetaData()

assets = Table(
    "assets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("source", String(100))
    
)

aimodels = Table(
    "aimodels",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("source", String(100)),
    Column("feature_counts", Integer),
    Column("model_name", String(500)),
    Column("ai_type", String(200)),
    Column("hashtag", String(100), nullable=True),
    Column("accuracy_score", Float()),
    Column("created_at", DateTime())
)


trackers = Table(
    "trackers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("datetime_t", String(200)),
    Column("position", Integer, nullable=False),
    Column("created_at", DateTime())
)

allocations_tracker = Table(
    "allocations_tracker",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tracker_id", ForeignKey("trackers.id")),
    Column("asset_id", ForeignKey("assets.id")),
)

cryptos = Table(
    "cryptos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), unique=True),
    Column("ticker", String(25)),
    Column("description", String(500))
)

forecast_models = Table(
    "forecast_models",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("source", String(100)),
    Column("feature_counts", Integer),
    Column("model_name", String(500)),
    Column("interval", String(10)),
    Column("ai_type", String(200)),
    Column("hashtag", String(100), nullable=True),
    Column("accuracy_score", Float()),
    Column("crypto_id", ForeignKey("cryptos.id")),
    Column("created_at", DateTime())

)

signal_trackers = Table(
    "signal_trackers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("datetime_t", String(200)),
    Column("signal", Integer, nullable=False),
    Column("ticker", String(25)),
    Column("tweet_counts", Integer),
    Column("forecast_model_id", ForeignKey("forecast_models.id")),
    Column("created_at", DateTime())
    
)



def start_mappers():
    lines_mapper_tracker = mapper_registry.map_imperatively(
        Tracker, trackers
    )
    
    mapper_registry.map_imperatively(
        Asset, 
        assets,
         properties={
            "_allocations_tracker": relationship(
                lines_mapper_tracker, secondary=allocations_tracker, collection_class=set,
            )
        },
    )
    
    mapper_registry.map_imperatively(
        AIModel, aimodels
    )
    
    
    crypto_mapper = mapper_registry.map_imperatively(Crypto, cryptos)
    forecast_model_mapper = mapper_registry.map_imperatively(ForecastModel, forecast_models, 
                                   properties={
                                       'crypto': relationship(crypto_mapper)
                                   })
    mapper_registry.map_imperatively(SignalTracker, signal_trackers,
           properties={
               'forecast_model': relationship(forecast_model_mapper)
           })

    
    """
        mapper_registry.map_imperatively(
        AIModel,
        aimodels,
        properties={
            "tracker": relationship(
                Tracker,
                backref="aimodel",
                uselist=False
            )
        },
    )
    
    

    
    
        mapper_registry.map_imperatively(
        AIModel,
        aimodels,
        properties={
            "allocations_tracker": relationship(
                Tracker,
                secondary=allocations_tracker,
                backref="aimodels",
                collection_class=set,
            )
        },
    )

    # Define foreign key constraints
    allocations_tracker.append_constraint(
        ForeignKeyConstraint(["ai_model_id"], ["aimodels.id"])
    )
    """