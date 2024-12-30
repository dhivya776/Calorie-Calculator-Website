from django_cron import CronJobBase, Schedule
from django.conf import settings

from django.core.management import call_command
import os
import logging

logger = logging.getLogger(__name__)

class UpdateCustomerExcelCronJob(CronJobBase):
    code = 'Fityfeed.download_customer_details_cron'
    schedule = Schedule(run_every_mins=60)

    def do(self):
        try:
            call_command('download_customer_details')
            logger.info("Customer details Excel file updated successfully.")
        except Exception as e:
            logger.error(f"Error in UpdateCustomerExcelCronJob: {e}")
