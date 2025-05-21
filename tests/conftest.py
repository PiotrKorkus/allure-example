from datetime import datetime

import pytest
from pytest_metadata.plugin import metadata_key


@pytest.fixture
def fixture_global():
    return "global"


def pytest_html_report_title(report):
    # Change report title
    report.title = "Report1"


def pytest_configure(config):
    config.stash[metadata_key]["AAA"] = "aaaaaaaa"


def pytest_html_results_table_header(cells):
    # Create additional table headers
    cells.insert(3, "<th>Requirement</th>")
    cells.insert(2, "<th>Description</th>")
    cells.insert(1, '<th class="sortable time" data-column-type="time">Time</th>')


def pytest_html_results_table_row(report, cells):
    # Create additional table columns with TC __doc__ and execution date
    cells.insert(3, f"<td><pre>{report.req}</pre></td>")
    cells.insert(2, f"<td><pre>{report.description}</pre></td>")
    cells.insert(1, f'<td class="col-time">{datetime.now()}</td>')


def get_req(text: str):
    if not text:
        return "None"
    req = text[text.find("REQ") : text.find("REQ") + 7]
    return req


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Extract TC's data
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.req = get_req(item.function.__doc__)


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers():
            name = marker.name
            value = marker.args
            item.user_properties.append((name, value))
