from whitenoise.storage import CompressedManifestStaticFilesStorage


class CustomManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
        manifest_strict = False  
        def post_process(self, *args, **kwargs):
            processed_files = super().post_process(*args, **kwargs)
            print("Manifest contents:", self.manifest)
            return processed_files  