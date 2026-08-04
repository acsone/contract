**Contract Line Successor**

This module provides functionality to suspend automatic invoicing for
contracts, with configurable suspension reasons and suspension tracking.

## Features

* Suspend automatic invoicing on a contract.
* Prevent suspended contracts from being included in the automatic invoicing
  process.
* Track the user who suspended automatic invoicing.
* Track the date on which automatic invoicing was suspended.
* Associate a suspension reason with a contract.
* Organize suspension reasons in a hierarchical structure.
* Define whether a suspension reason can be selected.
* Support multi-company suspension reasons.
* Automatically identify the top-level category of a suspension reason.
* Allow automatic invoicing to be resumed by removing the suspension.

Configuration
=============

Automatic Invoice Suspension Reasons
-------------------------------------

Suspension reasons can be configured from:

    Sales > Configuration > Automatic Invoice Suspension Reason

Each reason can have:

* **Name**: the name of the suspension reason.
* **Sequence**: the order in which reasons are displayed.
* **Parent**: an optional parent reason used to create a hierarchy.
* **Can be selected**: determines whether the reason can be selected when
  suspending automatic invoicing.
* **Company**: the company to which the reason belongs.

A reason can be used as a category by creating child reasons underneath it.
For example:

* Maintenance
    * Scheduled Maintenance
    * Emergency Maintenance

When a child reason is selected, its top-level category is automatically
identified.

Usage
=====

Suspend Automatic Invoicing
---------------------------

To suspend automatic invoicing for a contract:

#. Open the contract.
#. Enable **Automatic invoicing suspended**.
#. Select an **Automatic invoicing suspended reason**.

A suspended contract is excluded from the automatic invoicing process.

Resume Automatic Invoicing
---------------------------

To resume automatic invoicing, disable **Automatic invoicing suspended** on
the contract.

The suspension user and suspension date are then cleared.
