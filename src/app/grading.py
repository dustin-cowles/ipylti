""" Helper functions for grading assignments """
from datetime import datetime
import logging

from pylti1p3.grade import Grade


def submit_asignment(message_launch):
    """
    Marks the assignment as complete in the LMS.

    :param message_launch: The message launch.

    :returns: None
    """
    logging.info("Submitting assignment for launch_id %s", message_launch.get_launch_id())
    grading_service = message_launch.get_ags()
    launch_data = message_launch.get_launch_data()
    user_id = launch_data["https://purl.imsglobal.org/spec/lti/claim/lti1p1"]["user_id"]
    logging.debug("user_id: %s", user_id)

    grade = Grade()
    grade.set_timestamp(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000'))
    grade.set_activity_progress('Completed')
    grade.set_grading_progress('PendingManual')
    grade.set_user_id(user_id)

    grading_service.put_grade(grade)
