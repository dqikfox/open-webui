1. **Fix `ModuleNotFoundError: No module named 'open_webui'`**: The Python tests (`tests/unit/test_oasis_agent.py`) are failing because `open_webui` isn't found. This usually means `PYTHONPATH` needs to include `backend/`, or the test runner is being executed incorrectly, or we just need to install the current project in editable mode via `pip install -e .` from the `backend/` directory. Alternatively, `open_webui` should be added to `PYTHONPATH`. Looking at `.github/workflows/ci.yml`, it just runs `pytest tests/unit/`. I'll add `export PYTHONPATH="$PWD"` or `pip install -e .` to the workflow or install it properly.

2. **Fix PyAudio issue on 3.12**: PyAudio is still failing to build on python 3.12, likely because I'm installing `portaudio19-dev` but it isn't sufficient or Python 3.12 requires an updated version. Let's install `python3-pyaudio` from apt-get, or upgrade pip properly in the workflow, but wait, looking at the logs, it still says "portaudio.h: No such file or directory" during the Python 3.11/3.12 test! This means `sudo apt-get install -y portaudio19-dev` isn't running or isn't successful on those specific matrix environments or I didn't update all python matrix environments in `.github/workflows/ci.yml`.

3. **Check .github/workflows/ci.yml**: Let me explore `.github/workflows/ci.yml` again to see why `portaudio19-dev` wasn't installed for the other backend test matrices. Ah! There are *multiple* jobs or multiple `pip install -r requirements.txt` occurrences in the workflow file. I'll need to make sure I caught all of them.

4. **Verify Action Version**: The workflow has `actions/cache@v3`, `actions/checkout@v4`, `actions/setup-python@v4`. It's better to update `actions/cache@v3` to `actions/cache@v4` as the warning says.

5. **Submit fixes**.
