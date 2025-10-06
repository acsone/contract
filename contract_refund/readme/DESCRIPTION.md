This module allows stopping a contract line even after it has been invoiced.

When the stop date is earlier than the last invoiced date, the system will:

- Automatically create a refund invoice for the period between the stop date and the last invoiced date.
- Adjust the `last_date_invoiced` of the contract line to match the stop date.
- Proceed with the normal stop process.

This ensures that users can gracefully handle early contract terminations without manual refund management.
