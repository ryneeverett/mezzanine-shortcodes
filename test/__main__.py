import sys
import textwrap
import subprocess

import testutils


if __name__ == '__main__':
    is_failure = testutils.run_module(
        'test_register', 'test_render', 'test_browser')

    if not is_failure:
        with open('requirements.txt', 'w') as reqs:
            reqs.write(textwrap.dedent("""\
                # This file exists simply as a record of what was installed
                # when the tests passed. Go ahead and commit it.\n"""))

            freeze = subprocess.Popen(
                ['pip', 'freeze', '--local'], stdout=subprocess.PIPE)

            for line in freeze.stdout.readlines():
                line = line.decode()
                if 'mezzanine-shortcodes' not in line:
                    reqs.write(line)

    sys.exit(is_failure)
