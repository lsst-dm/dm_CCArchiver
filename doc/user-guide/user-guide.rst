..
  This is a template for the user-guide documentation that will accompany each CSC.
  This template is provided to ensure that the documentation remains similar in look, feel, and contents to users.
  The headings below are expected to be present for all CSCs, but for many CSCs, additional fields will be required.

  ** All text in square brackets [] must be re-populated accordingly **

  See https://developer.lsst.io/restructuredtext/style.html
  for a guide to reStructuredText writing.

  Use the following syntax for sections:

  Sections
  ========

  and

  Subsections
  -----------

  and

  Subsubsections
  ^^^^^^^^^^^^^^

  To add images, add the image file (png, svg or jpeg preferred) to the
  images/ directory. The reST syntax for adding the image is

  .. figure:: /images/filename.ext
   :name: fig-label

   Caption text.

  Feel free to delete this instructional comment.

.. Fill out data so contacts section below is auto-populated
.. add name and email between the *'s below e.g. *Marie Smith <msmith@lsst.org>*
.. |CSC_developer| replace::  *Stephen R. Pietrowicz <srp@illinois.edu>*
.. |CSC_product_owner| replace:: *Michael Reuter <mareuter@lsst.org>*

.. _User_Guide:

#######################
CCArchiver User Guide
#######################

.. Update links and labels below
.. image:: https://img.shields.io/badge/GitHub-dm_ccarchiver-green.svg
   :target: https://github.com/lsst-dm/dm_CCArchiver
.. image:: https://img.shields.io/badge/Jenkins-dm_CCArchiver-green.svg
   :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/dm_CCArchiver/
.. image:: https://img.shields.io/badge/Jira-dm_ccarchiver-green.svg
   :target: https://jira.lsstcorp.org/issues/?jql=text%20~%20%22CCArchiver%22
.. image:: https://img.shields.io/badge/ts_xml-CCArchiver-green.svg
   :target: https://ts-xml.lsst.io/sal_interfaces/CCArchiver.html


The Archiver interacts with the Archive Controller and the Forwarder to 
coordinate triggering image retrieval and storage. It receives commands 
and events from the SAL DDS messaging system.  This includes commands to 
change state and events from the Camera and Header Service.  

The Archiver also interacts with the Redis key/value store to hold state 
information, and the RabbitMQ broker to send/receive messages from the 
Controller, Forwarder, and Observatory Operations Data Service (OODS).

The Archive Controller handles operations for images. It sets up storage
locations that the Forwarder uses and creates hard links for incoming 
files which are later used by the OODS and the Data Backbone.  The OODS is
a service which maintains a Butler repository for local access.  The Data
Backbone is part of the software service infrastructure that transmits the
data to the LDF.

The Archiver and the Controller each run in their own Docker container.

The user has very little direct interaction with the Archiver, other than 
being able to get it to change states.  The Archiver's activities are 
automatic when it enters the ENABLED state, and no direct user interaction
is required for it to operate.

Usage
=====

The deployment scripts for Archiver processes are located in http://github.com/lsst-dm/dm_iip_deploy

The Archiver services are two separate services, the Archiver CSC service and the Controller.

To start the Archiver service, use the following:

usage: dm_iip_deploy/bin/run_ccarchiver.sh -p [summit|ncsa] -c container_version

example:

dm_iip_deploy/bin/run_ccarchiver.sh -p summit -c 4.1.0_base_3.2.0_c0018

To start the Controller service, use the following:

usage: dm_iip_deploy/bin/run_cccontroller.sh -p [summit|ncsa] -c container_version

example:

dm_iip_deploy/bin/run_cccontroller.sh -p summit -c 4.1.0_base_3.2.0_c0018

dm_iip_deploy/bin/run_cccontroller.sh -p summit -c 4.1.0_base_3.2.0_c0018

The Archiver begins in STANDBY mode when it first starts.

When a "start" command is sent to the Archiver while it is in STANDBY state,
it transitions to the DISABLED state.

When an "enable" command is sent to the Archiver, it transitions from DISABLED
to the ENABLED state.  When the Archiver is in ENABLED state will accept
incoming SAL messages, and will act on them as described in the "Overview"
section.

If the CC Archiver is in the ENABLED state, sending it "disable" will put it
into the DISABLED state.  Once this is done, incoming messages that it had 
previously been listening to will be ignored.

If the CC Archiver is in the DISABLED state, sending it "standby" will put it
into the STANDBY state.

When an "exitControl" command is sent to the Archiver's process while it is in 
STANDBY, and its process will exit.

It can then be restarted using same the procedure:

dm_iip_deploy/bin/run_ccarchiver.sh -p summit -c 4.1.0_base_3.2.0_c0018

Note that the Controller service does not exit when the Archiver is shut down.  That
can be stopped separately, if desired.
