from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment


from .schema import AssignmentGradeSchema, AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint(
    'teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted"""
    submitted_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    submitted_assignments_dump = AssignmentSchema().dump(
        submitted_assignments, many=True)
    return APIResponse.respond(data=submitted_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade the assignment"""

    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    grade_assignment_details = Assignment.grade_assignment(
        _id=grade_assignment_payload.id, grade=grade_assignment_payload.grade, principal=p)

    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(grade_assignment_details)
    return APIResponse.respond(data=graded_assignment_dump)
