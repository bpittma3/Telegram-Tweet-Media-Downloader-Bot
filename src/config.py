import os, logging

class Config:
    def __init__(self) -> None:
        rawLogLevel: str|None = os.environ.get("LOG_LEVEL")

        match rawLogLevel:
            case str(x):
                match x.lower():
                    case "debug":
                        self.logLevel = logging.DEBUG
                        self.printLogLevel(x)
                    case "info":
                        self.logLevel = logging.INFO
                        self.printLogLevel(x)
                    case "warn" | "warning":
                        self.logLevel = logging.WARN
                        self.printLogLevel(x)
                    case "error" | "err":
                        self.logLevel = logging.ERROR
                        self.printLogLevel(x)
                    case "critical" | "crit":
                        self.logLevel = logging.CRITICAL
                        self.printLogLevel(x)
                    case _:
                        self.logLevel = logging.INFO
                        self.printLogLevel("info")
            case _:
                # The default log level if couldn't find/parse the env variable
                self.logLevel = logging.INFO
                self.printLogLevel("info")
    
    def printLogLevel(self, level: str) -> None:
        print(f"Using logger with min log level of {level.upper()}")


    def loadEnvVars(self) -> None:
        # Load environment variables
        logging.debug("Getting ALLOWED_IDS environment variable")
        rawAllowedIds: str|None = os.environ.get("ALLOWED_IDS")
        logging.debug("Getting T_TOKEN environment variable")
        rawToken: str|None = os.environ.get("T_TOKEN")

        # Filter the ID list to only those which are digits, then convert those into ints
        logging.info("Parsing ALLOWED_IDS list")
        if rawAllowedIds != None:
            self.allowedIds: list = list(map(lambda x: int(x), list(filter(lambda x: str.isdigit(x), rawAllowedIds.split(',')))))
            logging.debug("ALLOWED_IDS list parse successful")
        else:
            self.allowedIds: list = []
            logging.warn("ALLOWED_IDS list parse couldn't find any IDS, not allowing anyone to talk to the bot for security")
        
        logging.info("Parsing Telegram token")
        if type(rawToken) == str:
            self.tToken: str = str(rawToken)
            logging.debug("Token parse successful")
        else:
            logging.error("Token parse found empty token, Telegram will reject this bot")
            self.tToken: str = ""