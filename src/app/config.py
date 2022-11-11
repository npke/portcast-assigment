from starlette import config

env_config = config.Config(".env")


class Config:
    NUMBER_OF_SENTENCES_PER_PARAGRAPH = 50
    TOP_WORDS_TO_RETURN_IN_DICTIONARY = 10
    METAPHORPSUM_API_URL = "http://metaphorpsum.com"
    ELASTICSEARCH_HOST = env_config("ELASTICSEARCH_HOST")
    ELASTICSEARCH_USERNAME = env_config("ELASTICSEARCH_USERNAME")
    ELASTICSEARCH_PASSWORD = env_config("ELASTICSEARCH_PASSWORD")
    ELASTICSEARCH_PARAGRAPHS_INDEX = "paragraphs"
    ELASTICSEARCH_WORDS_INDEX = "words"
    DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"


config = Config()
