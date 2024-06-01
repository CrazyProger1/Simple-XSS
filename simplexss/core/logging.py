import logging.config


def configure_logging(config_file: str):
    logging.config.fileConfig(config_file)
