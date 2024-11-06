# FirebaseXL

## Running Tests with xvfb

To run the tests for this project, you need to use a virtual display. This can be achieved by using `xvfb` (X Virtual Framebuffer) which is a display server implementing the X11 display server protocol.

### Steps to run tests with xvfb

1. Install `xvfb`:
   ```sh
   sudo apt-get install xvfb
   ```

2. Run `xvfb` before running the tests:
   ```sh
   xvfb-run -a python -m unittest discover -s tests
   ```

Alternatively, you can update your GitHub Actions workflow to include the installation and usage of `xvfb` before running the tests.
