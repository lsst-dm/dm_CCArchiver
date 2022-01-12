..
  This is a template for documentation that will accompany each CSC.
  It consists of a user guide and development guide, however, cross linking between the guides is expected.
  This template is provided to ensure that the documentation remains similar in look, feel, and contents to users.
  The headings below are expected to be present for all CSCs, but for many CSCs, additional fields will be required.
  An example case can be found at https://ts-athexapod.lsst.io/v/develop/

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
.. |CSC_developer| replace::  *Stephen R Pietrowicz <srp@illinois.edu>*
.. |CSC_product_owner| replace:: *Michael Reuter <mareuter@lsst.org>*

.. Note that the "ts_" prefix is omitted from the title

#########################
CCArchiver
#########################

.. update the following links to point to your CSC (rather than the athexapod)
.. image:: https://img.shields.io/badge/GitHub-dm_CCArchiver-green.svg
    :target: https://github.com/lsst-dm/dm_CCArchiver
.. image:: https://img.shields.io/badge/Jenkins-dm_CCArchiver-green.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/dm_CCArchiver/
.. image:: https://img.shields.io/badge/Jira-dm_CCArchiver-green.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+dm_CCArchiver
.. image:: https://img.shields.io/badge/ts_xml-dm_CCArchiver-green.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/CCArchiver.html

.. _Overview:

Overview
========

The Data Management CCArchiver coordinates Commissioning Camera 
archiving activities for the Vera C. Rubin Observatory.  This service 
interacts with other services coordinate retrieval and archival of
image data from the ComCam data acquisition system.

The primary services that the CCArchiver interacts with are the Forwarder
and the ComCam Controller.  The Forwarder retrieves and assembles
images. The ComCam Controller presents where files should be deposited and
stages files where the `Data Backbone https://dmtn-122.lsst.io` (DBB) and
the ComCam `Observatory Operations Data Service https://github.com/lsst-dm/ctrl_oods` (OODS) can act on them. 

The user does not directly interact with this CSC, but instead listens for
events indicating image ingestion into the OODS.

.. note:: If you are interested in viewing other branches of this repository append a `/v` to the end of the url link. For example `https://ts-xml.lsst.io/v/`


.. _User_Documentation:

User Documentation
==================

.. This template has the user documentation in a subfolder.
.. However, in cases where the user documentation is extremely short (<50 lines), one may move that content here and remove the subfolder.
.. This will require modification of the heading styles and possibly renaming of the labels.
.. If the content becomes too large, then it must be moved back to a subfolder and reformatted appropriately.

User-level documentation, found at the link below, is aimed at personnel looking to perform the standard use-cases/operations with the CCArchiver.

.. toctree::
    user-guide/user-guide
    :maxdepth: 2

.. _Configuration:

Configuring the CCArchiver
=========================================
.. For CSCs where configuration is not required, this section can contain a single sentence stating so.
   More introductory information can also be added here (e.g. CSC XYZ requires both a configuration file containing parameters as well as several look-up tables to be operational).

The configuration for the CCArchiver is described at the following link.

.. toctree::
    configuration/configuration
    :maxdepth: 1


.. _Development_Documentation:

Development Documentation
=========================

.. This template has the user documentation in a subfolder.
.. However, in cases where the user documentation is extremely short (<50 lines), one may move that content here and remove the subfolder.
.. This will require modification of the heading styles and possibly renaming of the labels.
.. If the content becomes too large, then it must be moved back to a subfolder and reformatted appropriately.

This area of documentation focuses on the classes used, API's, and how to participate to the development of the CCArchiver software packages.

.. toctree::
    developer-guide/developer-guide
    :maxdepth: 1

.. _Version_History:

Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.

The version history of the CCArchiver is found at the following link.

.. toctree::
    version-history
    :maxdepth: 1


.. _Contact_Personnel:

Contact Personnel
=================

For questions not covered in the documentation, emails should be addressed to |CSC_developer| and |CSC_product_owner|.

This page was last modified |today|.

