"""Given a spec, assuming we're in the homework folder, run the spec against the folder"""

import os

from .warning_unmerged_branches import find_unmerged_branches
from ..common import check_dates
from ..process_file import process_file
from .Record_Result import RecordResult
from ..specs import Spec
from .Submission_Warnings import SubmissionWarnings
from .supporting import import_supporting, remove_supporting


def process_assignment(*,
                       spec: Spec,
                       basedir: str,
                       debug: bool,
                       interact: bool,
                       ci: bool,
                       skip_web_compile: bool) -> RecordResult:
    """Run a spec against the current folder"""
    cwd = os.getcwd()
    try:
        first_submit = ''

        if not ci:
            first_date = check_dates(spec, cwd)
            first_submit = "First Submission for {}: {}".format(spec.id, first_date)

        result = RecordResult(spec_id=spec.id,
                              first_submission=first_submit)

        # prepare the current folder
        supporting_dir, written_files = import_supporting(spec=spec,
                                                          basedir=basedir)
        for file_spec in spec.files:
            file_result = process_file(file_spec=file_spec,
                                       cwd=cwd,
                                       supporting_dir=supporting_dir,
                                       interact=interact,
                                       skip_web_compile=skip_web_compile)
            result.file_results.append(file_result)

        # now we remove any compiled binaries
        remove_execs(spec)

        # and we remove any supporting files
        remove_supporting(written_files)

        return result

    except Exception as err:
        if debug:
            raise err
        else:
            return RecordResult(spec_id=spec.id,
                                warnings=SubmissionWarnings(recording_err=str(err)))


def remove_execs(spec: Spec):
    try:
        for file in spec.files:
            os.remove('{}.exec'.format(file.file_name))
    except FileNotFoundError:
        pass
