********************************
Test Plan for Manila Fuel plugin
********************************

Table of contents
==================

1. `Introduction`_
2. `Governing Evaluation Mission`_
3. `Test Approach`_
4. `Deliverables`_
5. `Test Cycle Structure`_
6. Test Scope:
     a) `Operations list`_
     b) `System tests list`_
     c) `Functional tests list`_

.. _Introduction:

Introduction
============

1.1.Purpose
-----------
This document describes Master Test Plan for Manila  Fuel Plugin. The scope of this plan defines the following objectives:
 - describe testing activities;
 - outline testing approach, test types, test cycles that will be used;
 - test mission;
 - deliverables;

1.2.Intended Audience
---------------------
This document is intended for Manila  project team staff (QA and Dev engineers and managers) all other persons who are interested in testing results.

.. _Governing Evaluation Mission:

Governing Evaluation Mission
=============================

There is the Manila project that provides a shared file system service for OpenStack. It's the new OpenStack project that provides coordinated access to shared or distributed file systems. The Manila has multiple storage backends (to support vendor or file system specific nuances/capabilities) that could work simultaneously on one environment.
The Fuel Manila plugin adds utilization the corresponding OpenStack service in an Fuel environment.

2.1. Evaluation Test Mission
----------------------------
- Lab environment deployment.
- Deploy MOS with developed plugin installed.
- Create and run specific tests for plugin/deployment.
- Documentation

2.2. Test items
---------------

- Manila UI;
- Fuel CLI;
- Fuel API;
- Fuel UI;
- MOS UI;
- MOS API.

.. _Test Approach:

Test Approach
=============

The project test approach consists of BVT, Acceptance Integration/System and Regression test levels.

3.1 Criteria for test process starting
--------------------------------------

Before test process can be started it is needed to make some preparation actions - to execute important preconditions.The following steps must be executed successfully for starting test phase:
 - all project requirements are reviewed and confirmed;
 - implementation of testing features has finished (a new build is ready for testing);
 - implementation code is stored in GIT;
 - bvt-tests are executed successfully (100% success);
 - test environment is prepared with correct configuration;
 - test environment contains the last delivered build for testing;
 - test plan is ready and confirmed internally;
 - implementation of manual tests and necessary autotests has finished.

3.2. Suspension Criteria
------------------------

Testing of a particular feature is suspended if there is a blocking issue which prevents tests execution. Blocking issue can be one of the following:
 - Feature has a blocking defect, which prevents further usage of this feature 	and there is no workaround available;
 - CI test automation scripts failure.

3.3. Feature Testing Exit Criteria
----------------------------------

Testing of a feature can be finished when:
 - All planned tests (prepared before) for the feature are executed;
 - no defects are found during this run;
 - All planned tests for the feature are executed;
 - defects found during this run are verified or confirmed to be acceptable (known issues);

The time for testing of that feature according to the project plan has run out and Project Manager confirms that no changes to the schedule are possible.

.. _Deliverables:

Deliverables
============

4.1 List of deliverables
------------------------

Project testing activities are to be resulted in the following reporting documents:
 - Test plan;
 - Test run report from TestRail;

4.2. Acceptance criteria
------------------------

 90% of tests cases should be with status - passed. Critical and high issues are fixed.
 Manual tests should be executed and pass:


**Steps:**
 1. Deploy cluster with Manila  plugin enabled.
 2. TBD

.. _Test Cycle Structure:

Test Cycle Structure
====================

An ordinary test cycle for each iteration consists of the following steps:
 - Smoke testing of each build ready for testing;
 - Verification testing of each build ready for testing;
 - Regression testing cycles in the end of iteration;
 - Creation of a new test case for covering of a new found bug (if such test does not exist).

5.1.1 Smoke Testing
-------------------

Smoke testing is intended to check a correct work of a system after new build delivery. Smoke tests allow to be sure that all main system functions/features work correctly according to customer requirements.

5.1.2 Verification testing
--------------------------

Verification testing includes functional testing covering the following:
new functionality (implemented in the current build);
critical and major defect fixes (introduced in the current build).
Some iteration test cycles also include non-functional testing types described in Overview of Planned Tests.

5.1.3 Regression testing
------------------------
Regression testing includes execution of a set of test cases for features implemented before current iteration to ensure that following modifications of the system haven't introduced or uncovered software defects. It also includes verification of minor defect fixes introduced in the current iteration.

5.1.4 Bug coverage by new test case
-----------------------------------
Bug detection starts after all manual and automated tests are prepared and test process initiated. Ideally, each bug must be clearly documented and covered by test case. If a bug without a test coverage was found it must be clearly documented and covered by custom test case to prevent occurrence of this bug in future deployments/releases etc. All custom manual test cases suppose to be added into TestRail and automated tests suppose to be pushed to Git/Gerrit repo.

5.2 Metrics
-----------

Test case metrics are aimed to estimate a quality of bug fixing;detect not executed tests and schedule their execution. 
 - Passed / Failed test cases - this metric shows results of test cases execution, especially, a ratio between test cases passed successfully and failed ones. Such statistics must be gathered after each delivered build test. This will help to identify a progress in successful bugs fixing. Ideally, a count of failed test cases should aim to a zero.
 - Not Run test cases - this metric shows a count of test cases which should be run within a current test phase (have not run yet). Having such statistics, there is an opportunity to detect and analyze a scope of not run test cases, causes of their non execution and planning of their further execution (detect time frames, responsible QA)

Test Scope
==========

.. include:: operations_list.rst
.. include:: test_suite_system.rst
.. include:: test_suite_functional.rst
