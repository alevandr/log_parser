from collections import defaultdict

from main import get_stats_from_file
from main import form_report_average

def test_get_stats_from_file_url_count():
    shared_stats = defaultdict(lambda: {"count": 0, "total_responce_time": 0})
    get_stats_from_file(shared_stats, "example1.log")
    assert len(shared_stats) == 5

def test_get_stats_from_file_first_entry_count():
    shared_stats = defaultdict(lambda: {"count": 0, "total_responce_time": 0})
    get_stats_from_file(shared_stats, "example1.log")
    first_entry = next(iter(shared_stats.values()))
    assert first_entry['count'] == 21

def test_get_stats_from_file_first_entry_avg_responce_time():
    shared_stats = defaultdict(lambda: {"count": 0, "total_responce_time": 0})
    get_stats_from_file(shared_stats, "example1.log")
    first_entry = next(iter(shared_stats.values()))
    assert round(first_entry['total_responce_time'], 3) == 0.896

def test_form_report_average_1_input_no_date():
    table_data = form_report_average(["example1.log"])
    assert table_data[0] == ['/api/context/...', 21, '0.043']

def test_form_report_average_2_input_no_date():
    table_data = form_report_average(["example1.log", "example2.log"])
    assert table_data[0] == ['/api/context/...', 43928, '0.019']

def test_form_report_average_1_input_with_date():
    table_data = form_report_average(["example1.log"], date="2025-22-06")
    assert table_data[0] == ['/api/context/...', 21, '0.043']

def test_form_report_average_2_input_with_date():
    table_data = form_report_average(["example1.log", "example2.log"], date="2025-22-06")
    assert table_data[0] == ['/api/context/...', 2564, '0.023']
