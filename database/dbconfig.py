import os

import sshtunnel
from flask_sqlalchemy import SQLAlchemy
from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError
from logconfig import logger

class Database:
    #Private method to open an ssh tunnel to the server defined in .env
    #Returns pointer to the tunnel
    @staticmethod
    def start_tunnel():
        #create an ssh tunnel
        logger.info(f"attempting tunnel start to default server configuration")
        try:
            tunnel = SSHTunnelForwarder(
                (os.getenv('SSH_HOST'), int(os.getenv('SSH_PORT'))), #SSH Server details
                ssh_username=os.getenv('SSH_USER'),
                ssh_pkey=os.getenv('SSH_KEYPATH'),
                remote_bind_address=(os.getenv('DB_HOST'), int(os.getenv('DB_PORT'))), #The destination server details
                local_bind_address=('localhost', 0) #The address where packets are sent to be forwarded to remote address
            )
            tunnel.start()
            logger.info(f"tunnel started on {tunnel.local_bind_address}")
        except sshtunnel.BaseSSHTunnelForwarderError as e:
            logger.warn(f"failed to establish tunnel connection on default configuration - unable to connect ({e})")
            logger.info("attempting tunnel start to backup server configuration")
            try:
                tunnel = SSHTunnelForwarder(
                    (os.getenv('SSH_HOST_BACKUP'), int(os.getenv('SSH_PORT'))), #SSH Server details
                    ssh_username=os.getenv('SSH_USER'),
                    ssh_pkey=os.getenv('SSH_KEYPATH'),
                    remote_bind_address=(os.getenv('DB_HOST'), int(os.getenv('DB_PORT'))), #The destination server details
                    local_bind_address=('localhost', 0) #The address where packets are sent to be forwarded to remote address
                )
                tunnel.start()
                logger.info(f"tunnel started on backup on {tunnel.local_bind_address}")
                logger.warn("(a long list of errors might have just appeared in your log - please ignore these, they have been handled.)")
                logger.warn(f"tunnel is established on backup; please alert db admin if this persists.")
            except sshtunnel.BaseSSHTunnelForwarderError as e:
                logger.critical(f"failed to establish tunnel connection on backup configuration - unable to connect ({e})")
                logger.critical("critical failure in database server connection; unable to connect to bastion server. please contact db admin.")
                raise Exception("Could not establish connection to db bastion server")
        except ValueError as e:
            logger.critical(f"failed to establish tunnel connection - invalid values ({e})")
            logger.critical("note: this issue can occur when .env is not up-to-date or has incorrect values. please check this before reporting this error")
            logger.critical("critical failure in database server connection")
            raise e

        return tunnel

    #Closes a connection to the given tunnel
    @staticmethod
    def stop_tunnel(tunnel):
        try:
            if tunnel.tunnel_is_up:
                logger.info(f"stopping tunnel on {tunnel.local_bind_address}")
                tunnel.stop()
                logger.info("tunnel stopped")
        except BaseSSHTunnelForwarderError as e:
            logger.info(f"tunnel failed to stop; {e}")
            pass

    #Runs database setup for a given flask app
    #Returns the constructed database object (db)
    @staticmethod
    def setup(app, tunnel, testing=False):
        #Setup database

        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        host = 'localhost'
        port = tunnel.local_bind_port
        dbname = os.getenv('DB_NAME')

        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
        db = SQLAlchemy(app)
        #with app.app_context():
            #db.reflect()
        logger.info(f'{"test "*testing}db connection to "{dbname}" setup success')
        return db

#TODO: Fix random timeout error - (backup bastion server?)
