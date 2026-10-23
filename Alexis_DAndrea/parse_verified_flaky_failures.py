#!/usr/bin/env python3

import csv
from pathlib import Path

VERIFIED_TESTS_FILE = "verified_test_names.csv"

NONDEX_TESTS = {
    "com.taobao.arthas.core.view.ObjectViewTest.testNestedClass",
    "com.taobao.arthas.core.view.ObjectViewTest.testObjectTooLarge",
    "junit.samples.SimpleTest.testAdd",
    "junit.samples.SimpleTest.testEquals",
    "org.junit.samples.SimpleTest.testEquals",
    "org.junit.internal.MethodSorterTest.testJvmMethodSorter"
}

IDFLAKIES_LOGS = [
    "results",
    "submission/results"
]

NONDEX_EVIDENCE = "nondex_failures.txt"

verified_tests = []

with open(VERIFIED_TESTS_FILE, newline="") as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        if row:
            verified_tests.append(row[0].strip())


def classify_tool(test):
    return "NonDex" if test in NONDEX_TESTS else "iDFlakies"


results = []
valid_count = 0

with open("valid_failure_logs.txt", "w", encoding="utf-8") as evidence:

    nondex_text = ""

    if Path(NONDEX_EVIDENCE).exists():
        nondex_text = Path(
            NONDEX_EVIDENCE
        ).read_text(errors="ignore")

    for test in verified_tests:

        tool = classify_tool(test)

        status = "NOT_FOUND"
        evidence_source = ""

        #######################################################################
        # NONDEX
        #######################################################################

        if tool == "NonDex":

            method = test.split(".")[-1]

            if (
                f"{method}(" in nondex_text
                and (
                    "<<< FAILURE!" in nondex_text
                    or
                    "<<< ERROR!" in nondex_text
                )
            ):

                status = "VERIFIED_NONDEX_FAILURE"

                evidence_source = (
                    "nondex_failures.txt"
                )

                valid_count += 1

                evidence.write(
                    "=" * 80 + "\n"
                )

                evidence.write(
                    f"TEST: {test}\n"
                )

                evidence.write(
                    "TOOL: NonDex\n"
                )

                evidence.write(
                    "RULE: testName + <<< FAILURE! detected\n"
                )

                evidence.write(
                    "SOURCE: nondex_failures.txt\n"
                )

                evidence.write(
                    "=" * 80 + "\n\n"
                )

            results.append([
                tool,
                test,
                status,
                evidence_source
            ])

            continue

        #######################################################################
        # IDFLAKIES
        #######################################################################

        found = False

        for root in IDFLAKIES_LOGS:

            root_path = Path(root)

            if not root_path.exists():
                continue

            for log in root_path.rglob(
                "idflakies.log"
            ):

                try:
                    text = log.read_text(
                        errors="ignore"
                    )

                except Exception:
                    continue

                #
                # Support both styles:
                #
                # Verified com.foo.Bar.testMethod
                #
                # and
                #
                # Verified com.foo.Bar#testMethod()
                #

                class_name = ".".join(
                    test.split(".")[:-1]
                )

                method_name = test.split(".")[-1]

                dot_style = (
                    f"Verified {test}"
                )

                hash_style = (
                    f"Verified {class_name}"
                    f"#{method_name}()"
                )

                if (
                    dot_style not in text
                    and
                    hash_style not in text
                ):
                    continue

                verification_patterns = [
                    "expected ERROR, got ERROR",
                    "expected FAILURE, got FAILURE",
                    "expected PASS, got PASS"
                ]

                matched = False

                for pattern in verification_patterns:

                    if pattern in text:
                        matched = True
                        break

                if not matched:
                    continue

                status = (
                    "VERIFIED_IDFLAKIES_DETECTOR"
                )

                evidence_source = str(log)

                valid_count += 1

                found = True

                evidence.write(
                    "=" * 80 + "\n"
                )

                evidence.write(
                    f"TEST: {test}\n"
                )

                evidence.write(
                    "TOOL: iDFlakies\n"
                )

                evidence.write(
                    f"SOURCE: {log}\n"
                )

                evidence.write(
                    "RULE: Verified TEST + matching detector result\n"
                )

                evidence.write(
                    "=" * 80 + "\n\n"
                )

                break

            if found:
                break

        results.append([
            tool,
            test,
            status,
            evidence_source
        ])

###############################################################################
# CSV OUTPUT
###############################################################################

with open(
    "corrected_results.csv",
    "w",
    newline=""
) as out:

    writer = csv.writer(out)

    writer.writerow([
        "tool",
        "test_name",
        "status",
        "evidence_source"
    ])

    writer.writerows(results)

###############################################################################
# REPORT
###############################################################################

with open(
    "parsing_report.txt",
    "w"
) as report:

    report.write(
f"""
FAILURE PARSING REPORT
======================

Professor Requirement
---------------------

Build failures are not counted as flaky failures.

Tool Separation
---------------

iDFlakies = Order Dependent

NonDex = Implementation Dependent

Tools are analyzed independently.

NonDex Parsing Rule
-------------------

A test is valid when:

testName(...)

and

<<< FAILURE!

or

<<< ERROR!

appear in the extracted NonDex failure evidence.

Evidence Source:
nondex_failures.txt

iDFlakies Parsing Rule
----------------------

A test is valid when:

Verified TEST_NAME

appears in idflakies.log together with
a successful detector verification such as:

expected ERROR, got ERROR

expected FAILURE, got FAILURE

expected PASS, got PASS

Evidence Source:
idflakies.log

Verified Tests Audited
----------------------
"""
    )

    for test in verified_tests:
        report.write(test + "\n")

    report.write(
f"""

Summary
-------

Valid Findings: {valid_count}

Total Tests Audited: {len(verified_tests)}
"""
    )

###############################################################################
# SUMMARY
###############################################################################

print()
print("=" * 70)
print("FLAKY TEST AUDIT COMPLETE")
print("=" * 70)
print()

print(f"Valid Findings: {valid_count}")
print(f"Tests Audited : {len(verified_tests)}")

print()
print("Generated:")
print("  corrected_results.csv")
print("  valid_failure_logs.txt")
print("  parsing_report.txt")
print()
