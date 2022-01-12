.. _Configuration_details:

########################
CCArchiver Configuration
########################

The ts_salobj configuration for this CSC is always set to "normal" on START.
It has no real configuration parameters at this level. Most of the configuration
is static, not SAL facing, and is set in a YAML file that is loaded by the CSC.

The CCArchiver is configured using a YAML file. It is loaded from:

 | $IIP_CONFIG_DIR/ccarchiver_config.yaml 

The $IIP_CONFIG_DIR is set on the command line which starts the container.

Our configuration method allows the re-use of the Archiver code between the 
ATArchiver, CCArchiver, and CatchupArchiver.  We do not hard code constant 
values (queue names, hostnames, etc) into the source code, and instead, set 
those values in the YAML file. On initialization, these values are set in the 
CSC. We can vary which service hosts we use, change machines, and change 
message exchange queues without having to change the source code. We can
consolidate most of the work in the main engine, and vary what we need to in 
specialized subclasses and message callbacks.

The following required entries are in the YAML file:

.. code-block:: yaml

    # Example Configuration settings for CCArchiver

    ROOT:

      # host where Redis service is running

      REDIS_HOST: localhost
    
      # Redis database used by ComCam

      ARCHIVER_REDIS_DB: 14
    
      # RabbitMQ queue to send messages to Forwarder

      FORWARDER_PUBLISH_QUEUE: cc_foreman_ack_publish
    
      # RabbitMQ queue to send messages to OODS
      OODS_PUBLISH_QUEUE: cc_publish_to_oods
    
      # RabbitMQ queuea to receive messages from OODS
      OODS_CONSUME_QUEUE: oods_publish_to_cc
    
      # RabbitMQ queue to send messages to Controller
      ARCHIVE_CTRL_PUBLISH_QUEUE: archive_ctrl_publish
    
      # RabbitMQ queue to receiver messages from Controller
      ARCHIVE_CTRL_CONSUME_QUEUE: archive_ctrl_consume
    
      # RabbitMQ queue to receive telemetry
      TELEMETRY_QUEUE: telemetry_queue
    
      # Name of the Camera
      CAMERA_NAME: COMCAM
    
      # Name of the Archiver
      ARCHIVER_NAME: CCArchiver
    
      # Abbreviation of the Archiver
      SHORT_NAME: CC
    
      # Name of the Archive controller
      ARCHIVE_CONTROLLER_NAME: cc_archive_controller
    
      # Redis Archiver association status location
      ASSOCIATION_KEY: ccarchiver_association
    
      # message types
      # Forwarder Health Check Acknowledgement
      FWDR_HEALTH_CHECK_ACK: CC_FWDR_HEALTH_CHECK_ACK
    
      # Request for OODS to ingest a file
      FILE_INGEST_REQUEST: CC_FILE_INGEST_REQUEST
    
      # Message for Controller indicating startIntegration
      NEW_ARCHIVE_ITEM: NEW_CC_ARCHIVE_ITEM
    
      # Message for Forwarder indicating startIntegration
      FWDR_XFER_PARAMS: CC_FWDR_XFER_PARAMS
    
      # Message for Forwarder indicating endReadout
      FWDR_END_READOUT: CC_FWDR_END_READOUT
    
      # Message for Forwarder indicating largeFileObjectAvailable
      FWDR_HEADER_READY: CC_FWDR_HEADER_READY
    
      # message acknowledgement timeout (deprecated)
      ACK_TIMEOUT: 60
    
      # CSC specific
      CSC:
        BEACON:
            # timeout value for beacon
            SECONDS_TO_EXPIRE: 10
    
            # refresh interval to reset timeout value
            SECONDS_TO_UPDATE: 3
    
      # RabbitMQ broker host, port and path
      BASE_BROKER_ADDR: localhost:5672/%2ftest_cc
    
      # Controller information
      ARCHIVE:
        # Archive username
        ARCHIVE_LOGIN: archiver
    
        # Archive hostname
        ARCHIVE_IP: localhost
    
        # checksum type
        CHECKSUM_TYPE: MD5   # Current available options: MD5, CRC-32
    
        # staging directory where files are to be deposited by forwarder
        FORWARDER_STAGING: /data/staging/comcam/forwarder
    
        # staging area for OODS links set by Controller
        OODS_STAGING: /data/staging/comcam/oods
    
        # staging area for Data Backbone links set by Controller
        DBB_STAGING: /data/staging/cc_dbb
    
      # Raft and CCD information to be transmitted in Forwarder requests
      ATS:
        WFS_RAFT: "00"
        WFS_CCD: [ "22/0", "22/1", "22/2" ]
