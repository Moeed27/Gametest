import logging, datetime, sys

#Logging
logger = logging.getLogger("applog")
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")


#fh = logging.FileHandler(f"logs/applog_{datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.log", mode='w')
#fh.setLevel(logging.ERROR)
#fh.setFormatter(formatter)
#logger.addHandler(fh)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)


logger.setLevel(logging.DEBUG)