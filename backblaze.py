from b2sdk.v2 import B2Api, SqliteAccountInfo, exception
import settings

APPLICATION_KEY_ID = settings.APPLICATION_KEY_ID
APPLICATION_KEY = settings.APPLICATION_KEY
KEY_NAME = settings.KEY_NAME


class Backblaze():
    def __init__(self, appKeyID, appKey):
        # object store credentials, tokens and cache in memory
        # b2sdk.v2.InMemoryAccountInfo - a basic implementation with no persistence
        # b2sdk.v2.SqliteAccountInfo - for console and GUI applications
        info = SqliteAccountInfo()

        # object store credentials, tokens and cache in memory
        self.b2_api = B2Api(info)

        self.b2_api.authorize_account("production", appKeyID, appKey)

    # cannot return buckets if application id is bucket specific
    def list_buckets(self):
        bucket_list = []
        try:
            for b in self.b2_api.list_buckets():
                return bucket_list.append({
                    'id': b.id_,
                    'type': b.type_,
                    'name': b.name
                })
        except exception.RestrictedBucket as e:
            print(e)
            return [{}]

    def get_bucket(self, bucket_name):
        return Bucket(parent=self.b2_api, bucket_name=bucket_name)

    def new_bucket(self, bucket_name, bucket_type):
        return self.b2_api.create_bucket(bucket_name, bucket_type)


class Bucket():
    def __init__(self, parent, bucket_name):
        self.parent = parent
        self.bucket = self.parent.get_bucket_by_name(bucket_name)

    def list_files(self):
        file_list = []
        for file_info, folder_name in self.bucket.ls(recursive=True):
            file_list.append({
                'folder_name':folder_name,
                'file_name':file_info.file_name,
                'timestamp':file_info.upload_timestamp
                })
        return file_list

    def upload_to_bucket(self, local_file_path, b2_file_name, file_info):
        self.bucket.upload_local_file(
            local_file=local_file_path,
            file_name=b2_file_name,
            file_infos=file_info,
        )


def main():
    backblazeObj = Backblaze(APPLICATION_KEY_ID, APPLICATION_KEY)
    bucketObj = backblazeObj.get_bucket('jr-portfolio')
    print(bucketObj.list_files())


if __name__ == "__main__":
    main()
