import logging

logger = logging.getLogger(__name__)

def logger_decorator(func):

    def wrapper(*args, **kwargs):
        logger.info(f"Starting function {func.__name__}. Args: {args}. Kwargs: {kwargs}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception executing function {func.__name__}. Args: {args}. Kwargs: {kwargs}: {e}")
            raise e
        finally:
            logger.info(f"Finishing function {func.__name__}. Args: {args}. Kwargs: {kwargs}")

    return wrapper
