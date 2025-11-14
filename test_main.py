import pytest
import os
import json
from main import load_tasks, save_tasks, view_tasks, add_task, delete_task, FILENAME

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
    yield
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

def test_load_tasks_empty_file():
    assert load_tasks() == []

def test_load_tasks_invalid_json():
    with open(FILENAME, 'w', encoding='utf-8') as f:
        f.write("invalid json")
    assert load_tasks() == []

def test_load_tasks_not_a_list():
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump({"key": "value"}, f)
    assert load_tasks() == []

def test_save_tasks():
    tasks = [{"title": "Test Task", "priority": "High"}]
    save_tasks(tasks)
    with open(FILENAME, 'r', encoding='utf-8') as f:
        saved_tasks = json.load(f)
    assert saved_tasks == tasks

def test_view_tasks_empty(capsys):
    view_tasks([])
    captured = capsys.readouterr()
    assert "Список задач пуст." in captured.out

def test_view_tasks_non_empty(capsys):
    tasks = [{"title": "Task 1", "priority": "Low"}, {"title": "Task 2", "priority": "Medium"}]
    view_tasks(tasks)
    captured = capsys.readouterr()
    assert "1. Task 1 — [Low]" in captured.out
    assert "2. Task 2 — [Medium]" in captured.out

def test_add_task(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda prompt: "New Task" if "название" in prompt else "High")
    tasks = []
    add_task(tasks)
    assert len(tasks) == 1
    assert tasks[0] == {"title": "New Task", "priority": "High"}

def test_delete_task_success(monkeypatch):
    tasks = [{"title": "Task 1", "priority": "Low"}]
    monkeypatch.setattr('builtins.input', lambda prompt: "1")
    delete_task(tasks)
    assert len(tasks) == 0

def test_delete_task_invalid_number(capsys, monkeypatch):
    tasks = [{"title": "Task 1", "priority": "Low"}]
    monkeypatch.setattr('builtins.input', lambda prompt: "2")
    delete_task(tasks)
    captured = capsys.readouterr()
    assert "Некорректный номер задачи." in captured.out

def test_delete_task_not_an_integer(capsys, monkeypatch):
    tasks = [{"title": "Task 1", "priority": "Low"}]
    monkeypatch.setattr('builtins.input', lambda prompt: "invalid")
    delete_task(tasks)
    captured = capsys.readouterr()
    assert "Ошибка: введён неверный номер задачи." in captured.out
