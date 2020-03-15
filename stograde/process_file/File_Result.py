from dataclasses import dataclass, field
from typing import List

from stograde.process_file.Compile_Result import CompileResult
from stograde.process_file.Test_Result import TestResult


@dataclass
class FileResult:
    file_name: str
    compile_results: List[CompileResult] = field(default_factory=list)
    test_results: List[TestResult] = field(default_factory=list)
    file_missing: bool = False
    last_modified: str = ''
    other_files: str = ''
    optional: bool = False
    compile_optional: bool = False
    contents: str = ''
