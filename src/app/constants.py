""" Constants used by the application. """
import re

# Roles passed from the tool consumer.
ADMIN_ROLE = "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator"
INSTRUCTOR_ROLE = "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Instructor"
STUDENT_ROLE = "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Student"

JUPYTER_TOKEN_REGEX = re.compile(r"\?token=(.*)$")
CONTAINER_NAME = "ipylti-jupyter"
JUPYTER_IMAGE = "nb"
