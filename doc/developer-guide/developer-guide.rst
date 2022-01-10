.. _Developer_Guide:

#########################################
CCArchiver Developer Guide
#########################################

.. Update these labels and links
.. image:: https://img.shields.io/badge/GitHub-dm_CCArchiver-green.svg
    :target: https://github.com/lsst-ts/dm_CCArchiver
.. image:: https://img.shields.io/badge/Jenkins-dm_CCArchiver-green.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/dm_CCArchiver/
.. image:: https://img.shields.io/badge/Jira-dm_CCArchiver-green.svg
    :target: https://jira.lsstcorp.org/issues/?jql=text%20~%20%22CCArchiver%22
.. image:: https://img.shields.io/badge/ts_xml-CCArchiver-green.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/CCArchiver.html


Introduction
============

The primary services that the CCArchiver interacts with are the Forwarder 
(dm_Forwarder) and the ComCam Controller.  The Forwarder retrieves and assembles
images. The ComCam Controller presents where files should be deposited and
stages files where the `Data Backbone <https://dmtn-122.lsst.io>` (DBB) and 
the ComCam `Observatory Operations Data Service <https://github.com/lsst-dm/ctrl_oods>` (OODS)
can act on them.  These services communicate to each other using RabbitMQ.  A Redis
database is also used to advertise service availablity and service health.

The archiver begins in the STANDBY state. When it receives a START command,
it transitions to the DISABLED state.  This causes the CCArchiver to attempt
to pair with an available Forwarder service through a Redis database. It also
establishes connections to a RabbitMQ server. After the archiver is brought to
the ENABLED state, it is ready to receive messages.

When the "startIntegration" message is received, the CCArchiver sends a
message to the ComCam Controller, informing it that a new archive image will
arrive soon.  In the controller’s response is the target directory for where
the image is supposed to be deposited by the forwarder. This target directory
changes over time because it incorporates the current date. The target 
directory is then sent in a message to the Forwarder, which sends back an 
acknowledgment that the message was received.

When the "endReadout" message is received, the CCArchiver sends the message to
the Forwarder, which sends back an acknowledgment that the message was
received.

When the "largeFileObjectAvailable" is received indicating that the header is
available from the HeaderService, the CCArchiver sends the message to the
Forwarder, which sends back an acknowledgment that the message was received.

When the telemetry message "IMAGE_RETRIEVAL_FOR_ARCHIVING" message is received
via RabbitMQ from the ComCam Controller, the CCArchiver translates this into the
"imageRetrievalForArchiving" event and publishes it via SAL.

Note that "IMAGE_RETRIEVAL_FOR_ARCHIVING" indicates that the Forwarder has
contacted the ComCam Controller and told it that it has finished writing
the file.  The ComCam Controller links data to the staging area of the DBB
and the ComCam OODS. Additionally, the Controller sends a message to the
ComCam OODS that it can ingest the file that was written.  The ComCam OODS
ingests the images into the Butler repository and issues a RabbitMQ
message to the ComCam Archiver about the status of the file ingestion.

When the message "CC_FILE_INGEST_REQUEST" is received from the ComCam OODS,
the ComCam Archiver translates that messages and transmits the status of the
Butler file ingestion as an "imageInOODS" event published to SAL.

Internal Operation
==================

This section describes the interaction between the Archiver, Controller, and 
Forwarder. Actions the Forwarder takes after receiving messages are outlined
in the Forwarder's documentation.

The Archiver begins in the STANDBY state. When it receives a START command, it
transitions to the DISABLED state, establishes connections to a RabbitMQ 
server, and queries the Redis keystore to find an available Forwarder service
to pair with.  

If no Forwarder service is available, the Archiver transitions to a FAULT
state.  If the Forwarder detects that the Archiver is no longer available, it
re-adds itself to the available Forwarder list in the Redis keystore.

After the Archiver receives an ENABLE command, it is ready to receive SAL 
messages.

When the "startIntegration" SAL message is received, the Archiver sends a 
message to the Controller, informing it that a new archive image will arrive 
soon.  The Controller sends a response with the user name, hostname, and
target directory where the image should be deposited by the Forwarder.  (This
target directory changes over time). This information is then sent in a 
message to the Forwarder, which sends back an acknowledgment that the message 
was received.

When the "endReadout" SAL message is received, the Archiver sends the message
to the Forwarder, which sends back an acknowledgment that the message was 
received.

When the "largeFileObjectAvailable" SAL message is received indicating that
the header is available from the HeaderService, the Archiver sends the message
to the Forwarder, which sends back an acknowledgment that the message was 
received.

Once the Forwarder has written a file to its data store, it sends a message to
the Controller indicating that it has finished and the file can be acted upon.
The Controller links the image file to the staging areas of the Data Backbone
and the OODS. The Controller sends a message to the OODS to indicate the file
can now be acted upon. 

The OODS then ingests the file into the Butler repository and issues a 
RabbitMQ message to the Archiver about the status of the file ingestion. If
the ingest fails, failure status is indicated with a description of what
happened, and that information is transmitted to the Archiver.  The Archiver
does not transition to a FAULT state in this case because there was no failure
in the Archiver. The response from the OODS that an attempt to ingest 
failed may have occurred for any number reason and it reports that reason
to the best of its ability.  Subsequent ingest attempts can still succeed, so
the OODS continues to operate.

When the message is received from the OODS, the Archiver transmits the status 
of the Butler file ingestion via SAL as an Archiver event.

Service Status
==============
When the Archiver and Forwarder services are paired, they must each be able to 
detect when the other service is no longer active to indicate a problem
exists. This section describes the mechanism used to accomplish this.
 
We take advantage of a feature in Redis that allows us to have a value set 
with a timeout. The timeout counts down from the time a value is set. If the
timeout expires before the value has been updated, Redis will automatically
remove this value. When the service updates a value with a timeout, it resets
that timeout. If the service goes away, nothing updates the "aliveness" state,
the timeout expires, and the entry is removed. A service is set to continuously
update the value and timeout at regular intervals, which shows they are still 
active.
 
Both the Archiver and Forwarder post status information about their own 
"aliveness" states.

When the Forwarder starts, it adds itself to a Redis database indicating that
it is available for pairing. When the Archiver goes to the DISABLED state, it
looks for available Forwarders, removes one from the Forwarder list, and sends
that Forwarder an association request via RabbitMQ messaging. The association
request includes the Archiver's service status Redis entry. The Forwarder
notes the Archiver's service status location and responds with its service
status location. At this point, the Archiver knows where to look for the
Forwarder's status, and the Forwarder knows where to look for the Archiver's
status.
 
Each service looks at the other services' status at regular intervals. If the 
"aliveness" status is no longer available, the service assumes the other side
has failed. If the Forwarder detects the CC Archiver failed, it adds itself to
the available Forwarder list in Redis. If the CC Archiver detects the 
Forwarder is no longer updating its status, it transitions to a FAULT state.
 
Note the service updates its value with a timeout at a much more frequent
interval than the timeout itself. For example, the Archiver updates its own 
status every three seconds, with a timeout value of ten seconds. Additionally,
since this is an atomic operation, one service can't read the value when 
another service is updating that same value. The Forwarder can look as 
frequently (or infrequently) as it wants, and the Archiver's status will be
there, as long as the Archiver is alive to update the value.
 
This has advantages over the traditional "message/ack" heartbeat mechanism. 
Heartbeats between services require a continuous exchange of messages between
those two services. If there is more than one service that needs to be 
interacted with, heartbeats would need to be sent to each service, generating
more network traffic. Delays in sending a message can cause false indications 
of failure when none exists.
 
In our method, multiple clients observe the value of status entries, even
employ external monitoring services. This requires no service code changes; 
external monitoring only has to look at the location of the service "aliveness"
status, and the service itself doesn't need to know anything about this. 
Additional services can be deployed, watch the services they depend on, and no
code changes need to be made to the initial service.
 
The initial exchange of where the Archiver service and Forwarder service give
each other the "well known" service status location is deliberate. Multiple 
Forwarders (as a backup) can be deployed, each with its status location. The 
Forwarder can be paired with either AuxTel or ComCam but doesn't know which 
until its initial contact.
 


.. _Dependencies:

Dependencies
============

[This section should list dependencies in bullet form]

* cycle_tag - c0023
* ts_ddsconfig - v0.9.0
* OpenSplice DDS - V6.10.4
* dm_csc_base - 4.2.0
* dm_CCarchiver - 3.1.0
* pika - 1.1.0
* redis - 3.5.3


.. Linking to the previous versions may also be worthwhile, depending on the CSC

.. _API:

CCArchiver API
=============================

The content in this section is autogenerated from docstrings.

.. The code below should insert the docstrings from the code.

.. automodapi:: lsst.dm.CCArchiver
    :no-main-docstr:
    :no-inheritance-diagram:


.. _Build:

Building and Running
====================

The CC Archiver and CC Controller services each run in a container.

The file dm_iip_deploy/docker/versions.sh contains all version numbers of all 
CSC components.

This includes: ts_salobj, ts_idl, ts_xml, ts_sal, OpenSplice, the DDS version 
derived from OpenSplice, Archiver CSC versions, and the dm_csc_base.  
(We also use this to build the OODS, and that information is included as well.

The Archiver and dm_csc_base versions are listed as "tags/version" (ie, 
"tags/2.1.0"), which is a reference to the release version in the Github 
repository.  When development packages are tested, you can specify 
"tickets/ticket-number" (ie, "tickets/DM-26157").

These version numbers are used to tag the containers that are being built. 
While lengthy, it allows for easy identification of which versions of the 
software were used to build the container.

To build:

1) Download a copy of the repository:

  | $ git clone http://github.com/lsst-dm/dm_iip_deploy

2) Execute the following:

  | $ cd dm_iip_deploy/docker
  | $ . ./versions.sh
  | $ docker-compose build base ccbase ccarchiver cccontroller

We supply a build script, dm_iip_deploy/docker/build.sh, which will build all containers.

Running the containers

The Forwarder and Archive Controller are set up to be the same user (The 
ARCHIVE_LOGIN user, stated in the configuration).   The Controller hard-links 
the files once they are written by the Forwarder to a void copying them.

To run the containers, download the dm_iip_deploy repository:

 | $ git clone http://github.com/lsst-dm/dm_iip_deploy

Note the version number of the containers:

Execute the following:

 | $ docker images | grep cc
 | lsstts/cccontroller  1.2.0_ts_salobj_5.17.0_ts_idl_1.3.0_6.1.0_4.1.4  b24179345b6d  10 seconds ago  2.15GB
 | lsstts/ccarchiver    1.2.0_ts_salobj_5.17.0_ts_idl_1.3.0_6.1.0_4.1.4  3e1fe6cb2baa  10 seconds ago  2.15GB
 | lsstts/ccbase        2.2.0_ts_salobj_5.17.0_ts_idl_1.3.0_6.1.0_4.1.4  aa3e0406e4c1  10 seconds ago  2.15GB


There are shell scripts provided to execute the containers.

The CCArchiver container script requires three arguments:  

1) The site name (ncsa or base)

2) The version number of the container image

3) The network on which SAL traffic runs

To run the CC Archiver container, execute the following:

 | $ cd dm_iip_deploy
 | ./bin/run_ccarchiver.sh ncsa 1.2.0_ts_salobj_5.17.0_ts_idl_1.3.0_6.1.0_4.1.4 141.142.238.15

The CCController container script requires two arguments

1) The site name (ncsa or base)

2) The version number of the container image

To run the CC Controller containers, execute the following:

 | $ cd dm_iip_deploy
 | $ ./bin/run_cccontroller.sh ncsa 1.2.0_ts_salobj_5.17.0_ts_idl_1.3.0_6.1.0_4.1.4

.. _Documentation:

Building the Documentation
==========================

[This section is to walk the developer through building the documentation. This should be a step-by-step process as it will most likely be used by non-developers as well who wish to edit the docs]

.. _Contributing:

Contributing
============

Code and documentation contributions utilize pull-requests on github.
Feature requests can be made by filing a Jira ticket with the `CCArchiver` label.
In all cases, reaching out to the :ref:`contacts for this CSC <Contact_Personnel>` is recommended.

