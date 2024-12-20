import json
import logging
import logging.config
from backend.backend import UserDataManager

def main():
    with open('configs/logging_config.json', 'r') as f:
        logging_config = json.load(f)
    logging.config.dictConfig(logging_config)

    user_data_manager = UserDataManager()
    args = user_data_manager.parse_arguments()
    user_data_manager.execute_command(args)

if __name__ == "__main__":
    main()
