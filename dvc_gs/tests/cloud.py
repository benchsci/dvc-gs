import uuid

from dvc.testing.cloud import Cloud
from dvc.testing.path_info import CloudURLInfo

GS_BUCKET = "dvc-temp"


class GCP(Cloud, CloudURLInfo):

    IS_OBJECT_STORAGE = True

    @property
    def config(self):
        return {"url": self.url, "projectname": "dvc-test"}

    @staticmethod
    def _get_storagepath():
        return GS_BUCKET + "/" + str(uuid.uuid4())

    @staticmethod
    def get_url():
        return "gs://" + GCP._get_storagepath()

    @property
    def _gc(self):
        from google.cloud.storage import Client

        return Client()

    @property
    def _bucket(self):
        return self._gc.bucket(self.bucket)

    @property
    def _blob(self):
        return self._bucket.blob(self.path)

    def is_file(self):
        if self.path.endswith("/"):
            return False

        return self._blob.exists()

    def is_dir(self):
        dir_path = self / ""
        return bool(list(self._bucket.list_blobs(prefix=dir_path.path)))

    def exists(self):
        return self.is_file() or self.is_dir()

    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        assert mode == 0o777
        assert parents

    def write_bytes(self, contents):
        assert isinstance(contents, bytes)
        self._blob.upload_from_string(contents)

    def read_bytes(self):
        return self._blob.download_as_string()