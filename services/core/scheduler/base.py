from abc import ABC, abstractmethod
from random import random
from lib.logger import get_logger

logger = get_logger()


class ScheduledJob(ABC):
    @abstractmethod
    def run_automtion(self, **kwargs):
        """
        Run the scheduled job automation.
        This method should be implemented by subclasses to define the job's behavior.
        """
        pass

    def start(self, is_running_flag, thread_lock):
        class_name = self.__class__.__name__
        self.iteration_id = class_name + "-" + random.random()
        logger.info(f"Started {class_name} is_running_flag={is_running_flag}" )

        try:
            is_running_flag[0] = True
            logger.info(f"Started automation {class_name} is_running_flag={is_running_flag}")

            try:
                self.run_automtion()
            except Exception as e:
                logger.exception(f"Error in {class_name} run_automtion: {e}")
                raise

            logger.info(f"Finished automation {class_name} is_running_flag={is_running_flag}")

        except Exception as e:
            logger.exception(f"Error in {class_name} start: {e}")
            raise

        finally:
            with thread_lock:
                is_running_flag[0] = False
                logger.info(f"Class={class_name} is_running_flag={is_running_flag}")