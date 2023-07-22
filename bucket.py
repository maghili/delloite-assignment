from upath import UPath
import os



class Bucket():

    def __init__(self, bucket:str, cloud:bool = False):

        if not bucket:
            raise "No Bucket is Provided"
        if cloud:
            #assuming this is gcs
            self.bucket=UPath("gs://"+bucket)
        else:
            self.bucket = UPath(bucket)
            if not self.bucket.exists() or not self.bucket.is_dir():
                # make this a logger if there is time
                print("the bucket does not exists setting to default ./buckets")
                self.bucket=UPath(os.path.abspath("."))/"buckets"
                print(self.bucket)


    def get_file(self, path):
        file_path = self.bucket/path 
        print(file_path)
        with open(file_path, 'r', encoding="latin") as f:
            return f.read()
        

    def exists(self, path):
        file_path = self.bucket/path 
        return file_path.exists()
    
    def isdir(self, path):
        full_path = self.bucket/path 
        return full_path.isdir()