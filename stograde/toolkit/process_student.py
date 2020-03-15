from typing import List

from ..specs import Spec
from ..student import analyze, checkout_date, clone_student, pull, record, remove, reset, stash
from ..student.Student_Result import StudentResult


def process_student(
        student: str,
        *,
        assignments: List[str],
        basedir: str,
        ci: bool,
        clean: bool,
        date: str,
        debug: bool,
        interact: bool,
        no_branch_check: bool,
        no_repo_update: bool,
        specs: List[Spec],
        skip_web_compile: bool,
        stogit_url: str
) -> StudentResult:
    if clean:
        remove(student)
    if not ci:
        clone_student(student, base_url=stogit_url)

    try:
        if not ci:
            stash(student, no_repo_update=no_repo_update)
            pull(student, no_repo_update=no_repo_update)

            checkout_date(student, date=date)

        student_result = StudentResult(name=student)

        record(student, specs=specs, assignments=assignments, basedir=basedir, debug=debug,
               interact=interact, ci=ci, skip_web_compile=skip_web_compile)
        analyze(student_result, specs=specs, check_for_branches=not no_branch_check, ci=ci)

        if date:
            reset(student)

        return student_result

    except Exception as err:
        if debug:
            raise err
        else:
            return StudentResult(name=student, error=err)
