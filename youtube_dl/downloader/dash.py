from __future__ import unicode_literals

import itertools

from .fragment import FragmentFD
from ..compat import compat_urllib_error
from ..utils import (
    DownloadError,
    urljoin,
)
from ..compat import compat_HTTPError

branch_coverage = {
    "real_download_1": False,  # if branch for fragments is None
    "real_download_2": False,  # if branch for not is_live
    "real_download_3": False,  # try branch in for loop
    "real_download_4": False   # except branch in for loop
}

class DashSegmentsFD(FragmentFD):
    """
    Download segments in a DASH manifest
    """

    FD_NAME = 'dashsegments'

    def real_download(self, filename, info_dict):
        self.report_destination(filename)
        tmpfilename = self.temp_name(filename)

        is_live = info_dict.get('is_live')

        ctx = {
            'filename': filename,
            'total_frags': None,
        }

        fragments = info_dict.get('fragments', [])

        if fragments is None:
            branch_coverage["real_download_1"] = True
            return False

        branch_coverage["real_download_2"] = True if not is_live else branch_coverage["real_download_2"]
        if not is_live:
            self.report_progress(ctx)

        success = True

        fragment_retries = self.params.get('fragment_retries', 10)
        frag_index = 0

        for fragment in fragments:
            frag_index += 1
            try:
                success &= self._download_fragment(ctx, fragment, info_dict)
                branch_coverage["real_download_3"] = True
            except compat_HTTPError as err:
                success = False
                self.report_retry(err, frag_index, fragment_retries)
                if not self._retry_fragment(ctx, fragment, info_dict):
                    break
                branch_coverage["real_download_4"] = True

        self._finish_frag_download(ctx)

        if not success:
            return False

        self._append_fragment(ctx, None)

        return True