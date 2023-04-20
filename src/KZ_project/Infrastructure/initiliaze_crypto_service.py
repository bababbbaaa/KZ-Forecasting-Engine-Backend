from KZ_project.Infrastructure import config
from KZ_project.core.adapters.crypto_repository import CryptoRepository
from KZ_project.core.adapters.forecastmodel_repository import ForecastModelRepository
from KZ_project.ml_pipeline.ai_model_creator.model_engine import ModelEngine
from KZ_project.ml_pipeline.data_generator.data_manipulation import DataManipulation
from KZ_project.ml_pipeline.services.twitter_service.tweet_sentiment_analyzer import TweetSentimentAnalyzer
from KZ_project.webapi.services import services
from KZ_project.Infrastructure.orm_mapper import orm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#orm.start_mappers()
engine = create_engine(config.get_postgres_uri())
get_session = sessionmaker(bind=engine)
#orm.metadata.create_all(engine)

coin_list = config.config_coin_list

def add_cryptos(crypto):
    session = get_session()
    repo = CryptoRepository(session)
    try:
        services.add_crypto(
                crypto.SYMBOL_NAME.lower(),  # because the check argument name for error is always lowercase
                crypto.SYMBOL_CUT,
                crypto.description,
                repo,
                session
        )
    except (services.InvalidName) as e:
        return f"errors: {e}"
    return f"Succes for {crypto.SYMBOL_NAME}"
            
def create_all_models_2hourly(asset_config):
    tsa = TweetSentimentAnalyzer()
    
    
    data = DataManipulation(asset_config.SYMBOL, asset_config.source, 
                        asset_config.range_list, start_date=asset_config.start_date, 
                        end_date=asset_config.end_date, interval=asset_config.interval, scale=asset_config.SCALE, 
                        prefix_path='.', saved_to_csv=False,
                        logger=asset_config.logger, client=asset_config.client)
    df_price = data.df.copy()
    
    model_engine = ModelEngine(asset_config.SYMBOL, asset_config.SYMBOL_CUT, asset_config.source, asset_config.interval_model)
    
    model_engine.start_model_engine(data, tsa, asset_config.tweet_file_hourly)
        
if __name__ == '__main__':
    #for i in coin_list:
     #   create_all_models_2hourly(i)
        #print(res)
    session = get_session()
    repo = ForecastModelRepository(session)
    print(f'deneme forecast: ')
    try:
        fm_model = services.get_forecast_model(
                            "BNBUSDT", 
                            "1h",
                            "XgboostForecaster",
                            repo,
                            session
                            )
    except Exception as e:
        print(f'errors occured frmodel: {e}')
    print(f'son test {type(repo.__class__.__name__)}')
        
    




